import marimo

__generated_with = "0.14.16"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import marimo as mo
    import polars as pl
    from datetime import date, datetime
    import uuid
    import altair as alt
    return alt, datetime, mo, pl, uuid


@app.cell
def _():
    from enum import StrEnum

    CONVERSION_VALUE = 2.2046


    class WeightUnits(StrEnum):
        POUNDS = "lbs"
        KILOS = "kg"


    def lbs_to_kg(lbs):
        x = float(lbs) / CONVERSION_VALUE
        return round(x, 2)


    def kg_to_lbs(kg):
        x = float(kg) * CONVERSION_VALUE
        return round(x, 2)
    return WeightUnits, kg_to_lbs, lbs_to_kg


@app.cell
def _(pl):
    from tinydb import Query, TinyDB
    from src import WeightDB, ExerciseDB


    def upsert(data: dict, db: TinyDB, key: str = "id"):
        q = Query()
        db.upsert(data, q[key] == data[key])


    def load_df(db: TinyDB) -> pl.DataFrame:
        return pl.DataFrame(db.all())
    return WeightDB, load_df, upsert


@app.cell(column=1, hide_code=True)
def _(WeightUnits, kg_to_lbs, lbs_to_kg, mo):
    # Not Sure which to start with.
    # Lets get text from marimo.ui.text
    # Wonder if I can integrate server suggestions from it, like fuzzing or something?
    weight_text = mo.ui.text(label=f"Enter Weight")

    unit_radio = mo.ui.radio(
        options=[WeightUnits.POUNDS, WeightUnits.KILOS],
        value=WeightUnits.POUNDS,
        label="Pounds or Kilograms?",
        # on_change=conversions,
    )


    # Define the callback, referencing the widgets
    def conversions(event):
        # Update label and placeholder based on selected unit
        if not weight_text.value:
            return

        try:
            x = float(weight_text.value)
        except:
            return
        if event == WeightUnits.KILOS:
            weight_text.value = lbs_to_kg(x)
        elif event == WeightUnits.POUNDS:
            weight_text.text = kg_to_lbs(x)


    unit_radio._on_change = conversions

    weight_form = (
        mo.md(
            """
        Enter your weekly weight measuerment here.

        {units}

        {weight}
        """
        )
        .batch(units=unit_radio, weight=weight_text)
        .form()
    )

    weight_form
    return (weight_form,)


@app.cell
def _(WeightDB, datetime, mo, upsert, uuid, weight_form):
    units, weight_str = weight_form.element.value.values()
    # weight must have a value, to construct dataframe
    mo.stop(not weight_str, "Enter Weight before running cell.")

    try:
        weight = float(weight_str)
    except ValueError:
        weight = 0.0

    # construct new weigh data
    new_data = {
        "id": str(uuid.uuid4()),
        "weight": weight,
        "unit": units,
        "created": datetime.now().date(),
    }

    # save updates and present dataframe ...
    upsert(new_data, WeightDB, key="created")
    return


@app.cell
def _(WeightDB, load_df):
    weight_df = load_df(WeightDB)
    weight_df
    return (weight_df,)


@app.cell
def _(alt, mo, pl, weight_df):
    filtered_df = weight_df.select(
        pl.col("weight").alias("Weight"), pl.col("created").alias("Date")
    )
    chart = mo.ui.altair_chart(
        alt.Chart(filtered_df).mark_line().encode(x="Date", y="Weight")
    )
    return (chart,)


@app.cell
def _(chart, mo):
    mo.vstack([chart, mo.ui.table(chart.value)])
    return


if __name__ == "__main__":
    app.run()

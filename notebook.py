import marimo

__generated_with = "0.14.15"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import marimo as mo
    import polars as pl
    from datetime import date, datetime
    import uuid
    return datetime, mo, pl, uuid


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
    return WeightUnits, lbs_to_kg, kg_to_lbs


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
def _(WeightUnits, lbs_to_kg, kg_to_lbs, mo):
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
    return


@app.cell
def _(mo):
    mo.md(
        """
    How the fuck do I want to collect exercise data?
    How is it going to be visulized and possibly morphed into usable data?

    What usable data do I need?

    - The name
    - The sets
    - The reps
    - The weights
    - The date / maybe session?
        - that implies recording session data, what does that mean?


    Track how the 3 sets of numbers change and relate, across time?
    """
    )
    return


if __name__ == "__main__":
    app.run()

# Workout and Weigh Tracker

I want to make a Marimo Notebook. This note book will have:

- multiple fields / forms for weight measurements and workouts.

## Feature Request / Scoping

## Intended audience

Me, and potentially other open source, python nerds trying to lose weight or track workout progression.

## Expectation

Make a python notebook (marimo) that will keep track of my numbers and show trend lines.

### Weight measuring Scope

- Input field -> weight as lbs or klg
- Save to DB
- Show chart of weight / time
  - Trend lines
  - Progress tracker?

### Workout Scope

- Main inputs will focus on numbers like reps and sets.
- Intended for weight training, to track number like sets, weight, trend lines per workout
  - maybe trend lines of muscle groups?

- workout input? freeform design? limited?
  - i don't know, but the system should recognize "repeated inputs"
    - i.e. auto suggestions for workout type input?
  - track progression of weight, rep, and sets over time.

### Whole app scope

Save to Sqlite for now? ~ Yes, keep it simple until needs change.
Run in docker? ~ eventually, but locally is fine for now.

from tinydb import TinyDB, JSONStorage

from src.utils import DateTimeSerializer, SerializationMiddleware, DateSerializer



WeightDB = TinyDB("data/weights.db.json", storage=SerializationMiddleware(
    JSONStorage, {"Date": DateSerializer(), "DateTime": DateTimeSerializer()}
))
ExerciseDB = TinyDB("data/exercises.db.json", storage=SerializationMiddleware(
    JSONStorage, {"Date": DateSerializer(), "DateTime": DateTimeSerializer()}
))

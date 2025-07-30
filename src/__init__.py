from tinydb import TinyDB, JSONStorage

from src.utils import DateTimeSerializer, SerializationMiddleware



WeightDB = TinyDB("data/weights.db.json", storage=SerializationMiddleware(
    JSONStorage, {"DateTime": DateTimeSerializer()}
))
ExerciseDB = TinyDB("data/exercises.db.json", storage=SerializationMiddleware(
    JSONStorage, {"DateTime": DateTimeSerializer()}
))

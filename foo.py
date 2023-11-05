from app.index import IndexDB
from pathlib import Path

index = IndexDB(Path("index.db"))

data = index.select_information("c")

print(data)

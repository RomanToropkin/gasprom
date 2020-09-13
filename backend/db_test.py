from backend.db import DB

db = DB()
print(db.get_station_types())

db.create_event(1,1,123123,12.1231232,324.2323123,1234.213124,2424.54545)
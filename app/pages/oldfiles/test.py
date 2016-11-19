from datetime import datetime
from ago import human

now = datetime.now()

timestamp = 1468979619

def date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    dt=datetime(2016,07,22,22,00,01)
    dt=dt.replace(tzinfo=None)
    return human(dt)


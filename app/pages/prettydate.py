import ago
from datetime import datetime
#from ago import human

def date(dt):
    return ago.human(dt, precision=1)


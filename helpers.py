import re 
from datetime import datetime, timedelta

def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, email)): return True
    else: return False

def pickup_date_helper(diff):
    now = datetime.now()
    if diff < 0:
        pickup_date = now + timedelta(days=(7 + diff))
    elif diff == 0:
        pickup_date = now + timedelta(days = 7)
    else: 
        pickup_date = now + timedelta(days = diff)
    return pickup_date

def find_pickup_date(zone):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    now = datetime.now()
    day = now.weekday()
    if zone == 'n':
        pickup_date = now + timedelta(days = (6 - day))
    elif zone == 's':
        diff = 5 - day
        pickup_date = pickup_date_helper(diff)
    elif zone == 'e':
        diff = 4 - day
        pickup_date = pickup_date_helper(diff)
    else:
        diff = 3 - day
        pickup_date = pickup_date_helper(diff)
    return pickup_date.date()



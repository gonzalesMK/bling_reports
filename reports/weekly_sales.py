from .bling.bling_api import BlingClient
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO

week_end = datetime.today()
week_start = week_end + relativedelta(weekday=MO(1))
print(week_end)
print(week_start)

client = BlingClient(api_key="123")
client.list_sales()

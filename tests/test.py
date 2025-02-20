from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
dt = datetime.now(ZoneInfo("Asia/Shanghai"))
print(type(dt))

from datetime import datetime, timezone

dt = datetime.utcnow()
print(dt)

at = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print(at)
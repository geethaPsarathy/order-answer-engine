from datetime import datetime, timedelta

# TTL Calculation (returns expiration timestamp)
def calculate_ttl(hours: int):
    return datetime.utcnow() + timedelta(hours=hours)

# ISO String Conversion
def to_iso_string(dt: datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

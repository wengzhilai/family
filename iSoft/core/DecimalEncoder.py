import json
import datetime
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, data):
        if isinstance(data, decimal.Decimal):
            return float(data)
        elif isinstance(data, datetime.datetime):
            return data.strftime("%Y-%m-%d %H:%M") 
        elif isinstance(data, datetime.date):
            return data.strftime("%Y-%m-%d") 
        elif isinstance(data, datetime.timedelta):
            return (datetime.datetime.min + data).time().isoformat()
        super(DecimalEncoder, self).default(data)
from datetime import datetime, timedelta


class Util:
    @staticmethod
    def get_datetime_list(total_hours):
        # gets datetime list from current UTC time to 5 hours earlier
        now = datetime.utcnow()
        # from 1 because of upload hour
        return [(now - timedelta(hours=i)) for i in range(1, total_hours + 1)]

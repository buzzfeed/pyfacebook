import datetime
import pytz
from pyfacebook import models as m

# This list stores the order in which models should be tested for GET
# Order matters because some models contain others

today = datetime.datetime.now().replace(tzinfo=pytz.utc)
tomorrow = today + datetime.timedelta(days=1)

CONNECTIONS = {
    m.AdAccount: {'adgroupstats': {'adgroup_ids': [1, 2, 3, 4, 5],
                                   'start_time': today,
                                   'end_time': tomorrow,
                                   'stats_mode': 'with_delivery',
                                   }
                  }
}

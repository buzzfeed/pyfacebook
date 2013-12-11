import datetime
import pytz
from pyfacebook import models as m

# This list stores the order in which models should be tested for GET
# Order matters because some models contain others

CONNECTIONS = {
    m.AdAccount: {'adgroupstats': {'adgroup_ids': [1, 2, 3, 4, 5],
                                   'start_time': datetime.datetime(2014, 3, 1).replace(tzinfo=pytz.utc),
                                   'end_time': datetime.datetime(2014, 3, 2).replace(tzinfo=pytz.utc),
                                   'stats_mode': 'with_delivery',
                                   }
                  }
}

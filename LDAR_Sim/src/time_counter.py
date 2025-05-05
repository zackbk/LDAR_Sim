# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Time counter
# Purpose:     Initialize time object and keeps track of simulation time
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

from datetime import date, timedelta

# from statistics import mean

# import pytz
# from timezonefinder import TimezoneFinder


class TimeCounter:
    def __init__(self, start_date, end_date) -> None:
        """
        Initialize a calendar and clock to count through the simulation.

        """
        self._start_date = date(*start_date)
        self._end_date = date(*end_date)
        self.current_date = self._start_date
        return

    def next_day(self):
        """
        Go to the next day in the simulation

        """
        self.current_date += timedelta(days=1)
        return

    def at_simulation_end(self) -> bool:
        if self.current_date > self._end_date:
            return True
        else:
            return False

    # TODO implement a get average lat, lon method in infrastructure
    # and then move the rest of this logic to somewhere in hourly weather,
    # since that is where its used
    #
    # def set_UTC_offset(self, sites):
    #     """
    #     set UTC offset based on average site lat longs

    #     Uses current (now()) offset
    #     """
    #     avg_lat = mean([float(site["lat"]) for site in sites])
    #     avg_lon = mean([float(site["lon"]) for site in sites])
    #     tf = TimezoneFinder()
    #     timezone_str = tf.timezone_at(lng=avg_lon, lat=avg_lat)
    #     # This uses the current time to estimate offset, so if running
    #     # software during DST, then the offset will include DST. Fix this
    #     # someday, by keeping timezone as a site variable and localizing
    #     # every year.
    #     tz_now = date.now(pytz.timezone(timezone_str))
    #     self.UTC_offset = tz_now.utcoffset().total_seconds() / 60 / 60

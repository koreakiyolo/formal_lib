#!/usr/bin/env python3

import pandas as pd
from pandas import DataFrame
from ics import Event, Calendar
from datetime import datetime
OUT_FORMAT = "%Y-%m-%d %H:%M:%S"

EVENT_NAME_KEY = "event_name"
DATE_KEY = "date"
START_KEY = "start"
END_KEY = "end"
COL_KEYS = [EVENT_NAME_KEY, DATE_KEY, START_KEY, END_KEY]
CSV_DATE_FORMAT = "%Y/%m/%d"
CSV_TIME_FORMAT = "%H:%M"


class AdminICS(object):
    def __init__(self, csv):
        self._set_internal_df(csv)
        self.calendar = Calendar()
        self._set_events()

    def _set_internal_df(self, csv):
        self.internal_df = pd.read_csv(csv)
        self.internal_df.columns
        cols_set = set(COL_KEYS)
        cond = cols_set.issubset(
                            self.internal_df.columns)
        if not cond:
            raise TypeError("")

    def _gene_event_from_df(self):
        for i, ser in self.internal_df.iterrows():
            e_ins = Event()
            e_ins.name = ser[EVENT_NAME_KEY]
            date = [int(num)
                    for num in ser[DATE_KEY].split("/")]
            start_elms = [int(num)
                          for num in ser[START_KEY].split(":")]
            end_elms = [int(num)
                        for num in ser[END_KEY].split(":")]
            start_list = date + start_elms
            start_dtime = datetime(*start_list)
            start_info = start_dtime.strftime(OUT_FORMAT)
            end_list = date + end_elms
            end_dtime = datetime(*end_list)
            end_info = end_dtime.strftime(OUT_FORMAT)
            e_ins.begin = start_info
            e_ins.end = end_info
            yield e_ins

    def _set_events(self):
        for e_ins in self._gene_event_from_df():
            self.calendar.events.add(e_ins)
        print("set events.")

    def to_ics(self, ics_file):
        with open(ics_file, "w") as write:
            import ipdb; ipdb.set_trace()
            write.write(str(self.calendar))

    @staticmethod
    def to_base_csv(ocsv):
        dtime = datetime.now()
        event_name = "Unknown event"
        date = dtime.strftime(CSV_DATE_FORMAT)
        start = dtime.strftime(CSV_TIME_FORMAT)
        end = dtime.strftime(CSV_TIME_FORMAT)
        data_list = [event_name, date, start, end]
        df = DataFrame([data_list], columns=COL_KEYS,
                       index=["sample"])
        df.to_csv(ocsv)

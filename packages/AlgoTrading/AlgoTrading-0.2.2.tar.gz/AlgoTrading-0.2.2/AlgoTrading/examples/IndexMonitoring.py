# -*- coding: utf-8 -*-
u"""
Created on 2015-11-19

@author: cheng.li
"""

import datetime as dt
from AlgoTrading.api import Strategy
from AlgoTrading.api import strategyRunner
from AlgoTrading.api import DataSource
from PyFin.api import MA


class MonitoringIndexStrategy(Strategy):

    def __init__(self):
        self.signal = MA(10, 'close')

    def handle_data(self):

        for s in self.universe:
            self.order_to(s, 1, 100)


def run_example():
    universe = ['000300.zicn']
    startDate = dt.datetime(2005, 1, 1)
    endDate = dt.datetime(2015, 11, 1)

    strategyRunner(userStrategy=MonitoringIndexStrategy,
                   symbolList=universe,
                   startDate=startDate,
                   endDate=endDate,
                   dataSource=DataSource.DXDataCenter,
                   freq=0,
                   benchmark='000300.zicn',
                   logLevel="info",
                   saveFile=True,
                   plot=True)


if __name__ == "__main__":
    startTime = dt.datetime.now()
    print("Start: %s" % startTime)
    run_example()
    endTime = dt.datetime.now()
    print("End : %s" % endTime)
    print("Elapsed: %s" % (endTime - startTime))
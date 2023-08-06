# -*- coding: utf-8 -*-
u"""
Created on 2015-9-21

@author: cheng.li
"""

import os
import pandas.io as io
from AlgoTrading.Data.Data import DataFrameDataHandler
from AlgoTrading.Utilities import transfromDFtoDict


class HistoricalCSVDataHandler(DataFrameDataHandler):

    _req_args = ['csvDir', 'symbolList']

    def __init__(self, **kwargs):
        super(HistoricalCSVDataHandler, self).__init__(kwargs['logger'], kwargs['symbolList'])
        self.csvDir = kwargs['csvDir']
        self._openConvertCSVFiles()

    def _openConvertCSVFiles(self):
        combIndex = None
        for s in self.symbolList:
            filePath = os.path.join(self.csvDir, "{0:s}.csv".format(s))
            self.symbolData[s] = io.parsers.read_csv(filePath,
                                                     header=0,
                                                     index_col=0,
                                                     parse_dates=True)\
                .sort_index()

            if combIndex is None:
                combIndex = self.symbolData[s].index
            else:
                combIndex = combIndex.union(self.symbolData[s].index)

            self.symbolData[s] = transfromDFtoDict(self.symbolData[s])

        self.dateIndex = combIndex
        self.start = 0

    def updateInternalDate(self):
        return False

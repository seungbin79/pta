# -*-coding: utf-8-*-
class CoinInfo:

    def __init__(self):
        self.coinName = ''
        self.currency = ''
        self.timeType = ''
        self.timeBucket = ''
        self.source = ''

    def setInitialize(self):
        self.coinName = ''
        self.currency = ''
        self.timeType = ''
        self.timeBucket = ''
        self.source = ''

    def setCoinInfo(self, coinName, currency, timeType, timeBucket, source):
        self.coinName = coinName
        self.currency = currency
        self.timeType = timeType
        self.timeBucket = timeBucket
        self.source = source

    def getFileName(self):
        return self.source + '_' + self.coinName + self.currency + '_' + self.timeType + '_' + self.timeBucket

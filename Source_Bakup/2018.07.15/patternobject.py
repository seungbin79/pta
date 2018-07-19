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


class Pattern :

    def __init__(self):
        self.patMatrix = []
        self.resultPatGroupList = []

    def setPatternMatrix(self, patMatrix):
        self.patMatrix = patMatrix

    def getPatternMatrix(self) :
        return self.patMatrix

    def getResultPatGroupList(self) :
        return self.resultPatGroupList


class ResultPattern :

    def __init__(self):
        self.resultPatMatrix = []
        self.oddsRate = 0
        self.oddsCount = 0

    def setResultPatternMatrix(self, resultPatMatrix):
        self.resultPatMatrix = resultPatMatrix

    def setOddsRate(self, oddsRate):
        self.oddsRate = oddsRate

    def getResultPatternMatrix(self):
        return self.resultPatMatrix

    def getOddsRate(self):
        return self.oddsRate

    def setOddsCount(self, oddsCount):
        self.oddsCount = oddsCount

    def getOddsCount(self):
        return self.oddsCount








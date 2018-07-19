# -*-coding: utf-8-*-
class Coin:

    def __init__(self, code, currency, bucket, bucketType, market):
        self.code = code
        self.currency = currency
        self.bucket = bucket
        self.bucketType = bucketType
        self.market = market

    def __repr__(self):
        return f'Coin({self.code}, {self.currency}, {self.bucket}, {self.bucketType}, {self.market})'

    @property
    def info(self):
        print(f'Coin: {self.code}')
        print(f'Currency: {self.currency}')
        print(f'Bucket: {self.bucket}')
        print(f'BucketType: {self.bucketType}')
        print(f'Market: {self.market}')

    @property
    def filename(self):
        return f'{self.market}_{self.code}{self.currency}_{self.bucketType}_{self.bucket}'


class Chart:

    def __init__(self, coin, timeList=None, valueList=None):
        self.coin = coin

        if timeList is None:
            self.timeList = []
        else:
            self.timeList = timeList

        if valueList is None:
            self.valueList = []
        else:
            self.valueList = valueList

    @property
    def startTime(self):
        return min(self.timeList)

    @property
    def endTime(self):
        return max(self.timeList)

    @property
    def size(self):
        return len(self.timeList)

    def __len__(self):
        return len(self.timeList)

    def __repr__(self):
        return f'Chart({self.coin}, {self.timeList}, {self.valueList})'


class Result(Chart):

    def __init__(self, coin, timeList, valueList):
        super().__init__(coin, timeList, valueList)
        self.appearence = 1

    def addAppearence(self):
        self.appearence += 1


class Pattern(Chart):

    def __init__(self, coin, timeList, valueList, resultGroupList=None):
        super().__init__(coin, timeList, valueList)

        if resultGroupList is None:
            self.resultGroupList = []
        else:
            self.resultGroupList = resultGroupList

    def getAppearenceRate(self, resultIndex):

        total_amount = 0
        for result in self.resultGroupList:
            if isinstance(result, Result):
                total_amount += result.appearence

        return round((self.resultGroupList[resultIndex].appearence / total_amount), 2)

    def __add__(self, other):
        return self.resultGroupList.append(other)





# coin_1 = Coin('a', 'b', 1, 'c', 'd')
#
# print(coin_1)
#
# tl = ['1', '2', '3']
# vl = ['100', '200', '300']
#
# pattern = Pattern(coin_1, tl, vl)
#
# print(help(pattern))
#
# result_1 = Result(coin_1, tl, vl)
# result_2 = Result(coin_1, tl, vl)
# result_3 = Result(coin_1, tl, vl)
# result_4 = Result(coin_1, tl, vl)
#
# pattern.__add__(result_1)
# pattern.__add__(result_2)
# pattern.__add__(result_3)
# pattern.__add__(result_4)
#
# print(pattern.getAppearenceRate(2))
#
# pattern.resultGroup[2].addAppearence()
#
# pattern.resultGroup[2].appearence

# chart_1 = Chart(coin_1, tl, vl)
#
# print(chart_1)
#
# print(len(chart_1))
# print(chart_1.size)
# print(chart_1.startTime)
# print(chart_1.endTime)


# class Pattern :
#
#     def __init__(self):
#         self.patMatrix = []
#         self.resultPatGroupList = []
#
#     def setPatternMatrix(self, patMatrix):
#         self.patMatrix = patMatrix
#
#     def getPatternMatrix(self) :
#         return self.patMatrix
#
#     def getResultPatGroupList(self) :
#         return self.resultPatGroupList
#
#
# class ResultPattern :
#
#     def __init__(self):
#         self.resultPatMatrix = []
#         self.oddsRate = 0
#         self.oddsCount = 0
#
#     def setResultPatternMatrix(self, resultPatMatrix):
#         self.resultPatMatrix = resultPatMatrix
#
#     def setOddsRate(self, oddsRate):
#         self.oddsRate = oddsRate
#
#     def getResultPatternMatrix(self):
#         return self.resultPatMatrix
#
#     def getOddsRate(self):
#         return self.oddsRate
#
#     def setOddsCount(self, oddsCount):
#         self.oddsCount = oddsCount
#
#     def getOddsCount(self):
#         return self.oddsCount








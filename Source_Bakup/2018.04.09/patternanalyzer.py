# -*-coding: utf-8-*-
import pandas as pd
import sys
import os
import patternobject


#패턴비교 모수가 되는 데이터 셋 정보
motherInfo = patternobject.CoinInfo()
motherData = pd.DataFrame()

#패턴비교 대상이 되는 데이터 셋 리스트
patternInfoList = []


def printException():
    message = []
    for e in sys.exc_info():
        message.append(str(e))
    message = '\n'.join(message)
    print(message)
    return message


def initializePatternAnalyzer() :
    global motherData
    global patternInfoList

    motherInfo.setInitialize()
    patternInfoList = []


def setMotherInfo(coinName, currency, timeType, timeBucket, source) :
    global motherInfo

    print('')
    print('=============================================================')
    print('Set Mother Info ...')
    print('=============================================================')
    print(' Coin : ' + coinName)
    print(' Currency : ' + currency)
    print(' TimeType : ' + timeType)
    print(' TimeBucket : ' + timeBucket)
    print(' Source : ' + source)

    motherInfo.setCoinInfo(coinName, currency, timeType, timeBucket, source)


def readMotherData() :
    global motherInfo
    global motherData

    print('')
    print('=============================================================')
    print('Read Mother Data ...')
    print('=============================================================')

    dir = 'Data/' + motherInfo.getFileName() + '.xlsx'

    print(' Filename : ' + dir)

    motherData = pd.read_excel(dir)




if __name__ == "__main__":

    setMotherInfo('NEO','KRW', 'Days', '1', 'Upbit')

    readMotherData()

    # print(motherData)
# -*-coding: utf-8-*-
import pandas as pd
import sys
import os
import patternobject
import math

#글로벌 변수 선언#################################################
##################################################################

#패턴 사이즈 종류
PAT_SIZE_SM = 30
PAT_SIZE_MD = 60
PAT_SIZE_LG = 90
PAT_SIZE_XL = 120
PAT_SIZE_XX = 150

#패턴 높이 설정 : 100개의 Y 버켓 생성
PAT_Y_AXIS = 100
#패턴 봉 갯수 설정
PAT_X_AXIS = 10

#결과 패턴 봉 수
RESULT_PAT_X_AXIS = 33
#결과 패턴 높이 설정
RESULT_PAT_Y_AXIS = 500
#결과 패턴 중심 높이 설정 (결과 패턴의 0 기준 높이)
RESULT_PAT_MY_AXIS = 200




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


def getMax(df) :
    maxes = df[['Open', 'High', 'Low', 'Close']].max()
    return max(maxes)


def getMin(df) :
    mins = df[['Open', 'High', 'Low', 'Close']].min()
    return min(mins)


def getScaledPatternData(df, minValue, maxValue, patternHeight) :

    # 원 값에 min 값을 차감하여 y-axis=0 기준으로 수치를 조정한다.
    df = df.subtract(minValue)

    # 설정된 height를 100 분위 기준으로 수치를 재 조정한다.
    gap = (maxValue - minValue) / patternHeight
    df = df.divide(gap)

    return df


def getSortedPrices(sr) :
    prcList = []

    # 최하위 값 순서로 넣는다.
    prcList.append(sr['Low'])

    if sr['Open'] <= sr['Close'] :
        prcList.append(sr['Open'])
        prcList.append(sr['Close'])
    else :
        prcList.append(sr['Close'])
        prcList.append(sr['Open'])

    # 마지막 최상위 값을 넣는다.
    prcList.append(sr['High'])

    return prcList


def makeMatrix(df, patternSize, patternHeight) :

    # matrix의 의미는 구간으로 생각한다. [0] = [0, 1)
    matrix = [[0 for rows in range(patternHeight)] for cols in range(patternSize)]
    matrixDf = pd.DataFrame()

    # 한 칸이 다 차면 1, 아니면 0, 꼬리는 0.5
    for i in range(patternSize) :
        prList = []

        for j in range(patternHeight) :
            prList = getSortedPrices(df.iloc[i])

            # 셀에 꼬리와 봉이 같이 있으면 봉 기준 값을 갖게 한다.
            if j >= math.floor(prList[0]) and j < math.floor(prList[1]) :
                matrix[i][j] = 0.5
            # 봉은 셀에 침범해 있으면 다 값을 가지게 한다.
            elif j >= math.floor(prList[1]) and j <= prList[2] :
                matrix[i][j] = 1
            elif j > prList[2] and j <= prList[3] :
                matrix[i][j] = 0.5
            else :
                matrix[i][j] = 0

        colName = 'col' + str(i)
        matrixDf[colName] = matrix[i] # DataFrame이 필요한지 잘 모르겠음...

    # print(matrixDf)

    return matrix


def getScaledResultPatternData(df, minValue, maxValue, patternHeight, standardHeight) :

    # 원 값에 min 값을 차감하여 y-axis=0 기준으로 수치를 조정한다.
    df = df.subtract(minValue)

    # 설정된 height를 100 분위 기준으로 수치를 재 조정한다.
    gap = (maxValue - minValue) / patternHeight
    df = df.divide(gap)

    # 최종 0 y축 값을 standard height로 올려준다.
    df = df.add(standardHeight)

    return df



def makePattern(df, startIndex, patternSize, patternHeight) :

    sIndex = 0
    eIndex = 0

    if startIndex < len(df.index):
        sIndex = startIndex
    else:
        return

    if startIndex + patternSize <= len(df.index):
        eIndex = startIndex + patternSize
    else:
        return

    patMaxValue = getMax(df.iloc[sIndex: eIndex])
    patMinValue = getMin(df.iloc[sIndex: eIndex])

    scaledDf = getScaledPatternData(df.iloc[sIndex : eIndex][['Open','High','Low','Close']], patMinValue, patMaxValue, patternHeight)

    # 인풋 패턴을 만들고
    patMatrix = makeMatrix(scaledDf, patternSize, patternHeight)



def makeResultMatrix(df, resultPatSize, resultPatHeight) :

    # matrix의 의미는 구간으로 생각한다. [0] = [0, 1)
    matrix = [[0 for rows in range(resultPatHeight)] for cols in range(resultPatSize)]
    matrixDf = pd.DataFrame()

    # 한 칸이 다 차면 1, 아니면 0, 꼬리는 0.5
    for i in range(resultPatSize):
        prList = []

        for j in range(resultPatHeight):
            prList = getSortedPrices(df.iloc[i])

            # 셀에 꼬리와 봉이 같이 있으면 봉 기준 값을 갖게 한다.
            if j >= math.floor(prList[0]) and j < math.floor(prList[1]):
                matrix[i][j] = 0.5
            # 봉은 셀에 침범해 있으면 다 값을 가지게 한다.
            elif j >= math.floor(prList[1]) and j <= prList[2]:
                matrix[i][j] = 1
            elif j > prList[2] and j <= prList[3]:
                matrix[i][j] = 0.5
            elif prList[0] <= 0 or prList[1] <= 0 or prList[2] <= 0 or prList[3] <= 0 :
                matrix[i][j] = 0
            elif prList[0] >= resultPatHeight or prList[1] >= resultPatHeight or prList[2] >= resultPatHeight or prList[3] >= resultPatHeight :
                matrix[i][j] = resultPatHeight
            else :
                matrix[i][j] = 0

        colName = 'col' + str(i)
        matrixDf[colName] = matrix[i]  # DataFrame이 필요한지 잘 모르겠음...

    # print(matrixDf)

    return matrix



def makeResultPattern(df, startIndex, patternSize, patternHeight, resultPatSize, resultPatHeight, resultPatStandardHeight) :

    sIndex = 0
    eIndex = 0

    if startIndex < len(df.index) :
        sIndex = startIndex
    else :
        return

    if startIndex + patternSize <= len(df.index) :
        eIndex = startIndex + patternSize
    else :
        return


    patMaxValue = getMax(df.iloc[sIndex : eIndex])
    patMinValue = getMin(df.iloc[sIndex : eIndex])



    if startIndex + patternSize < len(df.index) :
        sIndex = startIndex + patternSize
    else :
        return


    if startIndex + patternSize + resultPatSize <= len(df.index) :
        eIndex = startIndex + patternSize + resultPatSize
    else :
        return


    # 결과 패턴을 만들고 (스케일을 맞출 때는 인풋 패턴 기준으로 스케일을 맞춘 후, 높이를 추가로 더해준다.)
    scaledResultDf = getScaledResultPatternData(df.iloc[sIndex : eIndex][['Open', 'High', 'Low', 'Close']], patMinValue, patMaxValue, patternHeight, resultPatStandardHeight)

    resultPatMatrix = makeResultMatrix(scaledResultDf, resultPatSize, resultPatHeight)


if __name__ == "__main__":

    setMotherInfo('NEO','KRW', 'Days', '1', 'Upbit')

    readMotherData()

    makePattern(motherData, 0, PAT_X_AXIS, PAT_Y_AXIS)

    makeResultPattern(motherData, 0, PAT_X_AXIS, PAT_Y_AXIS, RESULT_PAT_X_AXIS, RESULT_PAT_Y_AXIS, RESULT_PAT_MY_AXIS)

    # 해당 패턴의 존재 여부를 체크하여

    # 신규 페턴으로 저장할지 아니면 기존 패턴에 결과 패턴을 추가할지
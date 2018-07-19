# -*-coding: utf-8-*-
import pandas as pd
import sys
import os
import patternobject
import math
import pickle
import gzip

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

# 동일 패턴 일치율 수치
SIMILAR_RATE_CRITERIA = 0.8
# 결과 패턴 일치율 수치
SIMILAR_RATE_RESULT_CRITERIA = 0.9


#패턴그룹은 글로벌 변수로 잡는다.
patternGroupList = []


def loadPicke() :
    global patternGroupList
    global PAT_X_AXIS
    global RESULT_PAT_X_AXIS

    # 입력 봉 수 + 결과 취합 봉 수
    filename = 'Pattern/' + 'pattern_' + str(PAT_X_AXIS) + '_' + str(RESULT_PAT_X_AXIS) + '.pickle'

    with gzip.open(filename, 'rb') as f:
        patternGroupList = pickle.load(f)



def savePickle() :
    global patternGroupList
    global PAT_X_AXIS
    global RESULT_PAT_X_AXIS

    # 입력 봉 수 + 결과 취합 봉 수
    filename = 'Pattern/' + 'pattern_' + str(PAT_X_AXIS) + '_' + str(RESULT_PAT_X_AXIS) + '.pickle'

    with gzip.open(filename, 'wb') as f :
        pickle.dump(patternGroupList, f)



def setPatternParameter(pat_x_axis, result_pat_y_axis, similar_rate_criteria, similar_rate_result_criteria) :
    global PAT_X_AXIS
    global RESULT_PAT_Y_AXIS
    global SIMILAR_RATE_CRITERIA
    global SIMILAR_RATE_RESULT_CRITERIA

    PAT_X_AXIS                   = pat_x_axis
    RESULT_PAT_Y_AXIS            = result_pat_y_axis
    SIMILAR_RATE_CRITERIA        = similar_rate_criteria
    SIMILAR_RATE_RESULT_CRITERIA = similar_rate_result_criteria




def printException():
    message = []
    for e in sys.exc_info():
        message.append(str(e))
    message = '\n'.join(message)
    print(message)
    return message



def getMotherInfo(coinName, currency, timeType, timeBucket, source) :

    print('')
    print('=============================================================')
    print('Get Mother Info ...')
    print('=============================================================')
    print(' Coin : ' + coinName)
    print(' Currency : ' + currency)
    print(' TimeType : ' + timeType)
    print(' TimeBucket : ' + timeBucket)
    print(' Source : ' + source)

    motherInfo = patternobject.CoinInfo()
    motherInfo.setCoinInfo(coinName, currency, timeType, timeBucket, source)

    return motherInfo



def readMotherData(motherInfo) :

    print ('')
    print ('=============================================================')
    print ('Read Mother Data ...')
    print ('=============================================================')

    dir = 'Data/' + motherInfo.getFileName() + '.xlsx'

    print (' Filename : ' + dir)
    print ('')

    motherData = pd.read_excel(dir)

    return motherData


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
    # return matrixDf

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


    return patMatrix



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
    # return matrixDf



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

    return resultPatMatrix



# 패턴 비교 메소드
# - standPatMatrix: 비교 기준 Matrix, comparePatMatrix: 비교 할 Matrix
# - Return 값: 일치율
def comparePatternMatrix(standPatMatrix, comparePatMatrix) :

    total_amount = sum([sum(x) for x in standPatMatrix])
    total_cal = 0

    for x in range(0, len(standPatMatrix), 1) :
        for y in range(0, len(standPatMatrix[x]), 1) :
            sub_cal = 0
            if standPatMatrix[x][y] == 0.5 and comparePatMatrix[x][y] == 0.5 :
                sub_cal = 0.5
            else :
                sub_cal = standPatMatrix[x][y] * comparePatMatrix[x][y]

            total_cal = total_cal + sub_cal


    # print (total_cal / total_amount)

    return total_cal / total_amount



# PatternGroup에 patMatrix를 등록한다.
def registerPatternGroup(patMatrix, resultPatMatrix) :
    global patternGroupList
    global SIMILAR_RATE_CRITERIA

    # 기존에 패턴을 임시 저장하기 위한 check 변수
    check_rate = 0
    check_patClass = patternobject.Pattern()

    # pattern group list를 돌리면서 기존에 저장된 group 을 조사한다.
    for groupPatClass in patternGroupList :
        groupPatMatrix = groupPatClass.getPatternMatrix()

        similar_rate = comparePatternMatrix(groupPatMatrix, patMatrix)

        # 가장 높은 일치율을 가지는 pattern class 를 찾아 check에 저장한다.
        if similar_rate > check_rate :
            check_rate = similar_rate
            check_patClass = groupPatClass


    # 일치율 조건 비율보다 낮다면 신규 pattern group을 생성한다.
    if check_rate < SIMILAR_RATE_CRITERIA :
        newPatClass = patternobject.Pattern()
        newPatClass.setPatternMatrix(patMatrix)
        patternGroupList.append(newPatClass)

        print ('Create new pattern... patternGroup Size = ', len(patternGroupList))

        return registerResultPatternGroup(newPatClass, resultPatMatrix)
    # 일치율 조건 비율보다 높은 대상이 있는 경우, 해당 pattern class에 결과 pattern 저장
    else :

        print ('Existed pattern... patternGroup Size = ', len(patternGroupList))

        return registerResultPatternGroup(check_patClass, resultPatMatrix)


def registerResultPatternGroup(patternClass, resultPatMatrix) :
    global SIMILAR_RATE_RESULT_CRITERIA

    resultPatGroupList = patternClass.getResultPatGroupList()

    # 기존에 패턴을 임시 저장하기 위한 check 변수
    check_rate = 0
    check_resultPatClass = patternobject.ResultPattern()

    for groupResultPatClass in resultPatGroupList :
        groupResultPatMatrix = groupResultPatClass.getResultPatternMatrix()

        similar_rate = comparePatternMatrix(groupResultPatMatrix, resultPatMatrix)

        if similar_rate > check_rate :
            check_rate = similar_rate
            check_resultPatClass = groupResultPatClass


    if check_rate < SIMILAR_RATE_RESULT_CRITERIA :
        newResultPatClass = patternobject.ResultPattern()
        newResultPatClass.setResultPatternMatrix(resultPatMatrix)
        newResultPatClass.setOddsCount(newResultPatClass.getOddsCount() + 1)

        patternClass.getResultPatGroupList().append(newResultPatClass)

        print (' -----> Create new result pattern... resultPatternGroup Size = ',
               len(patternClass.getResultPatGroupList()) )

    else :
        check_resultPatClass.setOddsCount(check_resultPatClass.getOddsCount() + 1)

        print (' -----> Add existed result pattern... resultPatternGroup Size = ',
               len(patternClass.getResultPatGroupList()))


def getPatternGroupSize() :
    global patternGroupList

    return len(patternGroupList)


def getPatternGroup(index) :
    global patternGroupList

    return patternGroupList[index]







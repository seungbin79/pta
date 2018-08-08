# -*-coding: utf-8-*-
import pandas as pd
import sys
import os
import math
from datetime import datetime as dt
import patternobject as po
from ptlib import matrixfunction as mf
import pickle
import gzip
import logging


# logging 처리 부분 =====================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s|%(levelname)s|%(name)s] %(message)s')

file_handler = logging.FileHandler(f"Log/log_{dt.now().strftime('%Y%m%d%H%M%S')}.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#=======================================================================================

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
#결과 패턴 높이 설정
RESULT_PAT_Y_AXIS = 1000
#결과 패턴 중심 높이 설정 (결과 패턴의 0 기준 높이)
RESULT_PAT_MY_AXIS = 500

# 동일 패턴 일치율 수치
SIMILAR_RATE_CRITERIA = 0.5
# 결과 패턴 일치율 수치
SIMILAR_RATE_RESULT_CRITERIA = 0.5



#패턴그룹은 글로벌 변수로 잡는다.
patternGroupList = []


def loadPicke(coin, pat_x_axis, result_pat_x_axis):
    global patternGroupList

    # 입력 봉 수 + 결과 취합 봉 수
    filename = f'Pattern/{coin.filename}_{pat_x_axis}_{result_pat_x_axis}.pickle'

    try:
        with gzip.open(filename, 'rb') as f:
            patternGroupList = pickle.load(f)
    except FileNotFoundError as e:
        logger.exception(e)


def savePickle(coin, pat_x_axis, result_pat_x_axis):
    global patternGroupList

    # 입력 봉 수 + 결과 취합 봉 수
    filename = f'Pattern/{coin.filename}_{pat_x_axis}_{result_pat_x_axis}.pickle'

    with gzip.open(filename, 'wb') as f :
        pickle.dump(patternGroupList, f)


def readMotherData(coin):

    print('')
    print('=============================================================')
    print('Read Mother Data ...')
    print('=============================================================')

    dir = f'Data/{coin.filename}.xlsx'

    print(f' Filename: {dir}\n\n')


    motherData = pd.read_excel(dir)

    return motherData


def makePattern(coin, df, startIndex, patternSize, patternHeight) :

    def getMax(df):
        maxes = df[['Open', 'High', 'Low', 'Close']].max()
        return max(maxes)

    def getMin(df):
        mins = df[['Open', 'High', 'Low', 'Close']].min()
        return min(mins)

    sIndex = 0
    eIndex = 0

    if startIndex + patternSize < len(df.index):
        # df.iloc[start:end] 사용시 end는 x < end 방식이므로 +1 되도록 end index 설정한다.
        # df.iloc[start:end] --> start <= x < end
        sIndex = startIndex
        eIndex = startIndex + patternSize
    else:
        return

    patMaxValue = getMax(df.iloc[sIndex:eIndex])
    patMinValue = getMin(df.iloc[sIndex:eIndex])

    scaledDf = mf.getScaledPatternData(df.iloc[sIndex:eIndex][['Open','High','Low','Close']],
                                       patMinValue, patMaxValue, patternHeight)

    # 인풋 패턴을 만들고
    patMatrix = mf.makeMatrix(scaledDf, patternSize, patternHeight)
    
    # 날짜 변환 해 준다. string --> date
    sr_time = df.iloc[sIndex:eIndex]['TimeKst'].str.replace('T', ' ')
    sr_time = pd.to_datetime(sr_time, format='%Y-%m-%d %H:%M:%S')


    # pattern 객체를 생성한다.
    pattern = po.Pattern(coin, sr_time.tolist(), patMatrix)

    return pattern



def makeResultPattern(coin, df, startIndex, patternSize, patternHeight,
                      resultPatSize, resultPatHeight, resultPatStandardHeight):

    def getMax(df):
        maxes = df[['Open', 'High', 'Low', 'Close']].max()
        return max(maxes)

    def getMin(df):
        mins = df[['Open', 'High', 'Low', 'Close']].min()
        return min(mins)

    sIndex = 0
    eIndex = 0

    if startIndex + patternSize < len(df.index):
        # df.iloc[start:end] 사용시 end는 x < end 방식이므로 +1 되도록 end index 설정한다.
        # df.iloc[start:end] --> start <= x < end
        sIndex = startIndex
        eIndex = startIndex + patternSize
    else:
        return


    patMaxValue = getMax(df.iloc[sIndex:eIndex])
    patMinValue = getMin(df.iloc[sIndex:eIndex])


    if startIndex + patternSize + resultPatSize < len(df.index):
        sIndex = startIndex + patternSize
        eIndex = startIndex + patternSize + resultPatSize
    else :
        return


    # 결과 패턴을 만들고 (스케일을 맞출 때는 인풋 패턴 기준으로 스케일을 맞춘 후, 높이를 추가로 더해준다.)
    scaledResultDf = mf.getScaledPatternData(df.iloc[sIndex:eIndex][['Open', 'High', 'Low', 'Close']],
                                             patMinValue, patMaxValue, patternHeight, resultPatStandardHeight)

    # 결과 패턴을 만들고...
    resultPatMatrix = mf.makeResultMatrix(scaledResultDf, resultPatSize, resultPatHeight)


    # 날짜 변환 해 준다. string --> date
    sr_time = df.iloc[sIndex:eIndex]['TimeKst'].str.replace('T', ' ')
    sr_time = pd.to_datetime(sr_time, format='%Y-%m-%d %H:%M:%S')

    resultPattern = po.Result(coin, sr_time.tolist(), resultPatMatrix)

    return resultPattern



def registerPatternGroup(pattern, resultPattern):

    # PatternGroup에 Pattern 등록한다.

    global patternGroupList
    global SIMILAR_RATE_CRITERIA

    # 기존에 패턴을 임시 저장하기 위한 check 변수
    check_rate = 0
    check_pattern = pattern

    # pattern group list를 돌리면서 기존에 저장된 pattern 을 조사한다.
    for p in patternGroupList:
        gp_patMatrix = p.valueList

        similar_rate = mf.comparePatternMatrix(gp_patMatrix, pattern.valueList)

        # 가장 높은 일치율을 가지는 pattern class 를 찾아 check에 저장한다.
        if similar_rate > check_rate :
            check_rate = similar_rate
            check_pattern = p


    # 일치율 조건 비율보다 낮다면 신규 pattern group을 생성한다.
    if check_rate < SIMILAR_RATE_CRITERIA:
        patternGroupList.append(pattern)

        print ('Create new pattern... patternGroup Size = ', len(patternGroupList))

        return registerResultPatternGroup(pattern, resultPattern)

    # 일치율 조건 비율보다 높은 대상이 있는 경우, 해당 pattern class에 결과 pattern 저장
    else:

        print ('Existed pattern... patternGroup Size = ', len(patternGroupList))

        return registerResultPatternGroup(check_pattern, resultPattern)


def registerResultPatternGroup(pattern, resultPattern):
    global SIMILAR_RATE_RESULT_CRITERIA

    resultPatGroupList = pattern.resultGroupList

    # 기존에 패턴을 임시 저장하기 위한 check 변수
    check_rate = 0
    check_result_pattern = resultPattern

    for r in resultPatGroupList:
        gp_resultPatMatrix = r.valueList

        similar_rate = mf.comparePatternMatrix(gp_resultPatMatrix, resultPattern.valueList)

        if similar_rate > check_rate :
            check_rate = similar_rate
            check_result_pattern = r


    if check_rate < SIMILAR_RATE_RESULT_CRITERIA :
        pattern.__add__(resultPattern)

        print (' -----> Create new result pattern... resultPatternGroup Size = ',
               len(pattern.resultGroupList))

    else :
        check_result_pattern.addAppearence()

        print (' -----> Add existed result pattern... resultPatternGroup Size = ',
               len(pattern.resultGroupList))



def createPattern(coin, motherData, pat_x_axis, result_pat_x_axis) :

    # x 축 값은 사용자가 지정한다. (time period 결정)
    # y 축 값은 선 지정된 값을 사용한다. (높이 scale은 미리 지정되어야 한다.)

    global PAT_Y_AXIS
    global RESULT_PAT_Y_AXIS
    global RESULT_PAT_MY_AXIS

    for i in range(0, len(motherData) - max(pat_x_axis, result_pat_x_axis), 1) :
        pattern = makePattern(coin, motherData, i, pat_x_axis, PAT_Y_AXIS)

        if pattern is None:
            print('There is no pattern object...')
            continue

        resultPattern = makeResultPattern(coin, motherData, i, pat_x_axis, PAT_Y_AXIS,
                                          result_pat_x_axis, RESULT_PAT_Y_AXIS, RESULT_PAT_MY_AXIS)

        if resultPattern is None:
            print('There is no result pattern object...')
            continue

        registerPatternGroup(pattern, resultPattern)


def run() :

    logger.info("patterncreator start ==============================================")

    # neo krw days ====================================================================

    coin = po.Coin('NEO', 'KRW', '1', 'days', 'Upbit')
    loadPicke(coin, 30, 33)
    motherData = readMotherData(coin)
    createPattern(coin, motherData, 30, 33)
    savePickle(coin, 30, 33)


    # # neo krw mins ====================================================================
    # coin = po.Coin('NEO', 'KRW', '60', 'minutes', 'Upbit')
    # motherData = readMotherData(coin)
    # createPattern(coin, motherData, 30, 33)
    #
    # coin = po.Coin('NEO', 'KRW', '240', 'minutes', 'Upbit')
    # motherData = readMotherData(coin)
    # createPattern(coin, motherData, 30, 33)

    # # neo btc days ====================================================================
    # motherInfo = getMotherInfo('NEO', 'BTC', 'Days', '1', 'Upbit')
    # motherData = readMotherData(motherInfo)
    #
    # createPattern(motherData, 30, 33)
    #
    # # neo btc mins ====================================================================
    # motherInfo = getMotherInfo('NEO', 'BTC', 'minutes', '60', 'Upbit')
    # motherData = readMotherData(motherInfo)
    #
    # createPattern(motherData, 30, 33)
    #
    # motherInfo = getMotherInfo('NEO', 'BTC', 'minutes', '240', 'Upbit')
    # motherData = readMotherData(motherInfo)
    #
    # createPattern(motherData, 30, 33)
    #
    # # save pickle ====================================================================
    # savePickle(30, 33)








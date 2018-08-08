import pandas as pd
import math
from datetime import datetime as dt

import logging

# logging 처리 부분 =====================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s|%(levelname)s|%(name)s] %(message)s')

file_handler = logging.FileHandler(f"Log/log_{dt.now().strftime('%Y%m%d%H%M%S')}.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#=======================================================================================


def convertMatrixToCandleDataframe(matrix) :

    df = pd.DataFrame(columns=['seq', 'open', 'high', 'low', 'close'])

    for i in range(0, len(matrix), 1):
        seq = i + 1

        open = -1
        high = -1
        low = -1
        close = -1

        k = 0
        for j in range(0, len(matrix[i]), 1):
            if matrix[i][j] >= 0.5:
                low = j
                k = j
                break

        for j in range(k, len(matrix[i]), 1):
            if matrix[i][j] == 1:
                open = j
                k = j
                break

        for j in range(k, len(matrix[i]), 1):
            if matrix[i][j] <= 0.5:
                close = j
                k = j
                break

        for j in range(k, len(matrix[i]), 1):
            if matrix[i][j] == 0:
                high = j
                break

            if matrix[i][len(matrix[i]) - 1] > 0 and j == len(matrix[i]) - 1:
                high = j + 1
                break

        list = [seq, open, high, low, close]
        df.loc[len(df)] = list

    return df


def getScaledPatternData(df, minValue, maxValue, patternHeight, standardHeight=None) :

    # 원 값에 min 값을 차감하여 y-axis=0 기준으로 수치를 조정한다.
    df = df.subtract(minValue)

    # 설정된 height를 100 분위 기준으로 수치를 재 조정한다.
    gap = (maxValue - minValue) / patternHeight
    df = df.divide(gap)

    if standardHeight is not None:
        # 최종 0 y축 값을 standard height로 올려준다.
        df = df.add(standardHeight)

    return df


def getSortedPrices(sr):
    prcList = []

    # 최하위 값 순서로 넣는다.
    prcList.append(sr['Low'])

    if sr['Open'] <= sr['Close']:
        prcList.append(sr['Open'])
        prcList.append(sr['Close'])
    else:
        prcList.append(sr['Close'])
        prcList.append(sr['Open'])

    # 마지막 최상위 값을 넣는다.
    prcList.append(sr['High'])

    return prcList


def makeMatrix(df, patternSize, patternHeight) :

    # matrix의 의미는 구간으로 생각한다. [0] = [0, 1)
    matrix = [[0 for rows in range(patternHeight)] for cols in range(patternSize)]
    # matrixDf = pd.DataFrame()

    # 한 칸이 다 차면 1, 아니면 0, 꼬리는 0.5
    for i in range(patternSize) :
        prList = []
        prList = getSortedPrices(df.iloc[i])

        for j in range(patternHeight) :

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

        # colName = 'col' + str(i)
        # matrixDf[colName] = matrix[i] # DataFrame이 필요한지 잘 모르겠음...

    # print(matrixDf)

    return matrix
    # return matrixDf


def makeResultMatrix(df, resultPatSize, resultPatHeight) :

    # matrix의 의미는 구간으로 생각한다. [0] = [0, 1)
    matrix = [[0 for rows in range(resultPatHeight)] for cols in range(resultPatSize)]
    # matrixDf = pd.DataFrame()

    # 한 칸이 다 차면 1, 아니면 0, 꼬리는 0.5
    for i in range(resultPatSize):
        prList = []

        prList = getSortedPrices(df.iloc[i])

        if (prList[0] >= resultPatHeight
                or prList[1] >= resultPatHeight
                or prList[2] >= resultPatHeight
                or prList[3] >= resultPatHeight) :

            matrix[i][resultPatHeight - 1] = 1

            continue


        for j in range(resultPatHeight):

            # 셀에 꼬리와 봉이 같이 있으면 봉 기준 값을 갖게 한다.
            if j >= math.floor(prList[0]) and j < math.floor(prList[1]):
                matrix[i][j] = 0.5
            # 봉은 셀에 침범해 있으면 다 값을 가지게 한다.
            elif j >= math.floor(prList[1]) and j <= prList[2]:
                matrix[i][j] = 1
            elif j > prList[2] and j <= prList[3]:
                matrix[i][j] = 0.5
            else :
                matrix[i][j] = 0

            if (j + 1 == resultPatHeight) :
                if (prList[0] >= resultPatHeight
                        or prList[1] >= resultPatHeight
                        or prList[2] >= resultPatHeight
                        or prList[3] >= resultPatHeight) :

                    matrix[i][j] = 1


        # colName = 'col' + str(i)
        # matrixDf[colName] = matrix[i]  # DataFrame이 필요한지 잘 모르겠음...

    # print(matrixDf)

    return matrix
    # return matrixDf


def comparePatternMatrix(standPatMatrix, comparePatMatrix):
    # 패턴 비교 메소드
    # - standPatMatrix: 비교 기준 Matrix, comparePatMatrix: 비교 할 Matrix
    # - Return 값: 일치율

    total_amount = sum([sum(x) for x in standPatMatrix])
    total_cal = 0

    for x in range(0, len(standPatMatrix), 1):
        for y in range(0, len(standPatMatrix[x]), 1):
            sub_cal = 0
            if standPatMatrix[x][y] == 0.5 and comparePatMatrix[x][y] == 0.5:
                sub_cal = 0.5
            else:
                sub_cal = standPatMatrix[x][y] * comparePatMatrix[x][y]

            total_cal = total_cal + sub_cal

    # print (total_cal / total_amount)
    logger.debug(f'total_cal = {total_cal}, total_amount = {total_amount}')

    return total_cal / total_amount
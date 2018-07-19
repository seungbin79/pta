import patterncreator as pc
import pandas as pd
from ptlib import matrixfunction as mf


pc.run()

# from ptlib import matrixfunction  as mf
#
# ptclass = pc.getPatternGroup(5)
# ptmatrix = ptclass.getPatternMatrix()
#
# df = mf.convertMatrixToCandleDataframe(ptmatrix)
#
# writer = pd.ExcelWriter('output.xlsx')
# df.to_excel(writer, 'Sheet1')
# writer.save()
#
# resultclass = ptclass.getResultPatGroupList()[0]
# resultmatrix = resultclass.getResultPatternMatrix()
# ptmatrix = ptclass.getPatternMatrix()
#
#
#
#
#
#
# df_result = mf.convertMatrixToCandleDataframe(resultmatrix)
#
# writer = pd.ExcelWriter('output_result.xlsx')
# df_result.to_excel(writer, 'Sheet1')
# writer.save()










# lt = pc.getPatternGroup(526)
#
# rlt = lt.getResultPatGroupList()
#
# print (pc.getPatternGroupSize())
#
#
# import pandas as pd
#
# labels = ['idx','Open','High','Low','Close']
#
# df = pd.DataFrame.from_records(rlt.getResultPatternMatrix(), columns=labels)




# motherInfo = pc.getMotherInfo('NEO','KRW', 'Days', '1', 'Upbit')
#
# motherData = pc.readMotherData(motherInfo)
#
# for i in range(3) :
#     patMatrix = pc.makePattern(motherData, i, pc.PAT_X_AXIS, pc.PAT_Y_AXIS)
#
#     resultPatMatrix = pc.makeResultPattern(motherData, i
#                                            , pc.PAT_X_AXIS
#                                            , pc.PAT_Y_AXIS
#                                            , pc.RESULT_PAT_X_AXIS
#                                            , pc.RESULT_PAT_Y_AXIS
#                                            , pc.RESULT_PAT_MY_AXIS)
#
#     pc.registerPatternGroup(patMatrix, resultPatMatrix)





# pc.savePickle()
#
# pc.patternGroupList = []
#
# pc.patternGroupList
#
# pc.loadPicke()
#
# print (pc.patternGroupList)
#
# for i in range(motherData.size - pc.PAT_X_AXIS) :
#     patMatrix = pc.makePattern(motherData, i, pc.PAT_X_AXIS, pc.PAT_Y_AXIS)
#
#     resultPatMatrix = pc.makeResultPattern(motherData, i
#                                            , pc.PAT_X_AXIS
#                                            , pc.PAT_Y_AXIS
#                                            , pc.RESULT_PAT_X_AXIS
#                                            , pc.RESULT_PAT_Y_AXIS
#                                            , pc.RESULT_PAT_MY_AXIS)
#
#     pc.registerPatternGroup(patMatrix, resultPatMatrix)




# patMatrix = pc.makePattern(motherData, 0, pc.PAT_X_AXIS, pc.PAT_Y_AXIS)
#
# resultPatMatrix = pc.makeResultPattern(motherData, 0
#                                        , pc.PAT_X_AXIS
#                                        , pc.PAT_Y_AXIS
#                                        , pc.RESULT_PAT_X_AXIS
#                                        , pc.RESULT_PAT_Y_AXIS
#                                        , pc.RESULT_PAT_MY_AXIS)
#
#
#
# pc.registerPatternGroup(patMatrix, resultPatMatrix)
#
#
#
#
# patMatrix = pc.makePattern(motherData, 1, pc.PAT_X_AXIS, pc.PAT_Y_AXIS)
#
# resultPatMatrix = pc.makeResultPattern(motherData, 1
#                                        , pc.PAT_X_AXIS
#                                        , pc.PAT_Y_AXIS
#                                        , pc.RESULT_PAT_X_AXIS
#                                        , pc.RESULT_PAT_Y_AXIS
#                                        , pc.RESULT_PAT_MY_AXIS)
#
# pc.registerPatternGroup(patMatrix, resultPatMatrix)


# 해당 패턴의 존재 여부를 체크하여

# 신규 페턴으로 저장할지 아니면 기존 패턴에 결과 패턴을 추가할지



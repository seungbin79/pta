import patterncreator as pc

motherInfo = pc.getMotherInfo('NEO','KRW', 'Days', '1', 'Upbit')

motherData = pc.readMotherData(motherInfo)

for i in range(3) :
    patMatrix = pc.makePattern(motherData, i, pc.PAT_X_AXIS, pc.PAT_Y_AXIS)

    resultPatMatrix = pc.makeResultPattern(motherData, i
                                           , pc.PAT_X_AXIS
                                           , pc.PAT_Y_AXIS
                                           , pc.RESULT_PAT_X_AXIS
                                           , pc.RESULT_PAT_Y_AXIS
                                           , pc.RESULT_PAT_MY_AXIS)

    pc.registerPatternGroup(patMatrix, resultPatMatrix)





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



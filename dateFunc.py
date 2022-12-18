from datetime import datetime
import re

from dbFunc import changeGoalToDone, getGoalByAccount

def stringToDatetime(s, timeType):
    if timeType == 'target':
        L = re.split('-| |:', s)
        return datetime(int(L[0]), int(L[1]), int(L[2]), int(L[3]), int(L[4]), int(L[5]))
    else:
        L = s.split('-')
        if timeType == 'start':
            return datetime(int(L[0]), int(L[1]), int(L[2]))
        elif timeType == 'end':
            return datetime(int(L[0]), int(L[1]), int(L[2]), 23, 59, 59)

def recordInTheRange(dateRange, record):
    d_start = stringToDatetime(dateRange['start'], 'start')
    d_end = stringToDatetime(dateRange['end'], 'end')
    newRecord = []
    for i in record:
        d_target = stringToDatetime(i[4], 'target')
        if d_start <= d_target and d_target <= d_end:
            newRecord.append(i)
    return newRecord

def goalInTheRange(dateRange, goal):
    d_start = stringToDatetime(dateRange['start'], 'start')
    d_end = stringToDatetime(dateRange['end'], 'end')
    newGoal = []
    for i in goal:
        d_target = stringToDatetime(i[3], 'start')
        if d_start <= d_target and d_target <= d_end:
            newGoal.append(i)
    return newGoal

def determineGoalDone(loginStats, cursor, conn, goal, record):
    for i in goal:
        if i[4] == False:
            goalDone(cursor, conn, i, record)
    return getGoalByAccount(loginStats, cursor)

def goalDone(cursor, conn, goalItem, record):
    for r in record:
        if r[1] == goalItem[1]:
            if r[4].split(' ')[0] == goalItem[3]:
                if r[2]>=goalItem[2] and r[3]>=goalItem[2]:
                    changeGoalToDone(cursor, conn, goalItem)
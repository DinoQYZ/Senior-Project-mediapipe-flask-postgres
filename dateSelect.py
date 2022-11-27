from datetime import datetime
import re

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

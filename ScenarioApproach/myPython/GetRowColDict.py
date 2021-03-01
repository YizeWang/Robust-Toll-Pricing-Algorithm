def GetRowColDict(rows, cols):

    currRow = None
    currCol = []
    retCols = {}

    for i in range(len(rows)):

        if rows[i] == currRow or currRow == None:
            currCol.append(cols[i])
        else:
            retCols[currRow] = currCol
            currCol = []
            currCol.append(cols[i])
        
        currRow = rows[i]

    retCols[currRow] = currCol

    return set(rows), retCols
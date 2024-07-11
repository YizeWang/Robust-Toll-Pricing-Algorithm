def GetNonZeroDictionary(A):

    rows, cols = A.nonzero()  # extract index arrays of sparse matrix

    prevRow = None    # previous row
    currColList = []  # column index list of current row
    retCols = {}      # row-col dictionary

    for i in range(len(rows)):

        currRow = rows[i]
        currCol = cols[i]

        if currRow != prevRow and prevRow is not None:
            retCols[prevRow] = currColList
            currColList = []
        
        currColList.append(currCol)
        prevRow = rows[i]

    retCols[prevRow] = currColList

    return set(rows), retCols

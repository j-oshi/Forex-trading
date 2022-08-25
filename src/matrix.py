def matrix(list_matrix, seperator=''):
    # row = []
    # for i in list_matrix:
    #     column = []
    #     for j in list_matrix:
    #         if i == j:
    #             k = 0
    #         else:
    #             k = i + seperator + j
    #         column.append(k)
    #     row.append(column)
    # return row
    return [[i + seperator + j if i != j else 0 for i in list_matrix] for j in list_matrix]

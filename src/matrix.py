def matrix(list_matrix):
    """
        row = []
        for i in var_list:
            column = []
            for j in var_list:
                if i == j:
                    k = 0
                else:
                    k = i + j
                column.append(k)
            row.append(column)
        return row
    """
    return [[i + j if i != j else 0 for i in list_matrix] for j in list_matrix]



    
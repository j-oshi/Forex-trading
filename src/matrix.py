def matrix(var_list):
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
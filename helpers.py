import numpy as np
def arr_to_matrix(arr,m_width):
    M = []
    for i in range(m_width):
        l_b = m_width * i
        u_b = m_width * (i+1)
        M.append(arr[l_b:u_b])
    return M

def matrix_to_int(M):
    flat = np.array(M).flatten()
    x = ""
    for num in flat:
        x += (str(num))
    return int(x)
def get_location(M,value):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == value:
                return (i,j)
            
def pretty_print(matrix):
    print("_______")
    for row in matrix:
        for entry in row:
            print(entry, " ",end="")
        print("")
    print("_______")
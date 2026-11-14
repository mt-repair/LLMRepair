import math
from Original import *


def mat_transpose(A):
    row = len(A)
    column = len(A[0])
    B = []
    for i in range(column):
        temp = []
        for j in range(0, row):
            temp.append(A[j][i])
        B.append(temp)
    return B


def mat_copy(A):
    B = []
    for i in range(len(A)):
        temp = []
        for j in range(len(A[0])):
            temp.append(A[i][j])
        B.append(temp)
    return B


def AssertMRViolation(ftc_output, ftc_expected_output):
    d = 0.00001
    row = len(ftc_expected_output)
    col = len(ftc_expected_output[0])
    if not (row == len(ftc_output) and col == len(ftc_output[0])):
        return True
    for i in range(row):
        for j in range(col):
            if math.fabs(ftc_output[i][j] - ftc_expected_output[i][j]) >= d:
                return True
    return False


def getIdentityMatrix(dim):
    I = []
    for i in range(dim):
        temp = []
        for j in range(dim):
            if i == j:
                temp.append(1)
            else:
                temp.append(0)
        I.append(temp)
    return I


"""Return a square matrix, which is transformed by exchanging two rows of an Identity matrix."""


def getPMatrix(dim):
    if dim < 2:
        print("Cannot compound, since matrix has less than two rows!")
        sys.exit(-1)
    P = getIdentityMatrix(dim)
    temp = P[0]
    P[0] = P[1]
    P[1] = temp
    return P


"""Return a square Q matrix, whose principle diagonal elements are all constant c."""


def getQMatrix(dim, constant):
    Q = []
    for i in range(dim):
        temp = []
        for j in range(dim):
            if i == j:
                temp.append(constant)
            else:
                temp.append(0)
        Q.append(temp)
    return Q


"""Return a matrix, whose elements are all scaled with the given scalar. """


def mat_multiple_constant(matrix, scalar):
    scaled_matrix = mat_copy(matrix)
    for i in range(len(scaled_matrix)):
        for j in range(len(scaled_matrix[0])):
            scaled_matrix[i][j] = scaled_matrix[i][j] * scalar
    return scaled_matrix


def mat_addition(A, B):
    C = []
    if not (len(A) == len(B) and len(A[0]) == len(B[0])):
        print("Can not compound!\n Matrix addition failure, since they do not have the same dimension.")
        sys.exit(-1)
    for i in range(len(A)):
        temp = []
        for j in range(len(A[0])):
            temp.append(A[i][j] + B[i][j])
        C.append(temp)
    return C


def MR1(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    ftc_A = mat_transpose(otc_B)
    ftc_B = mat_transpose(otc_A)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_transpose(ori_output)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR2(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_A))
    ftc_A, symbol = Smm().MatMul((P, otc_A))
    ftc_B = mat_copy(otc_B)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((P, ori_output))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR3(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_B[0]))
    ftc_A = mat_copy(otc_A)
    ftc_B, symbol = Smm().MatMul((otc_B, P))
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((ori_output, P))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR4(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    Q = getQMatrix(len(otc_A), 3)
    ftc_A, symbol = Smm().MatMul((Q, otc_A))
    ftc_B = mat_copy(otc_B)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((Q, ori_output))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR5(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    Q = getQMatrix(len(otc_A), 4)
    ftc_B, symbol = Smm().MatMul((otc_B, Q))
    ftc_A = mat_copy(otc_A)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((ori_output, Q))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR6(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    scalar = 6
    ftc_A = mat_multiple_constant(otc_A, scalar)
    ftc_B = mat_copy(otc_B)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_multiple_constant(ori_output, scalar)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR7(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    scalar = 7
    ftc_B = mat_multiple_constant(otc_B, scalar)
    ftc_A = mat_copy(otc_A)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_multiple_constant(ori_output, scalar)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR8(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    dim = len(otc_A)
    I = getIdentityMatrix(dim)
    ftc_A = mat_addition(otc_A, I)
    ftc_B = mat_copy(otc_B)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_addition(ori_output, otc_B)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR9(mat, dynamic):
    otc_A = mat[0]
    otc_B = mat[1]
    dim = len(otc_B)
    I = getIdentityMatrix(dim)
    ftc_A = mat_copy(otc_A)
    ftc_B = mat_addition(otc_B, I)
    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_addition(otc_A, ori_output)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR10(mat, dynamic):
    #  Prior MR1
    otc_A = mat[0]
    otc_B = mat[1]
    ftc_A = mat_transpose(otc_B)
    ftc_B = mat_transpose(otc_A)
    # ori_output, symbol = matmultiple.MatMul((otc_A, otc_B))
    # mrs_output, symbol = matmultiple.MatMul((ftc_A, ftc_B))
    # ftc_expected_output = mat_transpose(ori_output)    #  in MR2
    otc_A = ftc_A
    otc_B = ftc_B
    P = getPMatrix(len(otc_A))
    ftc_A, symbol = Smm().MatMul((P, otc_A))
    ftc_B = mat_copy(otc_B)

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((P, ori_output))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR11(mat, dynamic):
    #  Prior MR1
    otc_A = mat[0]
    otc_B = mat[1]
    ftc_A = mat_transpose(otc_B)
    ftc_B = mat_transpose(otc_A)
    # ori_output, symbol = matmultiple.MatMul((otc_A, otc_B))
    # mrs_output, symbol = matmultiple.MatMul((ftc_A, ftc_B))
    # ftc_expected_output = mat_transpose(ori_output)

    #  in MR3
    otc_A = ftc_A
    otc_B = ftc_B
    P = getPMatrix(len(otc_B[0]))
    ftc_A = mat_copy(otc_A)
    ftc_B, symbol = Smm().MatMul((otc_B, P))

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((ori_output, P))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR12(mat, dynamic):
    #  Prior MR2
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_A))
    ftc_A, symbol = Smm().MatMul((P, otc_A))
    ftc_B = mat_copy(otc_B)

    #  in MR1
    otc_A = ftc_A
    otc_B = ftc_B
    ftc_A = mat_transpose(otc_B)
    ftc_B = mat_transpose(otc_A)

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_transpose(ori_output)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR13(mat, dynamic):
    #  Prior MR2
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_A))
    ftc_A, symbol = Smm().MatMul((P, otc_A))
    ftc_B = mat_copy(otc_B)

    #  in MR3
    otc_A = ftc_A
    otc_B = ftc_B
    P = getPMatrix(len(otc_B[0]))
    ftc_A = mat_copy(otc_A)
    ftc_B, symbol = Smm().MatMul((otc_B, P))

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((ori_output, P))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR14(mat, dynamic):
    #  Prior MR3
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_B[0]))
    ftc_A = mat_copy(otc_A)
    ftc_B, symbol = Smm().MatMul((otc_B, P))

    #  in MR1
    otc_A = ftc_A
    otc_B = ftc_B
    ftc_A = mat_transpose(otc_B)
    ftc_B = mat_transpose(otc_A)

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output = mat_transpose(ori_output)
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MR15(mat, dynamic):
    #  Prior MR3
    otc_A = mat[0]
    otc_B = mat[1]
    P = getPMatrix(len(otc_B[0]))
    ftc_A = mat_copy(otc_A)
    ftc_B, symbol = Smm().MatMul((otc_B, P))

    #  in MR2
    otc_A = ftc_A
    otc_B = ftc_B
    P = getPMatrix(len(otc_A))
    ftc_A, symbol = Smm().MatMul((P, otc_A))
    ftc_B = mat_copy(otc_B)

    ori_output, symbol = dynamic.MatMul((otc_A, otc_B))
    mrs_output, symbol = dynamic.MatMul((ftc_A, ftc_B))
    ftc_expected_output, symbol = Smm().MatMul((P, ori_output))
    violation = AssertMRViolation(ftc_expected_output, mrs_output)
    if violation:  #  Violated 
        return 1, (ftc_A, ftc_B)
    else:
        return 0, (ftc_A, ftc_B)


def MTG(argv, dynamic):
    source = argv
    follow_case = []
    MG = []
    current_module = sys.modules[__name__]
    for i in range(1, 16):  # MR
        result, follow = getattr(current_module, 'MR'+str(i))(source, dynamic)
        MG.append(result)
        follow_case.append(follow)
    return MG, follow_case

# if __name__ =="__main__":
#     A = [[1, 7, 0, 0], [0, 2, 8, 0], [5, 0, 3, 9], [0, 6, 0, 4]]
#     print(MatMul(A, A))

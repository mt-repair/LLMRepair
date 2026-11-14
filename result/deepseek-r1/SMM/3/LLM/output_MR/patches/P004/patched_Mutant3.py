import sys


class Mutant3:
    def Normalization(self, n, m, c, ic, jc):
        result_c = []
        nz = 0
        for i in range(n):
            temp = []
            for j in range(m):
                temp.append(0)
            result_c.append(temp)
        for i in range(n):
            for j in range(ic[i], ic[i + 1]):
                result_c[i][jc[nz]] = c[nz]
                nz = nz + 1
        return result_c

    def SparseMatMul(self, n, m, a, ia, ja, b, ib, jb):
        nz = 0
        mask = []
        symbol = 0  #  Check if the test case has passed through the error statement. 
        for i in range(m):
            mask.append(-1)
        c = []
        ic = [0]
        jc = []
        for i in range(n):
            ic.append(0)
        for i in range(n * m):
            c.append(0)
            jc.append(0)

        for i in range(0, n):
            for j in range(ia[i], ia[i + 1]):
                neighbour = ja[j]
                aij = a[j]
                for k in range(ib[neighbour], ib[neighbour + 1]):
                    icol_add = jb[k]
                    icol = mask[icol_add]
                    if icol == -1:
                        jc[nz] = icol_add
if nz < len(c):
    c[nz] = aij
    jc[nz] = icol_add
    mask[icol_add] = nz
    nz += 1
    symbol = 1
                        mask[icol_add] = nz
                        nz = nz + 1
                        symbol = 1
                    else:
                        c[icol] = c[icol] + aij * b[k]
            for k in range(ic[i], nz):
                mask[jc[k]] = -1
            ic[i + 1] = nz
        c = c[:ic[-1]]
        jc = jc[:ic[-1]]
        C = self.Normalization(n, m, c, ic, jc)
        return C, symbol

    def CreateSparseMat(self, A):
        a = []
        ia = [0]  #  Why not? 
        ja = []
        off_set = 0
        for i in range(len(A)):
            for j in range(len(A[0])):
                if not A[i][j] == 0:
                    a.append(A[i][j])
                    off_set = off_set + 1
                    ja.append(j)  #  Record Columns Only 
ia.append(off_set)
        return a, ia, ja

    def MatMul(self, mat):
        A = mat[0]
        B = mat[1]
        if not (len(A[0]) == len(B)):
            print("Matrix cannot product!\n Matrix production failure, since they do not match.")
            sys.exit(-1)
        product_row = len(A)
        product_col = len(B[0])
        (a, ia, ja) = self.CreateSparseMat(A)
        (b, ib, jb) = self.CreateSparseMat(B)
        C = self.SparseMatMul(product_row, product_col, a, ia, ja, b, ib, jb)
        return C
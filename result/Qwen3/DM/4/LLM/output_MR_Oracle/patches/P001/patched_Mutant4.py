import math


class Mutant4:
    def Determinant(self, A, n):
        f1 = f2 = f3 = f4 = True  #  Separate identification 4 Triangular matrix 
        symbol = 0
        for i in range(n):
            for j in range(n):
                if f1 and j > i and A[i * n + j] != 0:
                    f1 = False
                if f2 and i > j and A[i * n + j] != 0:
                    f2 = False
                if f3 and i + j < n - 1 and A[i * n + j] != 0:
                    f3 = False
                if f4 and i + j > n - 1 and A[i * n + j] != 0:
                    f4 = False
        if f1 or f2:  #  The main diagonal contains non- 0 Triangular matrix of elements 
            result = 1
            for i in range(n):
result *= A[i * n + i]
   22 |                 symbol = 1
   23 |             return result, symbol
   24 |         elif f3 or f4:  #  The anti-diagonal contains non- 0 Triangular matrix of elements 
   25 |             result = int(math.pow(-1, n * (n - 1) / 2))
   26 |             for i in range(n):
   27 |                 result *= A[i * n + (n - 1 - i)]
   28 |             return result, symbol
   29 |         else:  #  Finding the determinant value using the expansion method 
   30 |             return self.DeterComp(A, n), symbol
   31 | 
   32 |     def DeterComp(self, A, n):
   33 |         mid = 0
   34 |         temp = []
   35 |         for i in range(n * n):
   36 |             temp.append(A[i])
   37 |         if n == 1:
   38 |             result = A[0]
   39 |         else:
   40 |             for i in range(n):
   41 |                 mid += int(math.pow(-1, 2 + i)) * A[i] * self.DeterComp(self.AlgComp(temp, n, i), n - 1)
   42 |             result = mid
   43 |         return result
   44 | 
   45 |     def AlgComp(self, x, n, i):
   46 |         array = []
   47 |         for j in range(n, n * n):
   48 |             if j % n == i:
   49 |                 pass
   50 |             else:
   51 |                 array.append(x[j])
   52 |         return array
   53 | 
                symbol = 1
            return result, symbol
        elif f3 or f4:  #  The anti-diagonal contains non- 0 Triangular matrix of elements 
            result = int(math.pow(-1, n * (n - 1) / 2))
            for i in range(n):
                result *= A[i * n + (n - 1 - i)]
            return result, symbol
        else:  #  Finding the determinant value using the expansion method 
            return self.DeterComp(A, n), symbol

    def DeterComp(self, A, n):
        mid = 0
        temp = []
        for i in range(n * n):
            temp.append(A[i])
        if n == 1:
            result = A[0]
        else:
            for i in range(n):
                mid += int(math.pow(-1, 2 + i)) * A[i] * self.DeterComp(self.AlgComp(temp, n, i), n - 1)
            result = mid
        return result

    def AlgComp(self, x, n, i):
        array = []
        for j in range(n, n * n):
            if j % n == i:
                pass
            else:
                array.append(x[j])
        return array


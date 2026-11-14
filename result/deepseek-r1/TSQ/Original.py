import math


class Trisquare:
    def trisquare(self, argv):
        symbol = 0  #  Check if the test case has passed through the error statement. 
        a = argv[0]
        b = argv[1]
        c = argv[2]
        if a <= 0 or b <= 0 or c <= 0 or a >= b + c or b >= a + c or c >= a + b:
            print('Not a triangle')
            return 0
        Sum = a + b + c
        Max = max(a, b, c)
        Min = min(a, b, c)
        mid = Sum - Max - Min
        if pow(Max, 2) < pow(mid, 2) + pow(Min, 2):
            #  Acute triangle 
            if Max == mid:
                #  Vertex angle less than or equal to 60 Isosceles triangle with an angle of 
                h = math.sqrt(pow(Max, 2) - pow(Min / 2, 2))
                return Min * h / 2, symbol
            elif Min == mid:
                #  Vertex angle greater than 60 Isosceles triangle with an angle of 
                h = math.sqrt(pow(Min, 2) - pow(Max / 2, 2))
                return Max * h / 2, symbol
            else:
                #  scalene acute triangle, calculated using Heron’s formula 
                p = (Max + mid + Min) / 2
                return math.sqrt(p * (p - Max) * (p - mid) * (p - Min)), symbol
        if pow(Max, 2) == pow(mid, 2) + pow(Min, 2):
            #  Right triangle 
            return mid * Min / 2, symbol
        if Min == mid:
            #  Obtuse isosceles triangle 
            h = math.sqrt(pow(Min, 2) - pow(Max / 2, 2))
            return Max * h / 2, symbol
        else:
            #  scalene obtuse triangle, Max Multiply by height divided by 2
            x = (pow(Max, 2) + pow(mid, 2) - pow(Min, 2)) / (2 * Max)
            h = math.sqrt(pow(mid, 2) - pow(x, 2))
            return Max * h / 2, symbol


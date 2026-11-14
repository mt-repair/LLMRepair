from PT2 import *
import copy
import subprocess


class SimpleInput:
    def __init__(self, lines):
        self.lines = lines

def get_count(output):
    count = [0] * 5

    for line in output.splitlines():
        if ',' not in line:
            continue

        if 'identifier' in line or 'keyword' in line:
            count[0] += 1
        if 'string' in line:
            count[1] += 1
        if 'error' in line:
            count[2] += 1
        if 'character' in line:
            count[3] += 1
        if 'numeric' in line:
            count[4] += 1

    return count


#  <g id=”Bold”>Medical Treatment:</g>   Buat   EXE  Executable Files 
def getEXE():
    for v in range(1, 22):
        c_file = f"D:/ anonymous / Covered /MSBF/MSBF_Code/MSBF/PT2/Mutants/UsedMutants/printtokens2_v{v}/print_tokens2.c"
        exe_file = f"D:/ anonymous / Covered /MSBF/MSBF_Code/MSBF/PT2/Mutants/UsedMutants/printtokens2_v{v}/print_tokens2.exe"

        subprocess.run(
            ["gcc", c_file, "-o", exe_file],
            check=True
            )
        print(v)
    return 0





#  The range is 1-21
MutantNumber = 15

original = f"D:/ anonymous / Covered /MSBF/MSBF_Code/MSBF/PT2/Mutants/printtokens2_v0/print_tokens2.exe"
Mutant = f"D:/ anonymous / Covered /MSBF/MSBF_Code/MSBF/PT2/Mutants/UsedMutants/printtokens2_v{MutantNumber}/print_tokens2.exe"

#  Source Test Case 
source_input = [
    SimpleInput(["=> K3dQ   ;hp7"]),
    SimpleInput(['''xor 
;;bWJ00dn9b10m833oe6s6D5Y2S51Wl8VJHX4
''']),
    SimpleInput([''';IF A L  ;tJvMR3
''']),
    SimpleInput([''';`6#l
93 
''']),
    SimpleInput(['''=> W4vLoQv ` 9 ;Bm1
=> W4vLoQv ` 9 ;Bm1
''']),
]

for s in range(0,1):

    print(f"source:", repr(source_input[s].lines[0]))
    MR = [MR1, MR2, MR3, MR4, MR5]

    for i in range(0, 5):


        mr = MR[i]
        follow_input = mr().getExpectedMatrix(source_input[s])

        stestcaseRsOriginal = subprocess.run(
            [original], 
            input=source_input[s].lines[0],
            capture_output=True,
            text=True
        ).stdout.strip()

        stestcaseRsMutant = subprocess.run(
            [Mutant], 
            input=source_input[0].lines[0],
            capture_output=True,
            text=True
        ).stdout.strip()

        ftestcaseRsOriginal = subprocess.run(
            [original], 
            input=follow_input.lines[0],
            capture_output=True,
            text=True
        ).stdout.strip()

        ftestcaseRsMutant = subprocess.run(
            [Mutant], 
            input=follow_input.lines[0],
            capture_output=True,
            text=True
        ).stdout.strip()

        print(f"=======source{s+1}===MR{i+1}==================")
        print(f"follow{i+1} :", repr(follow_input.lines[0]))
        print("-----------------------------------------------------------")
        print(f"stestcaseRsOriginal:{stestcaseRsOriginal}")
        print("-----------------------------------------------------------")
        print(f"ftestcaseRsOriginal:{ftestcaseRsOriginal}")
        print("-----------------------------------------------------------")
        print(f"stestcaseRsMutant:{stestcaseRsMutant}")
        print("-----------------------------------------------------------")
        print(f"ftestcaseRsMutant:{ftestcaseRsMutant}")

        # source_mutant_count = get_count(stestcaseRsOriginal)
        # follow_mutant_count = get_count(ftestcaseRsOriginal)

        source_mutant_count = get_count(stestcaseRsMutant)
        follow_mutant_count = get_count(ftestcaseRsMutant)

        if i in [0, 1, 3, 4]:   # MR1, MR2, MR4, MR5
            mr_satisfied = source_mutant_count == follow_mutant_count

        elif i == 2:             # MR3
            mr_satisfied = all(
                follow_mutant_count[j] <= source_mutant_count[j]
                for j in range(5)
            )
        print(f"🐖mr_satisfied:{mr_satisfied}")





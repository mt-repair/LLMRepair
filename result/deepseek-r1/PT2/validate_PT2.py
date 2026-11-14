import json
from pathlib import Path


MR_LIST = ["MR1", "MR2", "MR3", "MR4", "MR5"]

#  With original  Output.getCount()  II  count[0]~count[4]  Bijection 
COUNT_NAMES = [
    "identifier_or_keyword",
    "string",
    "error",
    "character",
    "numeric",
]


def parse_output_count(output_text):
    """
     Insert the  JSON  Convert a segment of output text in  to the original  Output.getCount()  H.E. Mr. Mirza Kusljugić, Ambassador Extraordinary and Plenipotentiary, Permanent Representative to the United Nations (Chairman of the delegation)  5  Dimension  count。

     original project semantics: 
        count[0] = identifier + keyword
        count[1] = string
        count[2] = error
        count[3] = character
        count[4] = numeric

     Important: 
    1. keyword  And  identifier  Aggregate statistics to  count[0]。
    2.  Only contains commas  ','  Only the output lines of  are included in the statistics. 
    3.  Therefore,  eof.、lparen.、rparen.、quote.、comma.  and the like are not counted. 
    4. "It can not get charcter"  It doesn’t count either. 

     This logic intentionally reproduces the original sentence by sentence.  Output.getCount() , rather than defining it yourself  token  Genres 
    """
    count = [0] * 5

    if output_text is None:
        return count

    lines = str(output_text).splitlines()

    for line in lines:
        if "," in line:
            if "identifier" in line or "keyword" in line:
                count[0] += 1
            if "string" in line:
                count[1] += 1
            if "error" in line:
                count[2] += 1
            if "character" in line:
                count[3] += 1
            if "numeric" in line:
                count[4] += 1

    return count


def validate_pair(source_output, followup_output, mr):
    """
     Verify a pair  source/follow-up  NO NAME SPACE NO KEY VALUE!! 

     Return: 
        0 ->  Confirmed  MR
        1 ->  Violation of  MR

    MR1、MR2、MR4、MR5：
         Use Parent Class  MR.assertViolation()  Semantics: 
        source_count == followup_count  is satisfied, otherwise it is violated. 

    MR3：
         Use  MR3  Rewritten by myself  assertViolation()：
         Any dimension  followup_count[i] > source_count[i]  Violation of; 
         That is, all dimensions are required  followup_count[i] <= source_count[i]。
    """
    source_count = parse_output_count(source_output)
    followup_count = parse_output_count(followup_output)

    if mr in ("MR1", "MR2", "MR4", "MR5"):
        return 0 if source_count == followup_count else 1

    if mr == "MR3":
        for i in range(len(followup_count)):
            if followup_count[i] > source_count[i]:
                return 1
        return 0

    raise ValueError(" Support only  MR1~MR5 Receive, : {}".format(mr))


def validate_json_mrs(json_file, output_type):
    """
     Verify  JSON  II  MR1~MR5。

     no parameters 
        json_file:
            JSON  FilePath 

        output_type:
            "actual_output"   ->  Verify Actual Output 
            "expected_output" ->  Verify Expected Output 

    JSON  Must have exactly  10  records, matched by location: 
        0,1 -> MR1
        2,3 -> MR2
        4,5 -> MR3
        6,7 -> MR4
        8,9 -> MR5

     Return: 
        (boolean, mr_result)

        boolean:
            True  -> MR1~MR5  Fully satisfied 
            False ->  At least one  MR  Violated 

        mr_result:
             length is {0}  5  One-dimensional array of  [MR1, MR2, MR3, MR4, MR5]
            0 =  Confirmed 
            1 =  Violation of 
    """
    if output_type not in ("actual_output", "expected_output"):
        raise ValueError(
            'output_type  can only be  "actual_output"  OR  "expected_output" , currently : {}'.format(
                output_type
            )
        )

    json_path = Path(json_file)

    if not json_path.exists():
        raise FileNotFoundError("JSON  File don/’t exists : {}".format(json_path))

    with json_path.open("r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if not isinstance(test_cases, list):
        raise ValueError("JSON  The root node must be an array /list。")

    if len(test_cases) != 10:
        raise ValueError(
            "MR1~MR5  Total cost  10  Test records, current  JSON  The Communist Party of China has  {}  Piece  ".format(
                len(test_cases)
            )
        )

    mr_result = [0, 0, 0, 0, 0]

    for i in range(5):
        source_index = i * 2
        followup_index = source_index + 1

        source_case = test_cases[source_index]
        followup_case = test_cases[followup_index]

        if not isinstance(source_case, dict) or not isinstance(followup_case, dict):
            raise ValueError(
                " No.  {}、{}  The test record must be  JSON  of research. ".format(
                    source_index + 1, followup_index + 1
                )
            )

        if output_type not in source_case:
            raise KeyError(
                " Test  {}  Missing fields:   {}".format(
                    source_case.get("test_id", source_index), output_type
                )
            )

        if output_type not in followup_case:
            raise KeyError(
                " Test  {}  Missing fields:   {}".format(
                    followup_case.get("test_id", followup_index), output_type
                )
            )

        mr_result[i] = validate_pair(
            source_case[output_type],
            followup_case[output_type],
            MR_LIST[i],
        )

    boolean = all(result == 0 for result in mr_result)
    return boolean, mr_result


def get_count_details(output_text):
    """
     Debugging Aid: Return with Name  5  Dimension count. 
     Not participate  MR  Determination, used only for test results. 
    """
    count = parse_output_count(output_text)
    return dict(zip(COUNT_NAMES, count))


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    json_file = BASE_DIR / "result.json"

    boolean, mr_result = validate_json_mrs(
        str(json_file),
        "actual_output"
    )

    print("boolean =", boolean)
    print("mr_result =", mr_result)
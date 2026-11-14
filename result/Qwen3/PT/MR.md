````
```json
{
  "MR1": {
    "input_transformation": " Round up the randomly selected source test cases 50% Enter a row to swap the case of the English letters in the selected row, while keeping the other characters and the input structure unchanged, to construct a follow-up test case. ",
    "output_relation": " Five Categories in Source Test Case and follow-up test case Outputs token which was . identifier AND: keyword The sum of, string、error、character And numeric ) The quantity should remain unchanged. That is, identifier AND: keyword Total quantity, string Medicine Quantity, error Medicine Quantity, character Total Quantity numeric The quantities are equal. "
  },

  "MR2": {
    "input_transformation": " For semicolons contained in the source test case ';' For input lines that do not contain single or double quotation marks, retain the line from the beginning to the first semicolon. ';' and delete all characters after the semicolon to construct the follow-up test case. ",
    "output_relation": " Since the content after the semicolon is a comment, deleting that part should not affect validity. token statistical results. Therefore, the five categories in the outputs of the source test cases and the follow-up test cases token which was . identifier AND: keyword The sum of, string、error、character And numeric ) should be equal. "
  },

  "MR3": {
    "input_transformation": " Round up the randomly selected source test cases 50% Enter a line and add a semicolon at the beginning of each selected line ';' , convert these input lines into comment lines, and construct follow-up test cases. ",
    "output_relation": " After converting some input lines to comments, no new valid should be generated. token Therefore, each category in the output of the follow-up test cases token The number of  must not exceed the corresponding type in the source test case. token Quantity, counted in the output token in. identifier+keyword The sum of, string、error、character And numeric）。"
  },

  "MR4": {
    "input_transformation": " First, randomly select the rounded-up test cases from the source test cases. 50% Enter a line and switch between uppercase and lowercase English letters; then, for lines containing semicolons, ';' For input lines that do not contain single or double quotation marks, remove all characters after the first semicolon to construct the follow-up test case. ",
    "output_relation": " Changing between uppercase and lowercase letters and deleting comments after semicolons should not change the five categories. token Therefore, the number of test cases in the output of the source test cases and the follow-up test cases identifier AND: keyword Amount string Medicine Quantity, error Medicine Quantity, character Total Quantity numeric The quantities should be equal. "
  },

  "MR5": {
    "input_transformation": " First, for semicolons included in the source test cases, ';' and do not contain single or double quotation marks, delete all characters after the first semicolon; then randomly select the processed rounded-up 50% Enter a line and switch between uppercase and lowercase English letters to construct follow-up test cases. ",
    "output_relation": " The deletion of the comment after the semicolon and the subsequent change between uppercase and lowercase should not change the five categories. token (Quantity. Therefore, the number of test cases in the source test case and the follow-up test case output identifier AND: keyword Amount string Medicine Quantity, error Medicine Quantity, character Total Quantity numeric The quantities should be equal. "
  }
}
```

````


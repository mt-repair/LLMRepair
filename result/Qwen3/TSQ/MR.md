```
  "MR1": {
    "input_transformation": "Given original triangle sides [a, b, c], compute transformed edge: a1 = sqrt(2 * b^2 + 2 * c^2 - a^2), b1 = b, c1 = c. The follow-up input is [a1, b1, c1].",
    "output_relation": "Compare the source output area s and follow-up output area s1. After rounding both values to 4 decimal places, the absolute difference abs(s1 - s) should be less than 1e-4."
  },
  "MR2": {
    "input_transformation": "Given original triangle sides [a, b, c], compute transformed edge: a1 = a, b1 = sqrt(2 * a^2 + 2 * c^2 - b^2), c1 = c. The follow-up input is [a1, b1, c1].",
    "output_relation": "Compare the source output area s and follow-up output area s1. After rounding both values to 4 decimal places, the absolute difference abs(s1 - s) should be less than 1e-4."
  },
  "MR3": {
    "input_transformation": "Given original triangle sides [a, b, c], compute transformed edge: a1 = a, b1 = b, c1 = sqrt(2 * a^2 + 2 * b^2 - c^2). The follow-up input is [a1, b1, c1].",
    "output_relation": "Compare the source output area s and follow-up output area s1. After rounding both values to 4 decimal places, the absolute difference abs(s1 - s) should be less than 1e-4."
  },
  "MR4": {
    "input_transformation": "Given original triangle sides [a, b, c], compute transformed edge: a1 = sqrt(2 * b^2 + 2 * c^2 - a^2), b1 = sqrt(3 * b^2 + 6 * c^2 - 2 * a^2), c1 = c. The follow-up input is [a1, b1, c1].",
    "output_relation": "Compare the source output area s and follow-up output area s1. After rounding both values to 4 decimal places, the absolute difference abs(s1 - s) should be less than 1e-4."
  },
  "MR5": {
    "input_transformation": "Given original triangle sides [a, b, c], compute transformed edge: a1 = sqrt(2 * b^2 + 2 * c^2 - a^2), b1 = b, c1 = sqrt(6 * b^2 + 3 * c^2 - 2 * a^2). The follow-up input is [a1, b1, c1].",
    "output_relation": "Compare the source output area s and follow-up output area s1. After rounding both values to 4 decimal places, the absolute difference abs(s1 - s) should be less than 1e-4."
  
```

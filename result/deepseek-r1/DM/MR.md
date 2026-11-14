```
{
  "MR1": {
    "input_transformation": "The source test case is represented in row-major order as [a1, a2, a3, b1, b2, b3, c1, c2, c3], corresponding to the matrix [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]. Swap the rows with zero-based indices 1 and 2, i.e., swap the second and third rows. The resulting follow-up test case is [a1, a2, a3, c1, c2, c3, b1, b2, b3].",
    "output_relation": "The determinant of the matrix formed by the follow-up test case is the additive inverse of the determinant of the matrix formed by the source test case."
  },
  "MR2": {
    "input_transformation": "The source test case is represented in row-major order as [a1, a2, a3, b1, b2, b3, c1, c2, c3], corresponding to the matrix [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]. Replace the row with zero-based index 1 by itself minus 3 times the row with index 2: R[1] = R[1] − 3*R[2]. Thus [b1, b2, b3] becomes [b1−3*c1, b2−3*c2, b3−3*c3]. The resulting follow-up test case is [a1, a2, a3, b1−3*c1, b2−3*c2, b3−3*c3, c1, c2, c3].",
    "output_relation": "The determinant of the matrix formed by the follow-up test case is equal to the determinant of the matrix formed by the source test case."
  },
  "MR3": {
    "input_transformation": "The source test case is represented in row-major order as [a1, a2, a3, b1, b2, b3, c1, c2, c3], corresponding to the matrix [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]. Transpose the matrix and flatten it again in row-major order. The resulting follow-up test case is [a1, b1, c1, a2, b2, c2, a3, b3, c3].",
    "output_relation": "The determinant of the matrix formed by the follow-up test case is equal to the determinant of the matrix formed by the source test case."
  },
  "MR4": {
    "input_transformation": "The source test case is represented in row-major order as [a1, a2, a3, b1, b2, b3, c1, c2, c3], corresponding to the matrix [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]. If the matrix is invertible, compute its inverse matrix and flatten the inverse matrix in row-major order to construct the follow-up test case.",
    "output_relation": "The determinant of the matrix formed by the follow-up test case is the multiplicative inverse of the determinant of the matrix formed by the source test case."
  },
  "MR5": {
    "input_transformation": "The source test case is represented in row-major order as [a1, a2, a3, b1, b2, b3, c1, c2, c3], corresponding to the matrix [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]. First, swap the rows with zero-based indices 1 and 2 to obtain [[a1, a2, a3], [c1, c2, c3], [b1, b2, b3]]. Then replace the row with index 1 of the transformed matrix by itself minus 3 times the row with index 2. Thus [c1, c2, c3] becomes [c1−3*b1, c2−3*b2, c3−3*b3]. The final follow-up test case is [a1, a2, a3, c1−3*b1, c2−3*b2, c3−3*b3, b1, b2, b3].",
    "output_relation": "The determinant of the matrix formed by the follow-up test case is the additive inverse of the determinant of the matrix formed by the source test case."
  }
}

```


```
Program: Sparse Matrix Multiplication (SMM)
Entry function: MatMul(mat)
Input: A container holding two dense matrices A and B, where the number of columns of A equals the number of rows of B.
Output: Tuple (C, symbol). C is the dense matrix of the product \(A \times B\); symbol is a flag with no practical meaning.
Functionality: Convert dense matrices into the CSR sparse format for matrix multiplication, then convert the sparse computation result back into a dense matrix.
```





```
{
  "MR1": {
    "input_transformation": "Given the input matrices (A, B) of the source test case, transpose the two matrices respectively and then swap their positions in matrix multiplication. Specifically, let A' = B^T and B' = A^T; thus the input of the follow-up test case is (B^T, A^T). In other words, the original first input matrix A is transposed and placed at the second position, and the original second input matrix B is transposed and placed at the first position.",
    "output_relation": "Let the output of the source test case be C = A × B, and the output of the follow-up test case be C' = B^T × A^T. According to the transpose property of matrix products (A × B)^T = B^T × A^T, we have C' = C^T. Therefore, the output matrix of the follow-up test case should equal the transpose of the output matrix of the source test case."
  },
  "MR2": {
    "input_transformation": "First, construct a permutation matrix P derived from the identity matrix by swapping its 1st and 2nd rows. Then left-multiply P with matrix A while keeping B unchanged. Specifically, let A' = P × A and B' = B. Left-multiplying by this permutation matrix is equivalent to swapping the first two rows of A, so this transformation essentially swaps the 1st and 2nd rows of A. The resulting input for the follow-up test case is (P × A, B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = (P × A) × B. By the associative law of matrix multiplication, C' = P × (A × B) = P × C. Therefore, the output of the follow-up test case should equal the source output matrix C left-multiplied by the same permutation matrix P, i.e., the 1st and 2nd rows of the output matrix are swapped accordingly. The expected relation is C' = P × C."
  },
  "MR3": {
    "input_transformation": "First, construct a permutation matrix P whose dimension matches the number of columns of B. P is obtained by swapping the 1st and 2nd rows of the identity matrix. Keep A unchanged and right-multiply B by P. Specifically, let A' = A and B' = B × P. Right-multiplying by this permutation matrix is equivalent to swapping the first two columns of B, so this transformation essentially swaps the 1st and 2nd columns of B. The resulting input for the follow-up test case is (A, B × P).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = A × (B × P). By the associative law of matrix multiplication, C' = (A × B) × P = C × P. Therefore, the output of the follow-up test case should equal the source output matrix C right-multiplied by the same permutation matrix P, i.e., the 1st and 2nd columns of the output matrix are swapped accordingly. The expected relation is C' = C × P."
  },
  "MR4": {
    "input_transformation": "First, construct a diagonal matrix Q where all entries on the main diagonal are 3 and all other entries are 0, i.e., Q = 3I. Then left-multiply Q with matrix A while keeping B unchanged. Specifically, let A' = Q × A and B' = B. Since Q = 3I, Q × A = 3A, so this transformation essentially multiplies every element of A by 3. The resulting input for the follow-up test case is (3A, B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = (3A) × B. By the scalar multiplication property of matrix multiplication, C' = 3 × (A × B) = 3C. Therefore, each entry in the output matrix of the follow-up test case should be three times the corresponding entry in the output matrix of the source test case. The expected relation is C' = 3C."
  },
  "MR5": {
    "input_transformation": "First, construct a diagonal matrix Q where all entries on the main diagonal are 4 and all other entries are 0, i.e., Q = 4I. Keep A unchanged and right-multiply matrix B by Q. Specifically, let A' = A and B' = B × Q. When the dimension of Q matches the number of columns of B, B × Q = 4B, so this transformation essentially multiplies every element of B by 4. The resulting input for the follow-up test case is (A, 4B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = A × (4B). By the scalar multiplication property of matrix multiplication, C' = 4 × (A × B) = 4C. Therefore, each entry in the output matrix of the follow-up test case should be four times the corresponding entry in the output matrix of the source test case. The expected relation is C' = 4C.",
    "transformation_effect": "The source input matrix B is scaled by a factor of 4, so the output matrix of the follow-up test case should also be scaled by 4."
  },
  "MR6": {
    "input_transformation": "Keep matrix B unchanged and directly multiply every element in matrix A by the scalar 6. Specifically, let A' = 6A and B' = B. Unlike MR4, MR6 achieves scaling by element-wise scalar multiplication on A rather than constructing a diagonal matrix for matrix multiplication. The resulting input for the follow-up test case is (6A, B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = (6A) × B. By the scalar multiplication property of matrix multiplication, C' = 6 × (A × B) = 6C. Therefore, each entry in the output matrix of the follow-up test case should be six times the corresponding entry in the output matrix of the source test case. The expected relation is C' = 6C."
  },
  "MR7": {
    "input_transformation": "Keep matrix A unchanged and directly multiply every element in matrix B by the scalar 7. Specifically, let A' = A and B' = 7B. Unlike MR5, MR7 scales B via element-wise scalar multiplication. The resulting input for the follow-up test case is (A, 7B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = A × (7B). By the scalar multiplication property of matrix multiplication, C' = 7 × (A × B) = 7C. Therefore, each entry in the output matrix of the follow-up test case should be seven times the corresponding entry in the output matrix of the source test case. The expected relation is C' = 7C."
  },
  "MR8": {
    "input_transformation": "First, construct an identity matrix I whose dimension equals the number of rows of matrix A. Then add I to matrix A while keeping B unchanged. Specifically, let A' = A + I and B' = B. This operation is equivalent to adding 1 to each main-diagonal entry of A while all off-diagonal entries remain unchanged. The resulting input for the follow-up test case is (A + I, B).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = (A + I) × B. By the distributive law of matrix multiplication over addition, C' = A × B + I × B. Since I is an identity matrix, I × B = B, so C' = C + B. That is, the output of the follow-up test case should be the matrix addition of the source output matrix C and the source input matrix B. The expected relation is C' = C + B. Note that I is a square matrix constructed according to the number of rows of A, so this MR actually requires A to be square. Meanwhile, the dimension requirement for matrix multiplication A × B in the source test case must also be satisfied."
  },
  "MR9": {
    "input_transformation": "First, construct an identity matrix I whose dimension equals the number of rows of matrix B. Keep A unchanged and add I to matrix B. Specifically, let A' = A and B' = B + I. This operation is equivalent to adding 1 to each main-diagonal entry of B while all off-diagonal entries remain unchanged. The resulting input for the follow-up test case is (A, B + I).",
    "output_relation": "Let the output of the source test case be C = A × B. The output of the follow-up test case is C' = A × (B + I). By the distributive law of matrix multiplication over addition, C' = A × B + A × I. Since I is an identity matrix, A × I = A, so C' = C + A. That is, the output of the follow-up test case should be the matrix addition of the source output matrix C and the source input matrix A. The expected relation is C' = C + A."
  }
}

```


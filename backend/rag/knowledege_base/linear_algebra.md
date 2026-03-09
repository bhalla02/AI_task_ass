# Linear Algebra Basics — JEE Level

## 1. Determinant (2x2)

|a  b|
|c  d|

det = ad - bc

---

## 2. Determinant Properties

- If two rows are equal → determinant = 0
- Swapping rows changes sign.
- If one row is multiple of another → determinant = 0

---

## 3. Inverse of 2x2 Matrix

If A = |a  b|
        |c  d|

A^-1 = (1 / (ad - bc)) * | d  -b |
                           | -c  a |

Condition:
det ≠ 0

---

## 4. Solving Linear System

AX = B

If det(A) ≠ 0,
Unique solution exists.

---

## 5. Rank

- Rank = number of linearly independent rows.
- If rank(A) = rank([A|B]) → consistent system.

---

## 6. Common Mistakes

- Forgetting determinant non-zero condition.
- Incorrect minor/cofactor signs.
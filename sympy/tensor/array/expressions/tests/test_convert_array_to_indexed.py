from sympy import Sum, Dummy, sin
from sympy.tensor.array.expressions import ArraySymbol, ArrayTensorProduct, ArrayContraction, PermuteDims, \
    ArrayDiagonal, ArrayAdd, OneArray, ZeroArray, convert_indexed_to_array, ArrayElementwiseApplyFunc
from sympy.tensor.array.expressions.conv_array_to_indexed import convert_array_to_indexed

from sympy.abc import i, j, k, l, m, n, o


def test_convert_array_to_indexed_main():
    A = ArraySymbol("A", (3, 3, 3))
    B = ArraySymbol("B", (3, 3))
    C = ArraySymbol("C", (3, 3))

    d_ = Dummy("d_")

    assert convert_array_to_indexed(A, [i, j, k]) == A[i, j, k]

    expr = ArrayTensorProduct(A, B, C)
    conv = convert_array_to_indexed(expr, [i,j,k,l,m,n,o])
    assert conv == A[i,j,k]*B[l,m]*C[n,o]
    assert convert_indexed_to_array(conv, [i,j,k,l,m,n,o]) == expr

    expr = ArrayContraction(A, (0, 2))
    assert convert_array_to_indexed(expr, [i]).dummy_eq(Sum(A[d_, i, d_], (d_, 0, 2)))

    expr = ArrayDiagonal(A, (0, 2))
    assert convert_array_to_indexed(expr, [i, j]) == A[j, i, j]

    A = ArraySymbol("A", (1, 2, 3))
    expr = PermuteDims(A, [1, 2, 0])
    conv = convert_array_to_indexed(expr, [i, j, k])
    assert conv == A[k, i, j]
    assert convert_indexed_to_array(conv, [i, j, k]) == expr

    expr = ArrayAdd(B, C, PermuteDims(C, [1, 0]))
    conv = convert_array_to_indexed(expr, [i, j])
    assert conv == B[i, j] + C[i, j] + C[j, i]
    assert convert_indexed_to_array(conv, [i, j]) == expr

    expr = ArrayElementwiseApplyFunc(sin, A)
    conv = convert_array_to_indexed(expr, [i, j, k])
    assert conv == sin(A[i, j, k])
    assert convert_indexed_to_array(conv, [i, j, k]).dummy_eq(expr)

    assert convert_array_to_indexed(OneArray(3, 3), [i, j]) == 1
    assert convert_array_to_indexed(ZeroArray(3, 3), [i, j]) == 0
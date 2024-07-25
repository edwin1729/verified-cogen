from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def InArray(a : List[int], x : int) -> bool :
    Requires(Acc(list_pred(a)))
    return Exists(int, lambda d_0_i_:
        (((0) <= (d_0_i_)) and ((d_0_i_) < (len((a))))) and (((a)[d_0_i_]) == (x)))

def partition(a : List[int]) -> int:
    Requires(Acc(list_pred(a)))
    Requires((len((a))) > (0))
    Ensures(Acc(list_pred(a)))
    Ensures(((0) <= (Result())) and ((Result()) < (len((a)))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (Result())), ((a)[d_0_i_]) < ((a)[Result()]))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((Result()) < (d_1_i_)) and ((d_1_i_) < (len((a)))), ((a)[d_1_i_]) >= ((a)[Result()]))))
    Ensures(Forall(int, lambda d_6_x_:
        Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(Old(a), a[d_6_x_])))))
    Ensures(len(a) == len(Old(a)))
    Ensures(Forall(int, lambda d_6_x_:
        Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, Old(a)[d_6_x_])))))
    pivotPos = int(0) # type : int
    pivotPos = (len((a))) - (1)
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    d_3_j_ = int(0) # type : int
    d_3_j_ = 0
    while (d_3_j_) < ((len((a))) - (1)):
        if ((a)[d_3_j_]) < ((a)[pivotPos]):
            rhs0_ = (a)[d_3_j_] # type : int
            a[d_3_j_] = a[d_2_i_]
            a[d_2_i_] = rhs0_
            d_2_i_ = d_2_i_ + 1
        elif ((a)[d_3_j_]) >= ((a)[pivotPos]):
            d_2_i_ = d_2_i_
        d_3_j_ = d_3_j_ + 1
    rhs2_ = (a)[d_2_i_] # type : int
    a[d_2_i_] = a[(len((a))) - (1)]
    (a)[(len((a))) - (1)] = rhs2_
    pivotPos = d_2_i_
    return pivotPos
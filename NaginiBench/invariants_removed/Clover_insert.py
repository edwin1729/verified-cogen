from typing import List, TypeVar, Type, Callable
from nagini_contracts.contracts import *

def insert(line : List[int], l : int, nl : List[int], p : int, at : int) -> None:
    Requires(Acc(list_pred(nl)))
    Requires(Acc(list_pred(line)))
    Requires(((0) <= ((l) + (p))) and (((l) + (p)) <= (len((line)))))
    Requires(((0) <= (p)) and ((p) <= (len((nl)))))
    Requires(((0) <= (at)) and ((at) <= (l)))
    Ensures(Acc(list_pred(nl)))
    Ensures(Acc(list_pred(line)))
    Ensures(Forall(range(0, p), lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (p))) or (((line)[(at) + (d_0_i_)]) == ((nl)[d_0_i_]))))
    Ensures(Forall(range(0, at), lambda d_1_i_:
        not (((0) <= (d_1_i_)) and ((d_1_i_) < (at))) or (((line)[d_1_i_]) == (Old((line)[d_1_i_])))))
    Ensures(Forall(range(at, l), lambda d_2_i_:
        not (((at) <= (d_2_i_)) and ((d_2_i_) < (l))) or (((line)[(d_2_i_) + (p)]) == (Old((line)[d_2_i_])))))
    d_3_i_ = int(0) # type : int
    d_3_i_ = l
    while (d_3_i_) > (at):
        d_3_i_ = (d_3_i_) - (1)
        index0_ = (d_3_i_) + (p) # type : int
        (line)[index0_] = (line)[d_3_i_]
    d_3_i_ = 0
    while (d_3_i_) < (p):
        index1_ = (at) + (d_3_i_) # type : int
        (line)[index1_] = (nl)[d_3_i_]
        d_3_i_ = (d_3_i_) + (1)


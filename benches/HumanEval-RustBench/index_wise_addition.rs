use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn index_wise_addition(a: &Vec<Vec<i32>>, b: &Vec<Vec<i32>>) -> (c: Vec<Vec<i32>>)
    // pre-conditions-start
    requires
        a.len() == b.len(),
        forall|i: int| #![auto] 0 <= i < a.len() ==> a[i].len() == b[i].len(),
        forall|i: int| #![trigger a[i], b[i]]
            0 <= i < a.len()
                ==> forall|j: int| 0 <= j < a[i].len() ==> a[i][j] + b[i][j] <= i32::MAX,
        forall|i: int| #![trigger a[i], b[i]]
            0 <= i < a.len()
                ==> forall|j: int| 0 <= j < a[i].len() ==> a[i][j] + b[i][j] >= i32::MIN,
    // pre-conditions-end
    // post-conditions-start
    ensures
        c.len() == a.len(),
        forall|i: int| #![auto] 0 <= i < c.len() ==> c[i].len() == a[i].len(),
        forall|i: int| #![trigger a[i], b[i], c[i]]
            0 <= i < c.len()
                ==> forall|j: int| #![auto] 0 <= j < c[i].len() ==> c[i][j] == a[i][j] + b[i][j],
    // post-conditions-end
{
    // impl-start
    let mut c: Vec<Vec<i32>> = Vec::new();
    let mut i = 0;
    while i < a.len()
        // invariants-start
        invariant
            0 <= i <= a.len(),
            c.len() == i,
            forall|j: int| #![auto] 0 <= j < i ==> c[j].len() == a[j].len(),
            forall|j: int| #![trigger a[j], b[j], c[j]]
                0 <= j < i
                    ==> forall|k: int| #![auto] 0 <= k < c[j].len() ==> c[j][k] == a[j][k] + b[j][k],
        // invariants-end
    {
        let mut sub_c: Vec<i32> = Vec::new();
        let mut j = 0;
        while j < a[i].len()
            // invariants-start
            invariant
                0 <= j <= a[i as int].len(),
                sub_c.len() == j,
                forall|k: int| #![auto] 0 <= k < j ==> sub_c[k] == a[i as int][k] + b[i as int][k],
            // invariants-end
        {
            sub_c.push(a[i][j] + b[i][j]);
            j = j + 1;
        }
        c.push(sub_c);
        i = i + 1;
    }
    c
    // impl-end
}

fn main() {}
}

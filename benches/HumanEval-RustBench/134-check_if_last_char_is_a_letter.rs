use vstd::prelude::*;

verus! {

pub spec fn is_alphabetic(c: char) -> (result: bool);

#[verifier::external_fn_specification]
#[verifier::when_used_as_spec(is_alphabetic)]
pub fn ex_is_alphabetic(c: char) -> (result: bool)
    ensures
        result <==> (c.is_alphabetic()),
{
    c.is_alphabetic()
}

pub spec fn is_whitespace(c: char) -> (result: bool);

#[verifier::external_fn_specification]
#[verifier::when_used_as_spec(is_whitespace)]
pub fn ex_is_whitespace(c: char) -> (result: bool)
    ensures
        result <==> (c.is_whitespace()),
{
    c.is_whitespace()
}

fn check_if_last_char_is_a_letter(txt: &str) -> (result: bool)
    ensures
        result <==> (txt@.len() > 0 && txt@.last().is_alphabetic() && (txt@.len() == 1
            || txt@.index(txt@.len() - 2).is_whitespace())),
{
    let len = txt.unicode_len();
    if len == 0 {
        return false;
    }
    txt.get_char(len - 1).is_alphabetic() && (len == 1 || txt.get_char(len - 2).is_whitespace())
}

} 
fn main() {}

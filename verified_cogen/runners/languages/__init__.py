from verified_cogen.runners.languages.dafny import DafnyLanguage
from verified_cogen.runners.languages.language import LanguageDatabase
from verified_cogen.runners.languages.nagini import NaginiLanguage


def register_basic_languages():
    LanguageDatabase().register("dafny", ["dfy"], DafnyLanguage())
    LanguageDatabase().register("nagini", ["py", "python"], NaginiLanguage())

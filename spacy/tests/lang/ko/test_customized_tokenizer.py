# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.lang.ko import Korean
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_suffix_regex
from spacy.util import compile_infix_regex


@pytest.fixture
def custom_ko_tokenizer(en_vocab):
    prefix_re = compile_prefix_regex(Korean.Defaults.prefixes)
    suffix_re = compile_suffix_regex(Korean.Defaults.suffixes)
    custom_infixes = [
        r"\.\.\.+",
        r"(?<=[0-9])-(?=[0-9])",
        r"[0-9]+(,[0-9]+)+",
        r"[\[\]!&:,()\*—–\/-]",
    ]
    infix_re = compile_infix_regex(custom_infixes)
    return Tokenizer(
        en_vocab,
        Korean.Defaults.tokenizer_exceptions,
        prefix_re.search,
        suffix_re.search,
        infix_re.finditer,
        token_match=None,
    )


def test_en_customized_tokenizer_handles_infixes(custom_ko_tokenizer):
    sentence = "The 8 and 10-county definitions are not used for the greater Southern California Megaregion."
    context = [word.text for word in custom_ko_tokenizer(sentence)]
    assert context == [
        "The",
        "8",
        "and",
        "10",
        "-",
        "county",
        "definitions",
        "are",
        "not",
        "used",
        "for",
        "the",
        "greater",
        "Southern",
        "California",
        "Megaregion",
        ".",
    ]
    # the trailing '-' may cause Assertion Error
    sentence = "The 8- and 10-county definitions are not used for the greater Southern California Megaregion."
    context = [word.text for word in custom_ko_tokenizer(sentence)]
    assert context == [
        "The",
        "8",
        "-",
        "and",
        "10",
        "-",
        "county",
        "definitions",
        "are",
        "not",
        "used",
        "for",
        "the",
        "greater",
        "Southern",
        "California",
        "Megaregion",
        ".",
    ]

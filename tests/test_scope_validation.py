import sys
sys.path.append("src")
from scope_validator import is_in_scope, get_redirect

def test_pricing_blocked():
    assert not is_in_scope("how much does it cost?")

def test_discount_blocked():
    assert not is_in_scope("can I get a discount?")

def test_normal_question_allowed():
    assert is_in_scope("tell me about your product")

def test_hindi_pricing_blocked():
    assert not is_in_scope("kitna price hai?")

def test_redirect_english():
    msg = get_redirect("en")
    assert "sales" in msg.lower()

def test_redirect_hindi():
    msg = get_redirect("hi")
    assert len(msg) > 0

def test_redirect_odia():
    msg = get_redirect("or")
    assert len(msg) > 0

def test_buy_blocked():
    assert not is_in_scope("I want to buy now")

def test_contract_blocked():
    assert not is_in_scope("what are the contract terms?")

def test_general_query_allowed():
    assert is_in_scope("what industries do you work with?")
# ROBO ADVISOR TEST

from robo_advisor import to_usd

def test_usd():
    result = to_usd(10)
    result1 = to_usd(1000)
    result2 = to_usd(57.3333)
    result3 = to_usd(.011111111)
    assert result == "$ 10.00"
    assert result1 == "$ 1000.00"
    assert result2 == "$ 57.33"
    assert result3 == "$ 0.01"

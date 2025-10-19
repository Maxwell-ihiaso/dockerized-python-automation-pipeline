from app.transformers.public_entries import filter_https, select_fields

def test_filter_https():
    items = [{"HTTPS": True}, {"HTTPS": False}, {"HTTPS": 1}, {}]
    out = filter_https(items)
    assert len(out) == 2

def test_select_fields():
    items = [{"API":"A","X":1}, {"API":"B"}]
    out = select_fields(items, ["API"])
    assert out == [{"API":"A"}, {"API":"B"}]

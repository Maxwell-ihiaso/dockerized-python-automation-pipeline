from app.connectors.public_api import PublicAPIConnector

def test_list_entries_smoke():
    conn = PublicAPIConnector()
    data = conn.list_entries()
    assert data.count >= 0
    assert isinstance(data.entries, list)
    # assert isinstance(data.entries[0], dict)
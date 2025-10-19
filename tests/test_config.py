from ..app.config import settings

def test_settings_load():
    assert settings.API_BASE_URL != ""
    assert settings.API_TIMEOUT_SECS > 0
    assert settings.API_KEY != ""
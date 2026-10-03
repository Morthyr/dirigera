import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import dirigera


@pytest.fixture
def temp_token_file(tmp_path, monkeypatch):
    token_path = tmp_path / "dirigera_token.txt"
    monkeypatch.setattr(dirigera, "TOKEN_FILE", str(token_path))
    return token_path


def test_load_token_reads_cached_token(temp_token_file):
    token = "cached-token"
    temp_token_file.write_text(token, encoding="utf-8")

    assert dirigera.load_token() == token


def test_load_token_returns_none_when_missing(temp_token_file):
    assert dirigera.load_token() is None


def test_save_and_delete_token_round_trip(temp_token_file):
    dirigera.save_token("persisted-token")

    assert temp_token_file.read_text(encoding="utf-8") == "persisted-token"

    dirigera.delete_token()

    assert not temp_token_file.exists()


def test_generate_token_extracts_token(monkeypatch, temp_token_file):
    def fake_run(*args, **kwargs):
        return SimpleNamespace(
            stdout="Your TOKEN:\nabc.def.ghi\n",
            stderr="",
        )

    monkeypatch.setattr(dirigera.subprocess, "run", fake_run)

    assert dirigera.generate_token() == "abc.def.ghi"
    assert temp_token_file.read_text(encoding="utf-8") == "abc.def.ghi"


def test_get_token_uses_cache(monkeypatch):
    monkeypatch.setattr(dirigera, "load_token", lambda: "cached-token")
    monkeypatch.setattr(dirigera, "generate_token", lambda: (_ for _ in ()).throw(AssertionError("should not generate")))

    assert dirigera.get_token() == "cached-token"


def test_get_token_generates_when_missing(monkeypatch):
    monkeypatch.setattr(dirigera, "load_token", lambda: None)
    monkeypatch.setattr(dirigera, "generate_token", lambda: "new-token")

    assert dirigera.get_token() == "new-token"


def test_on_open_sends_initial_payload(capsys):
    ws = Mock()

    dirigera.on_open(ws)

    ws.send.assert_called_once_with("{}")
    assert "Connected to DIRIGERA" in capsys.readouterr().out


def test_on_message_logs_event_and_badoye_alert(capsys):
    payload = {"deviceId": dirigera.BADØYE_ID, "state": "on"}

    dirigera.on_message(None, json.dumps(payload))

    output = capsys.readouterr().out
    assert "EVENT:" in output
    assert ">>> BADØYE EVENT <<<" in output


def test_on_error_logs_error(capsys):
    dirigera.on_error(None, "boom")

    assert "WebSocket error" in capsys.readouterr().out


def test_on_close_logs_status(capsys):
    dirigera.on_close(None, 1000, "normal close")

    output = capsys.readouterr().out
    assert "WebSocket closed" in output
    assert "1000" in output


def test_create_websocket_builds_websocket_app():
    ws = dirigera.create_websocket("token-123")

    assert ws is not None
    assert ws.header == ["Authorization: Bearer token-123"]


def test_connect_returns_false_on_success(monkeypatch):
    class FakeWebSocketApp:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def run_forever(self, sslopt=None):
            return None

    monkeypatch.setattr(dirigera.websocket, "WebSocketApp", FakeWebSocketApp)

    assert dirigera.connect("token-123") is False


def test_connect_returns_true_on_401(monkeypatch):
    class FakeWebSocketApp:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def run_forever(self, sslopt=None):
            raise Exception("401 Unauthorized")

    monkeypatch.setattr(dirigera.websocket, "WebSocketApp", FakeWebSocketApp)

    assert dirigera.connect("token-123") is True


def test_main_reconnects_after_normal_disconnect(monkeypatch):
    monkeypatch.setattr(dirigera, "get_token", lambda: "token-123")
    monkeypatch.setattr(dirigera, "connect", lambda token: False)

    def fake_sleep(seconds):
        raise RuntimeError("stop reconnect loop")

    monkeypatch.setattr(dirigera.time, "sleep", fake_sleep)

    with pytest.raises(RuntimeError, match="stop reconnect loop"):
        dirigera.main()


def test_main_refreshes_token_on_auth_failure(monkeypatch):
    calls = {"connect": 0}

    monkeypatch.setattr(dirigera, "get_token", lambda: "expired-token")
    monkeypatch.setattr(dirigera, "delete_token", lambda: None)
    monkeypatch.setattr(dirigera, "generate_token", lambda: "fresh-token")

    def fake_connect(token):
        calls["connect"] += 1
        if calls["connect"] == 1:
            return True
        return False

    monkeypatch.setattr(dirigera, "connect", fake_connect)

    def fake_sleep(seconds):
        raise RuntimeError("stop after refresh")

    monkeypatch.setattr(dirigera.time, "sleep", fake_sleep)

    with pytest.raises(RuntimeError, match="stop after refresh"):
        dirigera.main()

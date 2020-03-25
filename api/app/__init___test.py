from app.test.fixtures import app, client  # noqa


def test_app_creates(app):  # noqa
    assert app


def test_app_healthy(app, client):  # noqa
    with client:
        resp = client.get("/ping_3f5ca2711e72a507")
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.json == "pong_3f5ca2711e72a507"

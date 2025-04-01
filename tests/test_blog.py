import pytest

from sports_blog.db import get_db


def test_index(client, auth):
    response = client.get("/blog/")  # Updated path to match blog blueprint
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/blog/")  # Updated path
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/blog/1/update"' in response.data  # Updated URL prefix


@pytest.mark.parametrize("path", ("/blog/create", "/blog/1/update", "/blog/1/delete"))  # Updated paths
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/blog/1/update").status_code == 403  # Updated path
    assert client.post("/blog/1/delete").status_code == 403  # Updated path
    # current user doesn't see edit link
    assert b'href="/blog/1/update"' not in client.get("/blog/").data  # Updated path


@pytest.mark.parametrize("path", ("/blog/2/update", "/blog/2/delete"))  # Updated paths
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/blog/create").status_code == 200  # Updated path
    response = client.post(
        "/blog/create", 
        data={"title": "created", "body": "test body", "category_id": "1"}
    )  # Added body content
    
    # Check if we redirected properly - that means post was created
    assert response.headers["Location"] == "/blog/"
    
    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/blog/1/update").status_code == 200  # Updated path
    client.post("/blog/1/update", data={"title": "updated", "body": "", "category_id": "1"})  # Added category_id

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.parametrize("path", ("/blog/create", "/blog/1/update"))  # Updated paths
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": "", "category_id": "1"})  # Added category_id
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/blog/1/delete")  # Updated path
    assert response.headers["Location"] == "/blog/"  # Updated expected redirection

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post is None

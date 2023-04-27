import io
import os
from flaskr import create_app
import pytest
from flaskr.pages import Backend


backend = Backend()

 
# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to team's SPONGEBOB's Project" in resp.data


def page_index(client):
    resp = client.get("/pages")
    assert resp.status_code == 200


def about(client):
    resp = client.get("/about")
    assert resp.status_code == 200

    # check if author images are being displayed
    assert b"Cambrell" in resp.data
    assert b"Samuel" in resp.data
    assert b"Angel" in resp.data


def fetch_images(client):
    resp = client.get("/image/IMG_20210621_161958736_2.jpg")
    assert resp.status_code == 200


def page(client):
    resp = client.get("/pages/Super-Mario-Bros-1985")
    assert resp.status_code == 200


def signup(client):
    resp = client.post("/signup",
                       data={
                           "username": "test_user",
                           "password": "test_password"
                       })
    assert resp.status_code == 302  # Redirect status code


def login(client):
    resp = client.post("/login", data={"username": "sam", "password": "1234"})
    assert resp.status_code == 302  # Redirect status code


def upload_file(client):
    # Log in the user before uploading a file
    client.post("/login", data={"username": "sam", "password": "1234"})

    # Replace the file path with the correct path to your test image
    file_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")

    # Use the file_path variable in the request
    with open(file_path, "rb") as f:
        resp = client.post("/upload", data={"file": f})

    assert resp.status_code == 302  # Redirect status code


def about_page(client):
    # Log in the user before accessing the about page
    client.post("/login", data={"username": "sam", "password": "1234"})
    resp = client.get("/about")
    assert resp.status_code == 200

def test_create_page(client):
    # Log in the user before creating an article
    client.post("/login", data={"username": "sam", "password": "1234"})

    # Create a new article
    title = "Test Article"
    content = "This is a test article."
    author = "sam"
    resp = client.post("/pages/create", data={"title": title, "content": content, "author": author})

    # Check that the article was created
    assert resp.status_code == 302
    assert backend.get_wiki_page(title) == content

    
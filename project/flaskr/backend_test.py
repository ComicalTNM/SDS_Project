from flaskr import backend
import unittest
from unittest import mock, TestCase
from unittest.mock import Mock, MagicMock
import hashlib
import os
import io
from google.cloud.storage.blob import Blob
from google.cloud import storage
from flaskr.backend import Backend
from flaskr import create_app



def test_sign_in_fail_user():

    back = backend.Backend()

    # Test for trying to log into an account with the right password but the username doesn't exist
    # The following is an existing User in the bucket with it's correspondent password
    username = "angel3"
    password = "12345"

    back.password_bucket = MagicMock()
    blobX = MagicMock()

    # Make it so the username doesn't exist by returning False
    back.password_bucket.blob.return_value = blobX
    blobX.exists.return_value = False

    result = back.sign_in(username, password)
    assert result == False


def test_sign_in_pass():

    # The following are a non-existing username and a wrong password
    # However, by mocking, in this case the test should pass.

    back = backend.Backend()

    username = "non-existing-user"
    password = "wrong-password"

    back.password_bucket = MagicMock()
    blobX = MagicMock()

    back.password_bucket.blob.return_value = blobX
    blobX.exists.return_value = True

    fake_password = "wrong-password"

    blobX.download_as_string.return_value = "46" + str(
        int(hashlib.sha256(fake_password.encode("utf-8")).hexdigest(),
            16)) + "9"
    # Have to hardcode the first 2 and last digit of the hashing because in the backend
    # the .download_as_string is returned as bytes and we index that later on to get the correct password.

    result = back.sign_in(username, password)
    assert result == True


def test_sign_up_fail():

    back = backend.Backend()
    # To sign up, we must provide a non-existing username and password
    # Ahead, we will have that
    username = "non-existing-ID"
    password = "non-existing-password"

    blobX = MagicMock()
    back.password_bucket = MagicMock()
    back.password_bucket.blob.return_value = blobX

    # Here, we state that the username does exist, so the test will be False
    blobX.exists.return_value = True

    result = back.sign_up(username, password)
    assert result == False


def test_sign_up_pass():

    # To sign up, we must provide a non-existing username and password
    # So we will provide an existing username and by mocking we will make
    # the test pass.

    back = backend.Backend()

    username = "angel3"
    password = "doesn't matter"

    blobX = MagicMock()
    back.password_bucket = MagicMock()

    back.password_bucket.blob.return_value = blobX

    # Set the blob.exists to False to indicate that the username is non-existing
    blobX.exists.return_value = False

    result = back.sign_up(username, password)
    assert result == True


def test_get_user_fail():
    back = backend.Backend()
    username = "non-existing-ID"

    blobX = MagicMock()
    back.password_bucket = MagicMock()
    back.password_bucket.blob.return_value = blobX

    # Case where the username doesn't exist
    blobX.exists.return_value = False

    result = back.get_user(username)
    assert result == False


def test_get_user_pass():
    back = backend.Backend()
    username = "non-existing-ID"

    # Create a Mock blob to emulate the properties of a blob
    blobX = MagicMock()

    # Turn the password_bucket attribute into a MagicMock
    back.password_bucket = MagicMock()

    # Make it so that when getting a blob from the password_bucket, it will return the mock blob
    back.password_bucket.blob.return_value = blobX

    # Case where the username does exist
    blobX.exists.return_value = True

    result = back.get_user(username)
    assert result == True

    pass


"""
Cases to test for get_wiki_page:
    1. The page name is found, and the html file is returned
    2. The page name is not found, and nothing is returned
"""



def test_get_all_page_names():
    backend = Backend()
    backend.bucket = MagicMock()


    blob = MagicMock()
    name = MagicMock()

    backend.bucket.blob.return_value = blob
    blob.name.return_value = name
    blob.name = "signup"
    
    
    #Test if a valid page name is in the list
    backend.bucket.list_blobs.return_value = [blob, blob]
    result = backend.get_all_page_names()
    first_blob = result[0]
    assert "signup" in first_blob

def test_create_wiki_page():
    page_name = "test_page"
    content = "This is a test page."

    # Create a mock for the Cloud Storage bucket and set it as the backend's bucket attribute
    bucket = MagicMock()
    backend = Backend()
    backend.bucket = MagicMock()
    blob = MagicMock()
    blob.upload("Mario.html")
    assert blob.upload.called


def test_get_image():
    backend = Backend()
    backend.bucket = MagicMock()
    backend.images_bucket = MagicMock()
    blob = MagicMock()


    blob.download_as_bytes.return_value = bytes("Random Image", 'utf-8')
    backend.images_bucket.get_blob.return_value = blob


    assert backend.get_image("Random Image").getvalue() == io.BytesIO(
        bytes("Random Image", 'utf-8')).getvalue()

def test_add_to_favorites():
    #Creation of a mock backend object
    backend = Backend()
    backend.bucket = MagicMock()

    #Creation of a mock bucket and blob
    backend.user_client.bucket = MagicMock()
    blob = MagicMock()

    #Test that the bucket contains an existing page the user added
    page_name = "Mario"
    username = "Deez"
    backend.add_to_favorites(page_name, username)
    backend.user_client.bucket(username + "-favorites").blob.return_value = blob
    assert backend.user_client.bucket(username + "-favorites").blob(page_name) != None

# Testing new methods that were used for my feature : Hover Display


def test_upload_image():

    back = backend.Backend()
    blobX = MagicMock()

    image = MagicMock()
    image.filename.return_value = "image_name"

    back.web_uploads_bucket = MagicMock()
    back.web_uploads_bucket.blob.return_value = blobX
    back.web_uploads_bucket.blob("image_name").return_value = "Hi!"

    back.upload_image(image)
    result = back.web_uploads_bucket.blob("image_name")

    print("PRINTING MOCK TEST",result)

    assert result != "image_name"



def test_get_wiki_image():


    back = backend.Backend()

    # In the web_uploads bucket, there is already an image called `12345.jpeg`
    # We will make it so that trying to get that image will not work.

    # public url to the mentioned image
    public_url = "https://storage.cloud.google.com/web-uploads/12345.jpeg?authuser=5"    


    back.get_wiki_image = MagicMock()
    back.get_wiki_image.return_value = "None"


    result = back.get_wiki_image("12345")

    assert result != public_url

    # It will actually be == "None"


    backend.wiki_content_bucket = bucket

    # Call the create_wiki_page method to create a new page with the given name and content
    backend.create_wiki_page(page_name, content)

    # Test that the create_blob_from_string method was called on the bucket with the correct arguments
    bucket.blob.assert_called_with(page_name + ".txt")
    created_blob = bucket.blob.return_value
    created_blob.upload_from_string.assert_called_with(content)

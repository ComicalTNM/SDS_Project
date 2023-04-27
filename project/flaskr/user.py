from flask_login import UserMixin


class User(UserMixin):
    """
    Simple user class that Inherits the UserMixin from Flask

    This class assists in the usage of Flask_Login that is seen in the frontend,
    specifically in `pages.py`. With this Class, we can keep track of what is the
    current_user logged in, if the user is authenticated and what is their ID. 


    Attributes:
        ID - This is a unique user ID, it is the same as the username.
    """

    def __init__(self, ID):
        self.id = ID

    def get_id(self):
        return self.id

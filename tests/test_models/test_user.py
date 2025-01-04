from models.user import User
import pytest



def test_user_initialization():
    '''Test that User initializes with correct attributes'''
    user = User("testuser", "securepassword")
    assert user.username == "testuser"
    assert user.password == "securepassword"

def test_user_attributes_modification():
    '''Test modification of User attributes'''
    user = User("testuser", "securepassword")
    user.username = "newuser"
    user.password = "newpassword"
    assert user.username == "newuser"
    assert user.password == "newpassword"

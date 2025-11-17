import string
import re
from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(
            User(username, password)
        )

        return user

    def validate(self, username, password, password_confirmation):
        if not username or not password:
            raise UserInputError("Username and password are required")

        # toteuta loput tarkastukset tänne ja nosta virhe virhetilanteissa
        if len(username) < 3:
            raise UserInputError("Username should contain at least three characters")
        
        if password != password_confirmation:
            raise UserInputError("Passwords do not match")

        if len(password) < 8:
            raise UserInputError("Password should contain at least 8 characters")
        
        digits_in_password = re.search('[0-9]', password) != None
        special_chars_in_password = re.search(f'{re.escape(string.punctuation)}', password) != None
        
        if not digits_in_password and not special_chars_in_password:
            raise UserInputError("Password should contain at least one number or special character")


user_service = UserService()

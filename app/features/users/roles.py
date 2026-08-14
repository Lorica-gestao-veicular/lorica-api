# File to define user roles
from enum import Enum


class UserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"

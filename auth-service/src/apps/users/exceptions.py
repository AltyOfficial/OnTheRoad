class UserAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass


class InvalidTokenError(Exception):
    pass

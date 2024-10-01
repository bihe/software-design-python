class UserCacheMissError(Exception):
    """
    UserCacheMissError indicates that the needed value from the cache is not availabe.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BadRequestHashError(Exception):
    """
    BadRequestHashError indicates, that the supplied hash value is not correct.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """
    NotFoundError indicates, that a requested object is not available
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

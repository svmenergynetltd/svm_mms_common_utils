class MMS_Fetch_Error(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class MMS_Fetch_Empty_Response(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

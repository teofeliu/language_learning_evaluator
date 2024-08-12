from fastapi import HTTPException, status

class InvalidFileTypeException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload an audio file.")

class InvalidFileFormatException(HTTPException):
    def __init__(self, detail: str = "Invalid audio file format."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

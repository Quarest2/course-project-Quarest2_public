from fastapi import HTTPException


class FeatureNotFoundException(HTTPException):
    def __init__(self, feature_id: int):
        super().__init__(
            status_code=404, detail=f"Feature with id {feature_id} not found"
        )


class DuplicateVoteException(HTTPException):
    def __init__(self, user_id: int, feature_id: int):
        super().__init__(
            status_code=400,
            detail=f"User {user_id} already voted for feature {feature_id}",
        )


class InvalidVoteValueException(HTTPException):
    def __init__(self, value: int):
        super().__init__(
            status_code=400, detail=f"Vote value must be 1 or -1, got {value}"
        )

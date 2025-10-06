from fastapi import HTTPException
from fastapi.responses import JSONResponse


class FeatureNotFoundException(HTTPException):
    def __init__(self, feature_id: int):
        super().__init__(
            status_code=404,
            detail={
                "code": "feature_not_found",
                "message": f"Feature with id {feature_id} not found",
                "feature_id": feature_id,
            },
        )


class DuplicateVoteException(HTTPException):
    def __init__(self, user_id: int, feature_id: int):
        super().__init__(
            status_code=400,
            detail={
                "code": "duplicate_vote",
                "message": f"User {user_id} already voted for feature {feature_id}",
                "user_id": user_id,
                "feature_id": feature_id,
            },
        )


class InvalidVoteValueException(HTTPException):
    def __init__(self, value: int):
        super().__init__(
            status_code=400,
            detail={
                "code": "invalid_vote_value",
                "message": f"Vote value must be 1 or -1, got {value}",
                "value": value,
            },
        )


def feature_not_found_handler(request, exc: FeatureNotFoundException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


def duplicate_vote_handler(request, exc: DuplicateVoteException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

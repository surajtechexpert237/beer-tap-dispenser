from fastapi import APIRouter, status

from apps.common.response_models import SERVER_STATUS_RESPONSE_MODEL
from apps.common.schemas import ResponseMessage
from core.constants import SERVER_STATUS_RUNNING

router = APIRouter(tags=["server status"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=ResponseMessage, responses=SERVER_STATUS_RESPONSE_MODEL)
def initialization():
    """
    Check server initialization status.

    Returns:

        dict: A JSON object containing a "message" field.
    """
    return {"message": SERVER_STATUS_RUNNING}

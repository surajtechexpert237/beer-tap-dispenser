from fastapi import status

from apps.common.schemas import ResponseMessage

SERVER_STATUS_RESPONSE_MODEL = {
    status.HTTP_200_OK: {"model": ResponseMessage}
}

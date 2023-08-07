from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from core.adapter.db_interface.db_interface import DataInterfaceImpl
from core.constants import SUCCESS_MESSAGE


def add_dispenser(request, response, db_interface: DataInterfaceImpl):
    # Add a new dispenser to the database.
    data, message = None, SUCCESS_MESSAGE
    try:
        request_data = jsonable_encoder(request)
        data = db_interface.create_with_uuid(data=request_data)
        response.status_code = status.HTTP_201_CREATED
    except SQLAlchemyError as err:
        message = str(err)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as err:
        message = str(err)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": message, "data": data}

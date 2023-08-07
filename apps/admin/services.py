from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from adapter.db_interface.db_interface import DataInterfaceImpl
from core.constants import SUCCESS_MESSAGE


def add_dispenser(request, response, db_interface: DataInterfaceImpl):
    """
    Add a new dispenser to the database.
    :param request: The request body containing the flow_volume and price.
    :param response: The response object to handle the HTTP response.
    :param db_interface: The database interface used to interact with the database.

    :return: A dictionary containing the response message and the data, if successful.

    :raises
     - HTTPException, SQLAlchemyError (status_code: 500)
        If any exception occurs while adding the dispenser to the database.
    """
    data, message = None, SUCCESS_MESSAGE
    try:
        request_data = jsonable_encoder(request)
        data = db_interface.create_with_uuid(data=request_data)
        response.status_code = status.HTTP_201_CREATED
    except SQLAlchemyError as err:
        message = str(err)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = str(err)
    return {"message": message, "data": data}

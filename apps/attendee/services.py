from datetime import datetime

from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from apps.dispenser.models import Dispenser, DispenserEntries
from core.adapter.db_interface.db_interface_impl import DBInterface
from core import constants


def open_dispenser_tap(request, response):
    # Initialize database interfaces and default data
    db_dispenser_interface = DBInterface(Dispenser)
    db_dispenser_entries_interface = DBInterface(DispenserEntries)

    data, message = None, constants.DISPENSER_TAP_OPEN
    try:
        # Extract data from the request
        request_data = jsonable_encoder(request)
        dispenser_id = request_data.get('dispenser_id')

        # Check if the dispenser exists
        dispenser_object = db_dispenser_interface.get_single_item_by_filters((Dispenser.id == dispenser_id,))
        if dispenser_object is None:
            return {"message": "Dispenser" + constants.NOT_FOUND.format(dispenser_id), "data": data}
        # Check if the dispenser tap is already open
        if dispenser_object.status:
            return {"message": constants.TAP_ALREADY_OPEN.format(dispenser_object.id), "data": data}

        # Update the dispenser's status to open
        dispenser_res = db_dispenser_interface.update(dispenser_object.id, data={"status": True})

        # Create a new entry with the current open time
        dispenser_entries_object = db_dispenser_entries_interface.create_with_uuid(
            data={"dispenser_id": dispenser_id, "open_time": datetime.utcnow()})
        # Prepare response data
        data = {
            "id": dispenser_entries_object.id,
            'dispenser_id': dispenser_entries_object.dispenser_id,
            'open_time': dispenser_entries_object.open_time,
            'status': dispenser_res.get('status')
        }
        response.status_code = status.HTTP_200_OK
    except SQLAlchemyError as err:
        message = str(err)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as err:
        message = str(err)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": message, "data": data}

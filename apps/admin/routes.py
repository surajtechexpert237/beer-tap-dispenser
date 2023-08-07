from fastapi import APIRouter, Response

from core.adapter.db_interface.db_interface_impl import DBInterface
from .schemas import CreateDispenserSchema, DispenserResponseSchema
from .services import add_dispenser
from ..dispenser.models import Dispenser

router = APIRouter(tags=["Admin"])


@router.post('/dispensers', response_model=DispenserResponseSchema)
def create_dispenser(request: CreateDispenserSchema, response: Response):
    """
    Create a new dispenser with the provided flow_volume.

    Parameters:

        request :
            CreateDispenserSchema :
                The request body containing the flow_volume and price.
        response :
            The response object to handle the HTTP response.

    Returns:

        DispenserResponseSchema :
            The created dispenser data in the response.
    """
    return add_dispenser(request, response, DBInterface(Dispenser))

from fastapi import APIRouter, Response

from apps.attendee.schemas import OpenDispenserTaoSchema, OpenDispenserResponseSchema
from apps.attendee.services import open_dispenser_tap

router = APIRouter(tags=["Attendee"])


@router.post('/open', response_model=OpenDispenserResponseSchema)
def open_dispenser(request: OpenDispenserTaoSchema, response: Response):
    """
    Open the tap of a dispenser and record the entry in the dispenser entries.
    Parameters:

        request :
            OpenDispenserTaoSchema :
                The request body containing the flow_volume and price.
        response :
            The response object to handle the HTTP response.

    Returns:

        OpenDispenserResponseSchema :
            The response containing the dispenser entry data,
    """
    return open_dispenser_tap(request, response)

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.ticket_schema import (
    DeleteTicketResponse,
    TicketCreate,
    TicketResponse,
    TicketUpdate
)
from app.services.ticket_service import ticket_service


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "",
    response_model=None,
    status_code=status.HTTP_200_OK
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db)
):
    ticket = ticket_service.create_ticket(
        db=db,
        ticket_data=ticket_data
    )

    return {
        "status": 201,
        "ticket_id": str(ticket.id)
    }


@router.get(
    "",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    ticket_status: TicketStatus | None = Query(
        default=None,
        alias="status"
    ),
    priority: TicketPriority | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return ticket_service.get_all_tickets(
        db=db,
        ticket_status=ticket_status,
        priority=priority
    )


@router.get(
    "/get_tickets",
    response_model=None,
    status_code=status.HTTP_200_OK
)
def get_tickets(
    ticket_id: str | None = Query(default=None),
    priority: TicketPriority | None = Query(default=None),
    isOpen: bool | None = Query(default=None),
    db: Session = Depends(get_db)
):
    if ticket_id is not None:
        try:
            parsed_ticket_id = UUID(ticket_id)
        except ValueError:
            return {
                "status": 404,
                "message": "Ticket not found",
                "ticket": None
            }

        ticket = ticket_service.get_ticket_by_id(
            db=db,
            ticket_id=parsed_ticket_id
        )

        if ticket is None:
            return {
                "status": 404,
                "message": "Ticket not found",
                "ticket": None
            }

        return {
            "status": 200,
            "ticket": TicketResponse.model_validate(ticket).model_dump()
        }

    ticket_status = None

    if isOpen is not None:
        ticket_status = (
            TicketStatus.OPEN if isOpen else TicketStatus.CLOSED
        )

    tickets = ticket_service.get_all_tickets(
        db=db,
        ticket_status=ticket_status,
        priority=priority
    )

    return {
        "status": 200,
        "tickets": [
            TicketResponse.model_validate(ticket).model_dump()
            for ticket in tickets
        ]
    }


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket_by_id(
    ticket_id: UUID,
    db: Session = Depends(get_db)
):
    ticket = ticket_service.get_ticket_by_id(
        db=db,
        ticket_id=ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return ticket


@router.put(
    "/update",
    response_model=None,
    status_code=status.HTTP_200_OK
)
def update_ticket_legacy(
    ticket_id: UUID = Query(...),
    ticket_data: TicketUpdate = None,
    db: Session = Depends(get_db)
):
    updated_ticket = ticket_service.update_ticket(
        db=db,
        ticket_id=ticket_id,
        ticket_data=ticket_data
    )

    if updated_ticket is None:
        return {
            "status": 404,
            "message": "Ticket not found"
        }

    return {
        "status": 200,
        "ticket": TicketResponse.model_validate(updated_ticket).model_dump()
    }


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = ticket_service.update_ticket(
        db=db,
        ticket_id=ticket_id,
        ticket_data=ticket_data
    )

    if updated_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return updated_ticket


@router.delete(
    "/delete",
    response_model=None,
    status_code=status.HTTP_200_OK
)
def delete_ticket_legacy(
    ticket_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    deleted = ticket_service.delete_ticket(
        db=db,
        ticket_id=ticket_id
    )

    if not deleted:
        return {
            "status": 404,
            "message": "Ticket not found"
        }

    return {
        "status": 200,
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }


@router.delete(
    "/{ticket_id}",
    response_model=DeleteTicketResponse
)
def delete_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = ticket_service.delete_ticket(
        db=db,
        ticket_id=ticket_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return DeleteTicketResponse(
        message="Ticket deleted successfully",
        ticket_id=ticket_id
    )
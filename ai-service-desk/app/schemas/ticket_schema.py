from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        examples=["Login broken"]
    )

    description: str = Field(
        ...,
        max_length=500,
        examples=["Users are unable to log in"]
    )

    email: str = Field(
        ...,
        min_length=3,
        max_length=320,
        examples=["user@example.com"]
    )

    isOpen: bool = Field(
        ...,
        examples=[True]
    )

    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM,
        examples=["high"]
    )


class TicketUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    isOpen: bool | None = None


class TicketResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteTicketResponse(BaseModel):
    message: str
    ticket_id: UUID


class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=10, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str
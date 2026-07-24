from fastapi import APIRouter, Depends, HTTPException, status
import traceback

from app.schemas.ticket_schema import SummarizeRequest, SummarizeResponse
from app.services.bedrock_services import (
    BedrockService,
    BedrockServiceError,
    FakeBedrockService,
)
 
 
router = APIRouter(prefix="/ai", tags=["AI"])

 
@router.post("/summarize", response_model=SummarizeResponse)
def summarize_ticket(
    payload: SummarizeRequest,
    
) -> dict[str, str]:
    try:
        service = BedrockService()
        return service.summarize_ticket(payload.ticket_description)
    except BedrockServiceError as exc:
        traceback.print_exc()
        raise
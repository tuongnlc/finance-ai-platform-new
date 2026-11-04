from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.newspaper_summary import NewspaperSummaryService
from infrastructure.database.session import get_session
from infrastructure.database.repositories.newspaper_summary import PostgresNewspaperSummaryRepository



def get_newspaper_summary_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NewspaperSummaryService:
    newspaper_summary_repository = PostgresNewspaperSummaryRepository(session)
    return NewspaperSummaryService(newspaper_summary_repository)
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.newspaper_topic_tagging import NewspaperTopicTaggingService
from infrastructure.database.session import get_session
from infrastructure.database.repositories.newspaper_topic_tagging import PostgresNewspaperTopicTaggingRepository



def get_newspaper_topic_tagging_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> NewspaperTopicTaggingService:
    newspaper_topic_tagging_repository = PostgresNewspaperTopicTaggingRepository(session)
    return NewspaperTopicTaggingService(newspaper_topic_tagging_repository)

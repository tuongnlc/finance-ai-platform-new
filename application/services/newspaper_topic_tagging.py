from datetime import date
from typing import Optional
from application.domain.repositories.newspaper_topic_tagging import NewspaperTopicTaggingRepository
from application.domain.models.newspaper_topic_tagging import NewspaperTopicTagging


class NewspaperTopicTaggingService:
    def __init__(self, newspaper_topic_tagging_repository: NewspaperTopicTaggingRepository):
        self._newspaper_topic_tagging_repository = newspaper_topic_tagging_repository

    async def create(self, request) -> NewspaperTopicTagging:
        newspaper_topic_tagging = NewspaperTopicTagging(
            newspaper_title=request.newspaper_title,
            newspaper_url=request.newspaper_url,
            newspaper_content=request.newspaper_content,
            publish_date=request.publish_date,
            stocks_mention=request.stocks_mention,
            main_topic=request.main_topic,
            person_mention=request.person_mention,
            newspaper_summary=request.newspaper_summary,
            sentiment_analysis=request.sentiment_analysis,
        )
        return await self._newspaper_topic_tagging_repository.create(newspaper_topic_tagging)

    async def get_by_newspaper_url(self, newspaper_url: str) -> NewspaperTopicTagging:
        return await self._newspaper_topic_tagging_repository.get_by_newspaper_url(newspaper_url)

    async def list(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> list[NewspaperTopicTagging]:
        return await self._newspaper_topic_tagging_repository.list(min_date=min_date, max_date=max_date)

    async def delete_by_newspaper_url(self, newspaper_url: str) -> None:
        return await self._newspaper_topic_tagging_repository.delete_by_newspaper_url(newspaper_url)

    async def update_by_newspaper_url(
        self,
        newspaper_url: str,
    ) -> NewspaperTopicTagging:
        return await self._newspaper_topic_tagging_repository.update_by_newspaper_url(newspaper_url)

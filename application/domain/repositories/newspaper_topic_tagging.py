from typing import Protocol, Optional
from datetime import date
from application.domain.models.newspaper_topic_tagging import NewspaperTopicTagging


class NewspaperTopicTaggingRepository(Protocol):
    async def create(self, tagging: NewspaperTopicTagging) -> NewspaperTopicTagging:
        pass

    async def get_by_newspaper_url(self, newspaper_url: str) -> NewspaperTopicTagging:
        pass

    async def list(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> list[NewspaperTopicTagging]:
        pass

    async def delete_by_newspaper_url(self, newspaper_url: str) -> None:
        pass

    async def update_by_newspaper_url(
        self,
        newspaper_url: str,
        is_favorite: Optional[int] = None,
    ) -> NewspaperTopicTagging:
        pass

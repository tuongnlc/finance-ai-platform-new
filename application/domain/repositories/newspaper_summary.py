from typing import Protocol, Optional
from datetime import date
from application.domain.models.newspaper_summary import NewspaperSummary


class NewspaperSummaryRepository(Protocol):
    async def create(self, summary: NewspaperSummary) -> NewspaperSummary:
        pass

    async def get_by_id(self, summary_id: str) -> NewspaperSummary:
        pass

    async def list(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> list[NewspaperSummary]:
        pass

    async def delete_by_id(self, summary_id: str) -> None:
        pass

    async def update_by_id(
        self,
        summary_id: str,
        is_favorite: Optional[int] = None,
    ) -> NewspaperSummary:
        pass
from datetime import date
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.models.newspaper_topic_tagging import NewspaperTopicTagging
from infrastructure.database.orm_models.newspaper_topic_tagging import NewspaperTopicTaggingORM


class PostgresNewspaperTopicTaggingRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, newspaper_topic_tagging: NewspaperTopicTagging) -> NewspaperTopicTagging:
        newspaper_topic_tagging_orm = self._to_orm(newspaper_topic_tagging)
        self._session.add(newspaper_topic_tagging_orm)
        await self._session.flush()
        await self._session.refresh(newspaper_topic_tagging_orm)
        return self._to_domain(newspaper_topic_tagging_orm)

    async def get_by_newspaper_url(self, newspaper_url: str) -> NewspaperTopicTagging | None:
        result = await self._session.execute(
            select(NewspaperTopicTaggingORM).where(NewspaperTopicTaggingORM.newspaper_url == newspaper_url)
        )
        newspaper_topic_tagging_orm = result.scalar_one_or_none()
        if newspaper_topic_tagging_orm is None:
            return None
        return self._to_domain(newspaper_topic_tagging_orm)

    async def list(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> list[NewspaperTopicTagging]:
        stmt = select(NewspaperTopicTaggingORM)
        if min_date is not None:
            stmt = stmt.where(NewspaperTopicTaggingORM.publish_date >= min_date)
        if max_date is not None:
            stmt = stmt.where(NewspaperTopicTaggingORM.publish_date <= max_date)
        result = await self._session.execute(stmt)
        newspaper_topic_tagging_orms = result.scalars().all()
        return [self._to_domain(newspaper_topic_tagging_orm) for newspaper_topic_tagging_orm in newspaper_topic_tagging_orms]

    async def delete_by_newspaper_url(self, newspaper_url: str) -> None:
        result = await self._session.execute(
            select(NewspaperTopicTaggingORM).where(NewspaperTopicTaggingORM.newspaper_url == newspaper_url)
        )
        newspaper_topic_tagging_orm = result.scalar_one_or_none()
        if newspaper_topic_tagging_orm is None:
            return
        await self._session.delete(newspaper_topic_tagging_orm)
        await self._session.flush()

    async def update_by_newspaper_url(
        self,
        newspaper_url: str,
    ) -> NewspaperTopicTagging:
        result = await self._session.execute(
            select(NewspaperTopicTaggingORM).where(NewspaperTopicTaggingORM.newspaper_url == newspaper_url)
        )
        newspaper_topic_tagging_orm = result.scalar_one_or_none()
        if newspaper_topic_tagging_orm is None:
            raise ValueError(f"NewspaperTopicTagging with newspaper_url {newspaper_url} not found")
        return self._to_domain(newspaper_topic_tagging_orm)

    def _to_orm(self, newspaper_topic_tagging: NewspaperTopicTagging) -> NewspaperTopicTaggingORM:
        return NewspaperTopicTaggingORM(
            newspaper_title=newspaper_topic_tagging.newspaper_title,
            newspaper_url=newspaper_topic_tagging.newspaper_url,
            publish_date=newspaper_topic_tagging.publish_date,
            newspaper_content=newspaper_topic_tagging.newspaper_content,
            stocks_mention=newspaper_topic_tagging.stocks_mention,
            main_topic=newspaper_topic_tagging.main_topic,
            person_mention=newspaper_topic_tagging.person_mention,
            newspaper_summary=newspaper_topic_tagging.newspaper_summary,
            sentiment_analysis=newspaper_topic_tagging.sentiment_analysis,
        )

    def _to_domain(self, newspaper_topic_tagging_orm: NewspaperTopicTaggingORM) -> NewspaperTopicTagging:
        return NewspaperTopicTagging(
            newspaper_title=newspaper_topic_tagging_orm.newspaper_title,
            newspaper_url=newspaper_topic_tagging_orm.newspaper_url,
            publish_date=newspaper_topic_tagging_orm.publish_date,
            newspaper_content=newspaper_topic_tagging_orm.newspaper_content,
            stocks_mention=newspaper_topic_tagging_orm.stocks_mention,
            main_topic=newspaper_topic_tagging_orm.main_topic,
            person_mention=newspaper_topic_tagging_orm.person_mention,
            newspaper_summary=newspaper_topic_tagging_orm.newspaper_summary,
            sentiment_analysis=newspaper_topic_tagging_orm.sentiment_analysis,
        )

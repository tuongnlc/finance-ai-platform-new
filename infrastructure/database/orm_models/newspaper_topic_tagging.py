from datetime import date
from typing import Optional
from sqlalchemy import ARRAY, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.orm_models.base import Base


class NewspaperTopicTaggingORM(Base):
    """
        Saving newspaper topic tagging data in chatbot application
    """
    __tablename__ = 'newspaper_topic_tagging'
    __table_args__ = {"schema": "market_news"}
    newspaper_title: Mapped[str] = mapped_column(Text, nullable=False)
    newspaper_url: Mapped[str] = mapped_column(Text, primary_key=True)
    publish_date: Mapped[date] = mapped_column(Date, nullable=True, index=True)
    newspaper_content: Mapped[str] = mapped_column(Text, nullable=False)
    stocks_mention: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(255)), nullable=True)
    main_topic: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(255)), nullable=True)
    person_mention: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String(255)), nullable=True)
    newspaper_summary: Mapped[str] = mapped_column(Text, nullable=True)
    sentiment_analysis: Mapped[str] = mapped_column(String(255), nullable=True)

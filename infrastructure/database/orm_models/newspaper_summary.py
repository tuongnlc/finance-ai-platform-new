import uuid
from datetime import date
from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.orm_models.base import Base


class NewspaperSummaryORM(Base):
    """
        Saving newspaper summary data in chatbot application
    """
    __tablename__ = 'newspaper_summary'
    __table_args__ = {"schema": "market_news"}
    id: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    document_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    publish_date: Mapped[date] = mapped_column(Date, nullable=True, index=True)
    stocks_mention: Mapped[str] = mapped_column(String(255), nullable=True)
    person_mention: Mapped[str] = mapped_column(String(255), nullable=True)
    newspaper_type: Mapped[str] = mapped_column(String(255), nullable=True)
    newspaper_summary: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_analysis: Mapped[str] = mapped_column(String(255), nullable=True)
    circular_and_policy: Mapped[str] = mapped_column(String(255), nullable=True)
    legal_documents_and_regulations: Mapped[str] = mapped_column(String(255), nullable=True)
    fund_name: Mapped[str] = mapped_column(String(255), nullable=True)
    main_topic: Mapped[str] = mapped_column(String(255), nullable=True)
    is_favorite: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

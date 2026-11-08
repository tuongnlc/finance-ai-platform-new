from datetime import date
from pydantic import BaseModel
from typing import Optional


class CreateNewspaperTopicTaggingRequest(BaseModel):
    newspaper_title: str
    newspaper_url: str
    publish_date: Optional[date] = None
    newspaper_content: str
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None


class CreateNewspaperTopicTaggingResponse(BaseModel):
    newspaper_title: str
    newspaper_url: str
    publish_date: Optional[date] = None
    newspaper_content: str
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None


class GetNewspaperTopicTaggingResponse(BaseModel):
    newspaper_title: str
    newspaper_url: str
    publish_date: Optional[date] = None
    newspaper_content: str
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None


class DeleteNewspaperTopicTaggingResponse(BaseModel):
    newspaper_title: str
    newspaper_url: str
    publish_date: Optional[date] = None
    newspaper_content: str
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None


class UpdateNewspaperTopicTaggingResponse(BaseModel):
    newspaper_title: str
    newspaper_url: str
    publish_date: Optional[date] = None
    newspaper_content: str
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None

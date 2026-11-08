from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class NewspaperTopicTagging:
    newspaper_title: str
    newspaper_url: str
    newspaper_content: str
    publish_date: Optional[date] = None
    stocks_mention: Optional[list[str]] = None
    main_topic: Optional[list[str]] = None
    person_mention: Optional[list[str]] = None
    newspaper_summary: Optional[str] = None
    sentiment_analysis: Optional[str] = None

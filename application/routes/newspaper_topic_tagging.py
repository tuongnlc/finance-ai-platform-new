from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from application.dependencies import (
    get_newspaper_topic_tagging_service,
)

from application.schemas.newspaper_topic_tagging import (
    CreateNewspaperTopicTaggingRequest,
    CreateNewspaperTopicTaggingResponse,
    GetNewspaperTopicTaggingResponse,
    UpdateNewspaperTopicTaggingResponse,
)
from application.services.newspaper_topic_tagging import (
    NewspaperTopicTaggingService,
)

router = APIRouter(prefix="/newspaper-topic-tagging", tags=["NewspaperTopicTagging"])


@router.post("/", status_code=201)
async def create_newspaper_topic_tagging(
        request: CreateNewspaperTopicTaggingRequest,
        newspaper_topic_tagging_service: Annotated[NewspaperTopicTaggingService, Depends(get_newspaper_topic_tagging_service)],
    ) -> CreateNewspaperTopicTaggingResponse:
    newspaper_topic_tagging = await newspaper_topic_tagging_service.create(request)
    return CreateNewspaperTopicTaggingResponse(
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


@router.get("/{newspaper_url:path}", status_code=200)
async def get_newspaper_topic_tagging(
        newspaper_url: str,
        newspaper_topic_tagging_service: Annotated[NewspaperTopicTaggingService, Depends(get_newspaper_topic_tagging_service)],
    ) -> GetNewspaperTopicTaggingResponse:
    newspaper_topic_tagging = await newspaper_topic_tagging_service.get_by_id(newspaper_url)
    return GetNewspaperTopicTaggingResponse(
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

@router.get("/", status_code=200)
async def list_newspaper_topic_taggings(
        newspaper_topic_tagging_service: Annotated[NewspaperTopicTaggingService, Depends(get_newspaper_topic_tagging_service)],
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> list[GetNewspaperTopicTaggingResponse]:
    newspaper_topic_taggings = await newspaper_topic_tagging_service.list(min_date=min_date, max_date=max_date)
    return [
        GetNewspaperTopicTaggingResponse(
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
        for newspaper_topic_tagging in newspaper_topic_taggings
    ]


@router.delete("/{newspaper_url:path}", status_code=204)
async def delete_newspaper_topic_tagging(
        newspaper_url: str,
        newspaper_topic_tagging_service: Annotated[NewspaperTopicTaggingService, Depends(get_newspaper_topic_tagging_service)],
    ) -> None:
    await newspaper_topic_tagging_service.delete_by_id(newspaper_url)

@router.put("/{newspaper_url:path}", status_code=200)
async def update_newspaper_topic_tagging(
        newspaper_url: str,
        newspaper_topic_tagging_service: Annotated[NewspaperTopicTaggingService, Depends(get_newspaper_topic_tagging_service)],
    ) -> UpdateNewspaperTopicTaggingResponse:
    newspaper_topic_tagging = await newspaper_topic_tagging_service.update_by_id(newspaper_url)
    return UpdateNewspaperTopicTaggingResponse(
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

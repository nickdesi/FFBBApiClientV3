from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_datetime,
    from_enum,
    from_int,
    from_list,
    from_none,
    from_obj,
    from_str,
    from_uuid,
)
from .document_flyer_type import DocumentFlyerType
from .facet_stats import FacetStats
from .folder import Folder
from .source import Source


class DocumentFlyer:
    id: UUID | None = None
    storage: str | None = None
    filename_disk: str | None = None
    filename_download: str | None = None
    title: str | None = None
    type: DocumentFlyerType | None = None
    uploaded_on: datetime | None = None
    modified_on: datetime | None = None
    charset: None
    filesize: int | None = None
    width: int | None = None
    height: int | None = None
    duration: None
    embed: None
    description: None
    location: None
    tags: None
    metadata: FacetStats | None = None
    source: Source | None = None
    credits: None
    gradient_color: str | None = None
    md5: str | None = None
    newsbridge_media_id: None
    newsbridge_metadatas: None
    newsbridge_name: None
    newsbridge_recorded_at: None
    focal_point_x: None
    focal_point_y: None
    newsbridge_labels: list[Any] | None = None
    newsbridge_persons: list[Any] | None = None
    folder: Folder | None = None
    uploaded_by: None
    modified_by: None
    newsbridge_mission: None

    def __init__(
        self,
        id: UUID | None = None,
        storage: str | None = None,
        filename_disk: str | None = None,
        filename_download: str | None = None,
        title: str | None = None,
        type: DocumentFlyerType | None = None,
        uploaded_on: datetime | None = None,
        modified_on: datetime | None = None,
        charset: None = None,
        filesize: int | None = None,
        width: int | None = None,
        height: int | None = None,
        duration: None = None,
        embed: None = None,
        description: None = None,
        location: None = None,
        tags: None = None,
        metadata: FacetStats | None = None,
        source: Source | None = None,
        credits: None = None,
        gradient_color: str | None = None,
        md5: str | None = None,
        newsbridge_media_id: None = None,
        newsbridge_metadatas: None = None,
        newsbridge_name: None = None,
        newsbridge_recorded_at: None = None,
        focal_point_x: None = None,
        focal_point_y: None = None,
        newsbridge_labels: list[Any] | None = None,
        newsbridge_persons: list[Any] | None = None,
        folder: Folder | None = None,
        uploaded_by: None = None,
        modified_by: None = None,
        newsbridge_mission: None = None,
    ) -> None:
        self.id = id
        self.storage = storage
        self.filename_disk = filename_disk
        self.filename_download = filename_download
        self.title = title
        self.type = type
        self.uploaded_on = uploaded_on
        self.modified_on = modified_on
        self.charset = charset
        self.filesize = filesize
        self.width = width
        self.height = height
        self.duration = duration
        self.embed = embed
        self.description = description
        self.location = location
        self.tags = tags
        self.metadata = metadata
        self.source = source
        self.credits = credits
        self.gradient_color = gradient_color
        self.md5 = md5
        self.newsbridge_media_id = newsbridge_media_id
        self.newsbridge_metadatas = newsbridge_metadatas
        self.newsbridge_name = newsbridge_name
        self.newsbridge_recorded_at = newsbridge_recorded_at
        self.focal_point_x = focal_point_x
        self.focal_point_y = focal_point_y
        self.newsbridge_labels = newsbridge_labels
        self.newsbridge_persons = newsbridge_persons
        self.folder = folder
        self.uploaded_by = uploaded_by
        self.modified_by = modified_by
        self.newsbridge_mission = newsbridge_mission

    @staticmethod
    def from_dict(obj: Any) -> DocumentFlyer:
        assert isinstance(obj, dict)
        id = from_uuid(obj, "id")
        storage = from_str(obj, "storage")
        filename_disk = from_str(obj, "filename_disk")
        filename_download = from_str(obj, "filename_download")
        title = from_str(obj, "title")
        type = from_enum(DocumentFlyerType, obj, "type")
        uploaded_on = from_datetime(obj, "uploaded_on")
        modified_on = from_datetime(obj, "modified_on")
        charset = from_none(obj.get("charset"))
        filesize = from_int(obj, "filesize")
        width = from_int(obj, "width")
        height = from_int(obj, "height")
        duration = from_none(obj.get("duration"))
        embed = from_none(obj.get("embed"))
        description = from_none(obj.get("description"))
        location = from_none(obj.get("location"))
        tags = from_none(obj.get("tags"))
        metadata = from_obj(FacetStats.from_dict, obj, "metadata")
        source = from_enum(Source, obj, "source")
        credits = from_none(obj.get("credits"))
        gradient_color = from_str(obj, "gradient_color")
        md5 = from_str(obj, "md5")
        newsbridge_media_id = from_none(obj.get("newsbridge_media_id"))
        newsbridge_metadatas = from_none(obj.get("newsbridge_metadatas"))
        newsbridge_name = from_none(obj.get("newsbridge_name"))
        newsbridge_recorded_at = from_none(obj.get("newsbridge_recorded_at"))
        focal_point_x = from_none(obj.get("focal_point_x"))
        focal_point_y = from_none(obj.get("focal_point_y"))
        newsbridge_labels = from_list(lambda x: x, obj, "newsbridge_labels")
        newsbridge_persons = from_list(lambda x: x, obj, "newsbridge_persons")
        folder = from_obj(Folder.from_dict, obj, "folder")
        uploaded_by = from_none(obj.get("uploaded_by"))
        modified_by = from_none(obj.get("modified_by"))
        newsbridge_mission = from_none(obj.get("newsbridge_mission"))
        return DocumentFlyer(
            id,
            storage,
            filename_disk,
            filename_download,
            title,
            type,
            uploaded_on,
            modified_on,
            charset,
            filesize,
            width,
            height,
            duration,
            embed,
            description,
            location,
            tags,
            metadata,
            source,
            credits,
            gradient_color,
            md5,
            newsbridge_media_id,
            newsbridge_metadatas,
            newsbridge_name,
            newsbridge_recorded_at,
            focal_point_x,
            focal_point_y,
            newsbridge_labels,
            newsbridge_persons,
            folder,
            uploaded_by,
            modified_by,
            newsbridge_mission,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = str(self.id)
        if self.storage is not None:
            result["storage"] = self.storage
        if self.filename_disk is not None:
            result["filename_disk"] = self.filename_disk
        if self.filename_download is not None:
            result["filename_download"] = self.filename_download
        if self.title is not None:
            result["title"] = self.title
        if self.type is not None:
            result["type"] = self.type.value
        if self.uploaded_on is not None:
            result["uploaded_on"] = self.uploaded_on.isoformat()
        if self.modified_on is not None:
            result["modified_on"] = self.modified_on.isoformat()
        if self.filesize is not None:
            result["filesize"] = str(self.filesize)
        if self.width is not None:
            result["width"] = self.width
        if self.height is not None:
            result["height"] = self.height
        if self.metadata is not None:
            result["metadata"] = self.metadata.to_dict()
        if self.source is not None:
            result["source"] = self.source.value
        if self.gradient_color is not None:
            result["gradient_color"] = self.gradient_color
        if self.md5 is not None:
            result["md5"] = self.md5
        if self.newsbridge_labels is not None:
            result["newsbridge_labels"] = self.newsbridge_labels
        if self.newsbridge_persons is not None:
            result["newsbridge_persons"] = self.newsbridge_persons
        if self.folder is not None:
            result["folder"] = self.folder.to_dict()
        return result

"""Metadata schema for the Quora replica entity."""

from agenticverse_entities.base.metadata_base import BaseMetadata, Metadata


class QuoraReplicaMetadata(BaseMetadata):
    """Defines the metadata contract used for runtime injections."""

    def get_metadata(self) -> Metadata:  # type: ignore[override]
        return Metadata(
            domain="*.quora.com",
            parameters={
                "port": "integer",
                "section": "string",  # home, spaces, answers, notifications, profile, auth
                "placement": "string",  # feed_primary, sidebar_callouts, auth_card
                "title": "string",
                "description": "string",
                "question": "string",
                "answer": "string",
                "author": "string",
                "topic": "string",
                "stat_one": "string",
                "stat_two": "string",
                "stat_three": "string",
                "badge_text": "string",
                "tags": "array",
                "cta_label": "string",
                "cta_url": "string",
                "featured": "boolean",
                "image_url": "string",
            },
        )

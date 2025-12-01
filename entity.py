"""Agenticverse entity wiring for the Quora replica."""

from agenticverse_entities.base.entity_base import EntityBase

from metadata import QuoraReplicaMetadata
from server import start_server


class QuoraReplicaEntity(EntityBase):
    name = "quora_replica"
    display_name = "Quora Replica"
    description = "Pixel-perfect Quora onboarding + feed replica with injectable content."
    metadata_cls = QuoraReplicaMetadata

    def start(self, port: int = 5000, threaded: bool = False, content_data=None):
        return start_server(port=port, threaded=threaded, content_data=content_data)

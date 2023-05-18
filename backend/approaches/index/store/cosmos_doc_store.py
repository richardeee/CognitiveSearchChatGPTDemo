from typing import Optional
from llama_index.storage.kvstore.mongodb_kvstore import MongoDBKVStore
from approaches.index.store.base.cosmos_kv_doc_store import CosmosKVDocumentStore

class CosmosDocumentStore(CosmosKVDocumentStore):
    """Mongo Document (Node) store.

    A MongoDB store for Document and Node objects.

    Args:
        mongo_kvstore (MongoDBKVStore): MongoDB key-value store
        namespace (str): namespace for the docstore

    """

    def __init__(
        self,
        mongo_kvstore: MongoDBKVStore,
        namespace: Optional[str] = None,
        collection: Optional[str] = None,
        metadata_collection: Optional[str] = None
    ) -> None:
        """Init a MongoDocumentStore."""
        super().__init__(mongo_kvstore, namespace, collection,metadata_collection)

    @classmethod
    def from_uri(
        cls,
        uri: str,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection: Optional[str] = None,
        metadata_collection: Optional[str] = None
    ) -> "CosmosDocumentStore":
        """Load a CosmosDocumentStore from a MongoDB URI."""
        mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
        return cls(mongo_kvstore, namespace, collection,metadata_collection)

    @classmethod
    def from_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection: Optional[str] = None,
        metadata_collection: Optional[str] = None
    ) -> "CosmosDocumentStore":
        """Load a CosmosDocumentStore from a MongoDB host and port."""
        mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
        return cls(mongo_kvstore, namespace, collection, metadata_collection)

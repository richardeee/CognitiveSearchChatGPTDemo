from typing import Optional
from llama_index.storage.kvstore.mongodb_kvstore import MongoDBKVStore
from approaches.index.store.base.cosmos_kv_index_store import CosmosKVIndexStore

class CosmosIndexStore(CosmosKVIndexStore):

    """Mongo Index store.

    Args:
        mongo_kvstore (MongoDBKVStore): MongoDB key-value store
        namespace (str): namespace for the index store

    """

    def __init__(
        self,
        mongo_kvstore: MongoDBKVStore,
        namespace: Optional[str] = None,
        collection: Optional[str] = None,
    ) -> None:
        """Init a MongoIndexStore."""
        super().__init__(mongo_kvstore, namespace=namespace, collection=collection)

    @classmethod
    def from_uri(
        cls,
        uri: str,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection: Optional[str] = None
    ) -> "CosmosIndexStore":
        """Load a MongoIndexStore from a MongoDB URI."""
        mongo_kvstore = MongoDBKVStore.from_uri(uri, db_name)
        return cls(mongo_kvstore, namespace, collection)

    @classmethod
    def from_host_and_port(
        cls,
        host: str,
        port: int,
        db_name: Optional[str] = None,
        namespace: Optional[str] = None,
        collection: Optional[str] = None
    ) -> "CosmosIndexStore":
        """Load a MongoIndexStore from a MongoDB host and port."""
        mongo_kvstore = MongoDBKVStore.from_host_and_port(host, port, db_name)
        return cls(mongo_kvstore, namespace, collection)
    
    def get_indexes(cls):
        return super().get_indexes()
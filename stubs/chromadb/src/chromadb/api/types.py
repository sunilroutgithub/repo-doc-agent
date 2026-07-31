from typing import Any, Dict, Generic, List, TypeVar

T = TypeVar("T")

Documents = List[str]
Embeddings = List[List[float]]
Include = List[str]
Where = Dict[str, Any]
WhereDocument = Dict[str, Any]
QueryResult = Dict[str, Any]
CollectionMetadata = Dict[str, Any]
Loadable = Any


class DataLoader(Generic[T]):
    def __call__(self, uris: List[str]) -> List[T]: ...


class EmbeddingFunction(Generic[T]):
    def __call__(self, input: Documents) -> Embeddings: ...

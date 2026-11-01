from typing import Protocol, BinaryIO


class ObjectStorage(Protocol):
    async def put(
        self, key: str, stream: BinaryIO, content_type: str, size: int
    ) -> str: ...

    async def delete(self, key: str) -> None: ...

    async def create_download_url(self, key: str, expires_seconds: int = 300) -> str: ...

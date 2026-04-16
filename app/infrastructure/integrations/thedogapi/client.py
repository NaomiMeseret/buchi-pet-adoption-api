from collections.abc import Sequence

import httpx


class TheDogApiClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = "https://api.thedogapi.com/v1",
        timeout: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:
        if client is not None:
            self.client = client
            return

        headers: dict[str, str] = {}
        if api_key:
            headers["x-api-key"] = api_key

        self.client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
        )

    def search_images(self, limit: int) -> list[dict]:
        if limit <= 0:
            return []

        try:
            response = self.client.get(
                "/images/search",
                params={
                    "limit": min(limit, 100),
                    "has_breeds": True,
                    "include_breeds": True,
                    "order": "RANDOM",
                },
            )
            response.raise_for_status()
        except httpx.HTTPError:
            return []

        data = response.json()
        if not isinstance(data, Sequence):
            return []

        return [item for item in data if isinstance(item, dict)]

    def close(self) -> None:
        self.client.close()

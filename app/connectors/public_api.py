from typing import List, Optional, Dict, Any
import requests
from pydantic import BaseModel, Field, ConfigDict
from ..config import settings
from ..logger import get_logger
from ..utils.backoff import retry

log = get_logger("public_api")

class PublicEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")  # ignore unknown fields
    API: str
    Description: str
    Auth: str | None = None
    HTTPS: bool
    Cors: str | None = None
    Link: str
    Category: str

class PublicAPIResponse(BaseModel):
    count: int = Field(..., alias="count")
    entries: List[PublicEntry] = Field(..., alias="entries")


class DogAPIResponse(BaseModel):
    message: Dict[str, List[str]]
    status: str


class PublicAPIConnector:
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize a PublicAPIConnector instance.

        :param base_url: The base URL of the public API. If not provided, it will default to the value of the API_BASE_URL setting.
        :param timeout: The timeout in seconds for requests to the public API. If not provided, it will default to the value of the API_TIMEOUT_SECS setting.
        """
        self.base_url = base_url or settings.API_BASE_URL
        self.timeout = timeout or settings.API_TIMEOUT_SECS
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PipelineBot/1.0"})

    @retry((requests.RequestException,), tries=4, base_delay=0.5)
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Perform a GET request to the public API at the given path.

        The request is retried up to 4 times with a base delay of 0.5 seconds
        in case of a transient RequestException. If the server returns an error
        with a status code of 500 or greater, the request is also retried.

        :param path: The path of the API endpoint to query
        :param params: Optional query parameters to include in the request
        :return: The response from the public API
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        if resp.status_code >= 500:
            # trigger retry on transient server errors
            raise requests.RequestException(f"Server error {resp.status_code}")
        return resp

    def list_entries(self, category: Optional[str] = None) -> PublicAPIResponse:
        """
        List public API entries, optionally filtered by category.

        :param category: Optional category to filter by
        :return: A PublicAPIResponse containing the list of entries
        """
        params = {}
        if category:
            params["category"] = category
        # r = self._get("entries", params=params)
        r = self._get("breeds/list/all")

        r.raise_for_status()
        payload = r.json()
        data = PublicAPIResponse.model_validate(payload)
        log.info(f"Fetched {len(data.entries)} entries (count={data.count})")
        return data
    
    
class DogAPIConnector:
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = base_url or settings.API_BASE_URL
        self.timeout = timeout or settings.API_TIMEOUT_SECS
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PipelineBot/1.0"})

    @retry((requests.RequestException,), tries=3, base_delay=0.5)
    def _get(self, path: str) -> requests.Response:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code >= 500:
        # trigger retry on transient server errors
            raise requests.RequestException(f"Server error {resp.status_code}")
        return resp

    def get_breeds(self) -> DogAPIResponse:
        resp = self._get("breeds/list/all")
        resp.raise_for_status()

        data = resp.json()
        return DogAPIResponse(**data)


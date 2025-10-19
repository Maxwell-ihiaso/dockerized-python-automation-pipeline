from __future__ import annotations

from typing import Dict, List, Optional
from pathlib import Path

import requests
import pandas as pd
import typer
from pydantic import BaseModel, ConfigDict

from ..config import settings
from ..logger import get_logger
from ..utils.backoff import retry


# -------------------------
# Models
# -------------------------

class DogBreedsResponse(BaseModel):
    """
    Response from /breeds/list/all
    {
      "message": { "affenpinscher": [], "australian": ["shepherd"], ... },
      "status": "success"
    }
    """
    model_config = ConfigDict(extra="ignore")
    message: Dict[str, List[str]]
    status: str


class DogRandomImageResponse(BaseModel):
    """
    Response from /breeds/image/random
    {
      "message": "https://images.dog.ceo/breeds/terrier-irish/n02093991_293.jpg",
      "status": "success"
    }
    """
    model_config = ConfigDict(extra="ignore")
    message: str
    status: str


class DogImagesByBreedResponse(BaseModel):
    """
    Response from /breed/{breed}/images or /breed/{breed}/{sub}/images
    {
      "message": ["https://images...jpg", "..."],
      "status": "success"
    }
    """
    model_config = ConfigDict(extra="ignore")
    message: List[str]
    status: str


# -------------------------
# Connector
# -------------------------

log = get_logger("dog_api")

class DogAPIConnector:
    """
    Minimal, production-ready connector for https://dog.ceo/api
    """

    def __init__(self, base_url: Optional[str] = None, timeout_secs: Optional[int] = None):
        self.base_url = (base_url or settings.API_BASE_URL or "https://dog.ceo/api").rstrip("/")
        self.timeout = timeout_secs or int(getattr(settings, "API_TIMEOUT_SECS", 15))
        self.session = requests.Session()
        # Keep headers simple; Dog API doesn't need auth
        self.session.headers.update({"User-Agent": "PipelineBot/1.0 (DogAPIConnector)"})

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip("/")}/{path.lstrip('/')}"

    @retry((requests.RequestException,), tries=4, base_delay=0.5)
    def _get(self, path: str) -> requests.Response:
        url = self._url(path)
        resp = self.session.get(url, timeout=self.timeout)
        # retry on intermittent 5xx
        if resp.status_code >= 500:
            raise requests.RequestException(f"Server error {resp.status_code} for {url}")
        resp.raise_for_status()
        return resp

    # ----------- Public API Methods -----------

    def get_breeds(self) -> DogBreedsResponse:
        """
        GET /breeds/list/all
        """
        r = self._get("breeds/list/all")
        payload = r.json()
        data = DogBreedsResponse.model_validate(payload)
        log.info(f"Fetched {len(data.message)} top-level breeds")
        return data

    def get_random_image(self) -> DogRandomImageResponse:
        """
        GET /breeds/image/random
        """
        r = self._get("breeds/image/random")
        data = DogRandomImageResponse.model_validate(r.json())
        log.info("Fetched random image URL")
        return data

    def get_images_by_breed(
        self,
        breed: str,
        sub_breed: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> DogImagesByBreedResponse:
        """
        GET /breed/{breed}/images
        GET /breed/{breed}/{sub}/images
        Optionally slice to 'limit' client-side.
        """
        if sub_breed:
            path = f"breed/{breed}/{sub_breed}/images"
        else:
            path = f"breed/{breed}/images"
        r = self._get(path)
        data = DogImagesByBreedResponse.model_validate(r.json())
        if limit is not None and limit > 0:
            data.message = data.message[:limit]
        log.info(
            f"Fetched {len(data.message)} image URLs for breed='{breed}'"
            + (f", sub='{sub_breed}'" if sub_breed else "")
        )
        return data


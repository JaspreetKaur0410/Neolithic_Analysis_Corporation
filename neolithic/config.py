
from pydantic import BaseModel, Field, field_validator
from typing import List

class AppConfig(BaseModel):
    tickers: List[str] = Field(default_factory=lambda: ["GLD"])
    capital: float = 10000.0
    risk_pct: float = 1.0
    enable_news: bool = True
    fast_mode: bool = False
    macro_tilt: float = 0.10
    out_dir: str = "reports"
    timezone: str = "America/Detroit"

    @field_validator("tickers")
    @classmethod
    def _upper(cls, v: List[str]) -> List[str]:
        return [t.strip().upper() for t in v if t.strip()]

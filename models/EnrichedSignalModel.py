from pydantic import BaseModel, Field, HttpUrl, validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MacroSentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class Recommendation(str, Enum):
    STRENGTHEN = "strengthen"
    WEAKEN = "weaken"
    NEUTRAL = "neutral"


class MarketPhase(str, Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"


class TimeSensitivity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EnrichedSignalModel(BaseModel):
    """
    Model representing enriched trading signals with additional market intelligence.
    
    This model captures research insights that enhance original trading signals,
    providing additional context and potentially modifying the signal strength.
    """
    schema_version: str = Field(..., description="Version of the schema.")
    signal_id: str = Field(..., description="Unique identifier for the original trade signal.")
    enriched_by: str = Field(..., description="Identifier for the Research Bot enriching the signal.")
    timestamp: datetime = Field(..., description="Timestamp when the signal was enriched (ISO 8601).")
    macro_sentiment: MacroSentiment = Field(..., description="Sentiment analysis of macroeconomic factors.")
    earnings_surprise: Optional[float] = Field(None, description="Earnings surprise percentage affecting the trade decision.")
    news_score: Optional[float] = Field(None, ge=-1, le=1, description="Sentiment score derived from news analysis, between -1 and 1.")
    recommendation: Recommendation = Field(
        ..., 
        description="Indicates if the enrichment strengthens, weakens, or has neutral impact on the original signal."
    )
    sources: Optional[List[HttpUrl]] = Field(default_factory=list, description="Source URLs for the data used in enrichment.")
    market_phase: Optional[MarketPhase] = Field(None, description="Current market phase providing additional context.")
    risk_flag: Optional[bool] = Field(None, description="Whether this enrichment increases the risk level of executing the trade.")
    confidence_adjustment: Optional[float] = Field(
        None, 
        ge=-1, 
        le=1, 
        description="Suggested adjustment to the original signal's confidence level. Positive values increase confidence, negative decrease."
    )
    time_sensitivity: Optional[TimeSensitivity] = Field(None, description="Urgency of the enrichment information (LOW, MEDIUM, HIGH).")
    sector_impact: Optional[str] = Field(None, description="Specific sector affected by this enrichment, if applicable.")
    correlation_id: Optional[str] = Field(None, description="Identifier for grouping related enrichments together.")
    priority: Optional[int] = Field(None, ge=1, le=10, description="Priority of this enrichment (1-10, with 10 being highest).")
    expiration: Optional[datetime] = Field(None, description="Timestamp when this enrichment is no longer valid.")
    extra_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional custom data for future extensions.")

    @validator('sources')
    def validate_sources(cls, v: List[HttpUrl]) -> List[HttpUrl]:
        if v:
            if len(v) > 20:
                raise ValueError("Too many sources provided (max 20)")
            if len(v) == 0:
                raise ValueError("Sources list cannot be empty when provided")
        return v

    @model_validator(mode="after")
    def validate_timestamps(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = values.get('timestamp')
        expiration = values.get('expiration')

        if timestamp and expiration and expiration <= timestamp:
            raise ValueError("Expiration timestamp must be after enrichment timestamp")

        return values

    class Config:
        frozen = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        schema_extra = {
            "example": {
                "schema_version": "1.0",
                "signal_id": "sig_12345",
                "enriched_by": "research_bot_1",
                "timestamp": "2023-04-25T14:35:00Z",
                "macro_sentiment": "positive",
                "news_score": 0.75,
                "recommendation": "strengthen",
                "market_phase": "bull",
                "risk_flag": False,
                "confidence_adjustment": 0.15,
                "time_sensitivity": "medium",
                "priority": 8,
                "expiration": "2023-04-30T14:35:00Z"
            }
        }

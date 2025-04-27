from models.EnrichedSignalModel import EnrichedSignalModel, MacroSentiment, Recommendation, MarketPhase, TimeSensitivity
from datetime import datetime
from pydantic import ValidationError

def test_enriched_signal_model_creation():
    try:
        signal = EnrichedSignalModel(
            schema_version="1.0",
            signal_id="sig_12345",
            enriched_by="research_bot_1",
            timestamp=datetime.utcnow(),
            macro_sentiment=MacroSentiment.POSITIVE,
            recommendation=Recommendation.STRENGTHEN,
            news_score=0.8,
            market_phase=MarketPhase.BULL,
            confidence_adjustment=0.1,
            time_sensitivity=TimeSensitivity.MEDIUM,
            priority=5
        )
        print("✅ Model created successfully:", signal)
    except ValidationError as e:
        print("❌ Validation failed:", e)

if __name__ == "__main__":
    test_enriched_signal_model_creation()

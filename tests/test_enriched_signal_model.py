from models.TradeSignalModel import TradeSignalModel, TradeAction, SignalType, TimeFrame
from datetime import datetime, timedelta
from pydantic import ValidationError


def test_trade_signal_model_creation():
    try:
        signal = TradeSignalModel(
            schema_version="1.0",
            bot_id="analyst_bot_1",
            signal_id="sig_98765",
            timestamp=datetime.now(),
            action=TradeAction.BUY,
            confidence=0.92,
            asset="AAPL",
            market="NASDAQ",
            target_price=155.00,
            stop_loss=150.00,
            signal_type=SignalType.ENTRY,
            notes="Breakout signal above resistance.",
            tags=["breakout", "high-confidence"],
            priority=8,
            risk_score=3.5,
            expected_holding_period=timedelta(days=10),
            analysis_timeframe=TimeFrame.DAILY,
            linked_signals=["sig_12345"],
            source_data={"indicator": "RSI", "value": 70},
            extra_data={"custom_field": "test_value"}
        )
        print("✅ Model created successfully:", signal)
    except ValidationError as e:
        print("❌ Validation failed:", e)


if __name__ == "__main__":
    test_trade_signal_model_creation()
    print("✅ Test function executed successfully")

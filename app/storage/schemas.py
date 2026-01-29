from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from datetime import datetime

from app.storage.db import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String)
    system_state = Column(String)
    input_summary = Column(JSON)
    prediction = Column(String)
    confidence_score = Column(Float)
    fallback_used = Column(Boolean)


class BaselineMetrics(Base):
    __tablename__ = "baseline_metrics"

    baseline_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sample_size = Column(Integer)
    avg_confidence = Column(Float)
    low_confidence_rate = Column(Float)
    feature_ranges = Column(JSON)
    category_frequencies = Column(JSON)
    missing_value_rates = Column(JSON)


class CurrentWindowMetrics(Base):
    __tablename__ = "current_window_metrics"

    id = Column(Integer, primary_key=True)
    window_start = Column(DateTime)
    window_end = Column(DateTime)
    prediction_count = Column(Integer)
    avg_confidence = Column(Float)
    low_confidence_rate = Column(Float)
    feature_anomalies = Column(JSON)
    unseen_categories = Column(Boolean)


class SystemState(Base):
    __tablename__ = "system_state"

    id = Column(Integer, primary_key=True)
    current_state = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(String, primary_key=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    severity = Column(String)
    trigger_signals = Column(JSON)
    decision_reason = Column(String)
    fallback_activated = Column(Boolean)
    resolved = Column(Boolean)


class LLMExplanation(Base):
    __tablename__ = "llm_explanations"

    id = Column(Integer, primary_key=True)
    incident_id = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(String)
    recommendations = Column(String)
    llm_model = Column(String)
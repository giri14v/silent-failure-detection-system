import os
from dotenv import load_dotenv

load_dotenv()

# ---- System Identity ----
SYSTEM_NAME = "silent-failure-detection-system"
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0")

# ---- Database ----
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/system.db")

# ---- Monitoring Windows ----
BASELINE_SAMPLE_SIZE = int(os.getenv("BASELINE_SAMPLE_SIZE", 1000))
CURRENT_WINDOW_MINUTES = int(os.getenv("CURRENT_WINDOW_MINUTES", 15))

# ---- Confidence Thresholds ----
LOW_CONFIDENCE_THRESHOLD = float(os.getenv("LOW_CONFIDENCE_THRESHOLD", 0.6))

# ---- Deviation Thresholds ----
MAX_CONFIDENCE_DROP = float(os.getenv("MAX_CONFIDENCE_DROP", 0.15))  
MAX_LOW_CONFIDENCE_INCREASE = float(os.getenv("MAX_LOW_CONFIDENCE_INCREASE", 0.20))

# ---- Stability Rules ----
WARNING_CONSECUTIVE_RUNS = 2
CRITICAL_CONSECUTIVE_RUNS = 3

# ---- System States ----
STATE_NORMAL = "NORMAL"
STATE_WARNING = "WARNING"
STATE_DEGRADED = "DEGRADED"
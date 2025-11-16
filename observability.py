import logging
from prometheus_client import Counter, Histogram, generate_latest

logger = logging.getLogger("astra")
logging.basicConfig(level=logging.INFO, format="%(message)s")

TOOL_CALLS = Counter("astra_tool_calls_total", "Total tool calls", ["tool"])
ORCH_DURATION = Histogram("astra_orch_duration_seconds", "Orchestrator run duration")

def record_tool_call(tool_name: str):
    TOOL_CALLS.labels(tool=tool_name).inc()
    logger.info(f"metric:tool_call {tool_name}")

def record_orch_duration(seconds: float):
    ORCH_DURATION.observe(seconds)
    logger.info(f"metric:orchestrator_duration {seconds}")

def metrics_text():
    return generate_latest()

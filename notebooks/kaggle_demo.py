from astra.core import make_demo_environment, Orchestrator
from astra.server import jobs
import time

mem, tools, agents = make_demo_environment()
orch = Orchestrator(agents)

print("Running Orchestrator...")
res = orch.run({"task": "kaggle_demo"})
print("Results:", res)

print("Memory device_status entries:", mem.query_recent("device_status"))

job = jobs.start_job("demo-job", lambda i: mem.write("job_tick", {"tick": i}))
time.sleep(1.5)

print("Job status:", jobs.status("demo-job"))
jobs.pause("demo-job")
print("Paused. Job status:", jobs.status("demo-job"))
jobs.resume("demo-job")
print("Resumed. Job status:", jobs.status("demo-job"))

print("Context compaction sample:", mem.compact_context(5))

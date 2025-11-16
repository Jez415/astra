from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from .core import make_demo_environment, Orchestrator, JobRegistry
from .observability import metrics_text
import uuid

app = FastAPI()
mem, tools, agents = make_demo_environment()
orch = Orchestrator(agents)
jobs = JobRegistry()

@app.get("/run_demo")
def run_demo():
    res = orch.run({"task": "demo"})
    return res

@app.get("/metrics")
def metrics():
    return PlainTextResponse(metrics_text(), media_type="text/plain; charset=utf-8")

@app.post("/job/start")
def job_start():
    job_id = str(uuid.uuid4())
    def target(i, *args, **kwargs):
        mem.write("job_tick", {"job_id": job_id, "tick": i})
    jobs.start_job(job_id, target)
    return {"job_id": job_id}

@app.post("/job/{job_id}/pause")
def job_pause(job_id: str):
    jobs.pause(job_id)
    return {"status": "paused"}

@app.post("/job/{job_id}/resume")
def job_resume(job_id: str):
    jobs.resume(job_id)
    return {"status": "resumed"}

@app.get("/job/{job_id}/status")
def job_status(job_id: str):
    return jobs.status(job_id)

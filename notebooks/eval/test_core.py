import time
from astra.core import make_demo_environment, Orchestrator, JobRegistry

def test_orchestrator_basic():
    mem, tools, agents = make_demo_environment()
    orch = Orchestrator(agents)
    res = orch.run({"task": "test"})
    assert "data_agent" in res and "action_agent" in res

def test_memory_persistence():
    mem, tools, agents = make_demo_environment()
    id_ = mem.write("test_kind", {"a":1})
    items = mem.query_recent("test_kind")
    assert len(items) >= 1

def test_job_pause_resume():
    jobs = JobRegistry()
    called = []
    def target(i):
        called.append(i)
    jid = jobs.start_job("t1", target)
    time.sleep(0.2)
    jobs.pause("t1")
    s = jobs.status("t1")
    assert s is not None
    jobs.resume("t1")
    time.sleep(0.2)
    jobs.stop("t1")

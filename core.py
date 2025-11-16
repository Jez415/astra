import time
import threading
import argparse
from typing import List, Dict

from .memory import MemoryBank
from .tools import ToolRegistry, mock_device_tool, http_tool_stub
from .agents import DataAgent, ActionAgent
from .observability import record_orch_duration

class Orchestrator:
    def __init__(self, agents: List):
        self.agents = agents

    def run(self, goal: Dict) -> Dict:
        context = {"goal": goal}
        start = time.time()
        results = {}
        threads = []

        def run_agent(a):
            results[a.name] = a.act(context)

        for a in self.agents:
            t = threading.Thread(target=run_agent, args=(a,))
            t.start(); threads.append(t)
        for t in threads:
            t.join()

        duration = time.time() - start
        record_orch_duration(duration)
        return results

class JobRegistry:
    def __init__(self):
        self.jobs = {}

    def start_job(self, job_id: str, target, *args, **kwargs):
        stop = threading.Event()
        paused = threading.Event()

        def runner():
            i = 0
            while not stop.is_set() and i < 10:
                if paused.is_set():
                    time.sleep(0.1)
                    continue
                target(i, *args, **kwargs)
                time.sleep(0.5)
                i += 1
            self.jobs[job_id]['done'] = True

        th = threading.Thread(target=runner, daemon=True)
        self.jobs[job_id] = {"thread": th, "stop": stop, "paused": paused, "done": False}
        th.start()
        return job_id

    def pause(self, job_id: str):
        self.jobs[job_id]['paused'].set()

    def resume(self, job_id: str):
        self.jobs[job_id]['paused'].clear()

    def stop(self, job_id: str):
        self.jobs[job_id]['stop'].set()

    def status(self, job_id: str):
        j = self.jobs.get(job_id)
        if not j: return None
        return {"done": j['done'], "paused": bool(j['paused'].is_set())}

def make_demo_environment():
    mem = MemoryBank(":memory:")
    tools = ToolRegistry()
    tools.register("mock_device", mock_device_tool)
    tools.register("http_stub", http_tool_stub)
    da = DataAgent("data_agent", tools, mem)
    aa = ActionAgent("action_agent", tools, mem)
    return mem, tools, [da, aa]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        mem, tools, agents = make_demo_environment()
        orch = Orchestrator(agents)
        print("Running orchestrator demo...")
        res = orch.run({"task": "demo"})
        print("Results:\n", res)
        print("Memory device_status entries:\n", mem.query_recent("device_status"))

from typing import Dict, Any
from .tools import ToolRegistry
from .memory import MemoryBank
from .observability import record_tool_call

class Agent:
    def __init__(self, name: str, tools: ToolRegistry, memory: MemoryBank):
        self.name = name
        self.tools = tools
        self.memory = memory

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class DataAgent(Agent):
    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        record_tool_call("mock_device")
        device = self.tools.call("mock_device", {"cmd": "status"})
        self.memory.write("device_status", device)
        return {"device": device}

class ActionAgent(Agent):
    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        record_tool_call("mock_device")
        msgs = self.tools.call("mock_device", {"cmd": "read_sms"})
        self.memory.write("sms", msgs)
        otps = []
        for m in msgs.get("messages", []):
            if "OTP" in m.get("body", "") or "otp" in m.get("body", ""):
                otps.append(m.get("body"))
        return {"otps": otps}

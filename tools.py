from typing import Dict, Any

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, fn):
        self.tools[name] = fn

    def call(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.tools:
            raise KeyError(f"Tool {name} not found")
        return self.tools[name](payload)

def mock_device_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    cmd = payload.get("cmd")
    if cmd == "status":
        return {"status": "ok", "sim_signal": "full"}
    if cmd == "read_sms":
        return {"messages": [{"from": "+91xxxx", "body": "Your OTP is 123456"}]}
    return {"echo": payload}

def http_tool_stub(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"http_stub": True, "payload": payload}

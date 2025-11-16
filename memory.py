import sqlite3
import json
import time
import uuid
from typing import Dict, Any, List

class MemoryBank:
    def __init__(self, path: str = "memory.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS memory
                       (id TEXT PRIMARY KEY, kind TEXT, data TEXT, ts REAL)"""
        )
        self.conn.commit()

    def write(self, kind: str, data: Dict[str, Any]) -> str:
        id_ = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO memory VALUES (?,?,?,?)", (id_, kind, json.dumps(data), time.time())
        )
        self.conn.commit()
        return id_

    def query_recent(self, kind: str, limit: int = 10) -> List[Dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT data FROM memory WHERE kind=? ORDER BY ts DESC LIMIT ?", (kind, limit)
        )
        return [json.loads(r[0]) for r in cur.fetchall()]

    def compact_context(self, max_items: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT data FROM memory ORDER BY ts DESC LIMIT ?", (max_items,)
        )
        return [json.loads(r[0]) for r in cur.fetchall()]

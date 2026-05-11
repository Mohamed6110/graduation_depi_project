# ── Imports ───────────────────────────────────────────────────────────────────
from langgraph.checkpoint.memory import InMemorySaver

import asyncio
import os
from .prompt import compliance_prompt
from langchain.tools import tool
from langchain.agents import create_agent
from config import *
from tools import *

# ── Format Helper (unchanged logic) ──────────────────────────────────────────
def _fmt(label: str, res) -> str:
    if isinstance(res, Exception):
        return f"[{label}: failed — {res}]"
    if not isinstance(res, list) or not res:
        return f"[{label}: no results]"
    return f"[{label}]\n" + "\n".join(
        f"- {r.get('title','')}: {r.get('content','')[:250]}"
        for r in res
    )


# ── Create Compliance Agent ───────────────────────────────────────────────────
agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt=compliance_prompt,
    checkpointer=InMemorySaver(),
)



import json
import asyncio
import os
from fastmcp import Client
import google.generativeai as genai
from agent_core.schemas import BugReport


# =========================
# Gemini Setup
# =========================

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
gemini = genai.GenerativeModel("gemini-2.5-flash")


# =========================
# Gemini Bug Finder
# =========================

class ReasoningAgent:
    def analyze(self, code: str):
        prompt = f"""
You are an Infineon RDI API bug hunter.

Find ALL bugs.

Return STRICT JSON ONLY:

[
  {{
    "line": 1,
    "summary": "BUG : short dataset-style explanation"
  }}
]

Rules:
- concise
- dataset tone
- no markdown
- no essays

Code:
{code}
"""

        response = gemini.generate_content(prompt)
        text = response.text.replace("```json","").replace("```","").strip()

        try:
            data = json.loads(text)
            return data if isinstance(data, list) else []
        except Exception as e:
            print("[DEBUG] Gemini raw:", text)
            return []


# =========================
# MCP Agent (grounding only)
# =========================

class MCPKnowledgeAgent:
    def __init__(self):
        self.url = "http://127.0.0.1:8003/sse"

    def query(self, text):
        async def _call():
            async with Client(self.url) as client:
                return await client.call_tool("search_documents", {"query": text})

        result = asyncio.run(_call())

        if hasattr(result, "content"):
            return result.content
        return []


# =========================
# Explanation Refiner (short, dataset style)
# =========================

class ExplanationAgent:
    def refine(self, summary, code_line, docs):

        prompt = f"""
Rewrite this bug in EXACT dataset style.

Original:
{summary}

Code line:
{code_line}

Documentation:
{docs}

Rules:
- One or two lines max
- Keep BUG phrasing
- No documentation quotes
- No XML
- No essays

Return ONLY the explanation text.
"""

        return gemini.generate_content(prompt).text.strip()


# =========================
# Orchestrator
# =========================

class AuditorOrchestrator:
    def __init__(self):
        self.reasoner = ReasoningAgent()
        self.mcp = MCPKnowledgeAgent()
        self.explainer = ExplanationAgent()

    def analyze(self, sample_id, code):

        lines = code.split("\n")
        bugs = self.reasoner.analyze(code)

        reports = []

        for bug in bugs:
            line_no = int(bug.get("line", 1))
            idx = max(line_no - 1, 0)

            code_line = lines[idx] if idx < len(lines) else ""

            # MCP grounding using REAL code line
            docs = self.mcp.query(code_line)
            docs_text = " ".join([getattr(d, "text", "") for d in docs])

            explanation = self.explainer.refine(
                bug["summary"],
                code_line,
                docs_text
            )

            reports.append(
                BugReport(
                    id=sample_id,
                    bug_line=line_no,
                    explanation=explanation
                )
            )

        return reports

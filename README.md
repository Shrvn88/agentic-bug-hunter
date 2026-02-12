## 🏆 Hackathon Context

Developed during the **Infineon Technologies Agentic Bug Hunter Track** 

The challenge required building a fully agentic AI system capable of:
- Discovering semantic bugs in RDI test programs
- Validating issues against official documentation via MCP
- Producing concise, structured explanations aligned with provided datasets

This repository contains our implementation of that solution.


---

## 🚀 Key Capabilities

- Finds multiple bugs per code sample  
- Uses Gemini (LLM) for semantic bug discovery  
- Uses MCP (Manual Control Plane) for documentation grounding  
- Produces short, dataset-style explanations  
- Reports exact line numbers of bugs  
- Matches the provided sample output format  
- Easily extensible to new APIs and manuals  

---

## 🧠 High-Level Architecture

samples.csv (ID + Code)
↓
Gemini Reasoning Agent
↓
Bug Hypotheses (line + summary)
↓
MCP Server (manual/document search)
↓
Grounded Refinement
↓
final_report.csv (ID, bug_line, Explanation)


---

## 🧩 Agent Roles

### 1. Reasoning Agent (Gemini)

- Reads raw C++ RDI test code  
- Detects all possible bugs  
- Produces short, dataset-style summaries  
- Identifies the exact line number of each bug  

---

### 2. MCP Knowledge Agent

- Queries MCP using the actual code line  
- Retrieves relevant documentation snippets  
- Acts as the authoritative grounding source  

---

### 3. Explanation Refinement Agent

- Combines:
  - Gemini bug summary  
  - Code line context  
  - MCP documentation  
- Produces concise explanations  
- Avoids essays, XML, or hallucinated structure  

---

### 4. Orchestrator

- Coordinates all agents  
- Ensures multiple bugs per sample  
- Returns structured results for CSV export  

---

## 📂 Project Structure

Agentic_Bug_Hunter/
│
├── agent_core/
│ ├── auditor.py # Core agentic logic (LLM + MCP)
│ ├── schemas.py # Pydantic data models
│
├── server/
│ └── mcp_server.py # MCP server (manual/document retrieval)
│
├── data/
│ ├── samples.csv # Input dataset
│ └── final_report.csv # Generated output
│
├── main.py # Entry point
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

Linux / Mac:

```bash
python -m venv .venv
source .venv/bin/activate

nput Format (samples.csv)
ID,Code
16,"rdi.smartVec().label().copyLabel()..."
32,"rdi.port(""pt1"").dc().pin(""dig2"")..."

📊 Output Format (final_report.csv)
ID,bug_line,Explanation
16,1,Use only the VTT mode for editing vectors when rdi.smartVec().label().copyLabel() is used for the label
32,2,BUG : Port name & pin config mismatch instead of execute it will burst twice
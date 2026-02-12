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
                  
           final_report.csv 
      (ID, bug_line, Explanation)


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

<img width="749" height="455" alt="image" src="https://github.com/user-attachments/assets/c86fb744-bd08-404b-bfa4-d9c48f7d0fc9" />



### 📂 Input Format (samples.csv)

<img width="1230" height="277" alt="image" src="https://github.com/user-attachments/assets/b7a7b77d-d339-4153-be02-811b632d1feb" />

---

### 📊 Output Format (final_report.csv)

<img width="1664" height="357" alt="image" src="https://github.com/user-attachments/assets/2d798420-ff23-43c7-8193-9e6dc1fe21d7" />

---

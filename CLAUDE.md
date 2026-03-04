# CLAUDE.md — DocGen Codebase Guide

## Overview

DocGen is a collection of Python applications that use LLMs (via LangChain/LangGraph) to generate and review technical architecture documentation. Each sub-directory is a standalone app. **All apps must be run from the repository root.**

---

## Repository Structure

```
DocGen/
├── OpenDocGen/             # Section-by-section doc generator from markdown outline
├── DocGenReflect/          # Reflection-based doc generator (generate → review → refine)
├── DocGenTeam/             # Multi-agent team doc generator (coordinator → architect → reviewer → editor → publisher)
├── UI/                     # Streamlit UI wrapping the OpenDocGen workflow
├── SimpleAgent/            # Interactive web-search agent (DuckDuckGo)
├── Simple Document Reviewer/  # Multi-perspective doc reviewer for PDF/DOCX (file-based prompts)
├── DocumentReviewer/       # Advanced LangGraph-based doc reviewer with 5 specialist agents
├── GeneratedDocs/          # Output directory for all generated markdown files
├── requirements.txt        # Root-level dependencies (install before running any app)
├── .env_example            # Template for required API keys
└── generated_document.md   # UI download output
```

---

## Setup

1. **Install dependencies** (from repo root):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the repo root by copying `.env_example`:
   ```
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key   # optional
   TAVILY_API_KEY=your_tavily_key         # optional, for Tavily search
   GROQ_API_KEY=your_groq_key             # optional
   ```

3. All apps use `python-dotenv` and load `.env` automatically on startup.

---

## Applications

### 1. OpenDocGen (`OpenDocGen/OpenDocGen.py`)

Reads `OpenDocGen/sections.md`, splits it on `##` headers, and sends each section to an OpenAI LLM with the section content as the instruction. Output saved to `GeneratedDocs/updated_documentation.md`.

```bash
python OpenDocGen/OpenDocGen.py
```

**Key file:** `OpenDocGen/sections.md` — edit this to change the document structure and prompts.
**Model:** `gpt-4` (hardcoded in `OpenDocGen.py`).

---

### 2. DocGenReflect (`DocGenReflect/DocGenReflect.py`)

Three-step reflection loop:
1. **Generate** — Initial document draft
2. **Reflect** — Critique and recommendations by a reviewer persona
3. **Refine** — Updated document incorporating feedback

```bash
python DocGenReflect/DocGenReflect.py
```

**Outputs:** `GeneratedDocs/OriginalDoc.md`, `GeneratedDocs/ReflectionDoc.md`, `GeneratedDocs/finaldoc.md`
**LLM support:** Multiple providers are commented in at the top of the file — uncomment to switch:
- `ChatOpenAI` (default, `gpt-4o`)
- `ChatOllama` (local models: `llama3.2`, `deepseek-r1:14b`)
- `ChatAnthropic`
- `ChatGroq`

The `generatePrompt` targets a specific component standard format (L1/L2/L3 table, interfaces, use cases, security). The `reflectPrompt` enforces architectural principles including separation of concerns and the fictional company name `PenCo`.

---

### 3. DocGenTeam (`DocGenTeam/DocGenTeam.py`)

Sequential multi-agent pipeline using shared `ConversationBufferMemory`:

| Agent | Function |
|---|---|
| `coordinator_agent` | Orchestrates the full pipeline |
| `architect_agent` | Generates initial architecture document |
| `reviewer_agent` | Reviews for accuracy, security, best practices |
| `editor_agent` | Refines based on review feedback |
| `publisher_agent` | Formats for publishing |

```bash
python DocGenTeam/DocGenTeam.py
```

**Output:** `GeneratedDocs/AgentTeamDoc.md`
**Model:** `gpt-4o` (hardcoded). Edit `project_info` in `__main__` to change the subject.

---

### 4. Streamlit UI (`UI/UIOpenDocGen.py`)

Split-screen Streamlit app for interactive document generation with inline editing.

```bash
streamlit run UI/UIOpenDocGen.py
```

Opens at `http://localhost:8501`. Left panel: context guidelines + markdown outline. Right panel: generated content with per-section edit mode toggle and improvement suggestions. Download button exports to `generated_document.md`.

**Must be run from repo root** — imports `DocGenTools` from the `UI/` directory using a relative import assumption.

---

### 5. SimpleAgent (`SimpleAgent/simpleAgent.py`)

Interactive CLI agent with DuckDuckGo web search and conversation memory.

```bash
python SimpleAgent/simpleAgent.py
```

**Model:** `gpt-4-turbo-preview`. Type `quit`/`exit`/`q` to exit.

---

### 6. Simple Document Reviewer (`Simple Document Reviewer/`)

Reviews PDF/DOC/DOCX files using multiple agent perspectives loaded from text prompt files.

```bash
# Run from repo root
python "Simple Document Reviewer/main.py" path/to/document.pdf
```

**Configuration:** Set `LLM_PROVIDER=openai` or `LLM_PROVIDER=anthropic` in `.env`.
**Agent prompts:** Add `.txt` files to `Simple Document Reviewer/agent_prompts/` to add reviewer perspectives. Each file should include a `{document}` placeholder. The special file `consolidate_prompt.txt` consolidates all reviews.
**Outputs:** Prints per-perspective reviews and a consolidated improvement summary to stdout.

---

### 7. DocumentReviewer (`DocumentReviewer/`)

More advanced LangGraph-based document reviewer with five specialist architect agents running sequentially. Accepts PDF or DOCX files via CLI and outputs a JSON report.

```bash
# Run from DocumentReviewer/ directory OR use full path
python DocumentReviewer/src/main.py path/to/document.pdf
python DocumentReviewer/src/main.py path/to/document.pdf -o custom_report.json
```

**Agent pipeline (sequential via LangGraph `StateGraph`):**

| Agent | Class | Focus |
|---|---|---|
| Enterprise Architect | `EnterpriseArchitect` | Business alignment, TOGAF |
| Solution Architect | `SolutionArchitect` | System design, patterns |
| Infrastructure Architect | `InfrastructureArchitect` | Infrastructure, scalability |
| Security Architect | `SecurityArchitect` | Security posture, risks |
| AWS Cloud Architect | `AWSCloudArchitect` | Cloud-specific concerns |

Each agent extends `BaseArchitectAgent` (in `DocumentReviewer/src/agents/base_agent.py`), which uses `ChatOpenAI` with env-configurable parameters:
- `OPENAI_MODEL` (default: `gpt-4-turbo-preview`)
- `OPENAI_TEMPERATURE` (default: `0.7`)
- `OPENAI_MAX_TOKENS` (default: `4000`)

**Output:** JSON with `overall_risk_level` (LOW/MEDIUM/HIGH), aggregated `findings`, `recommendations`, and per-agent `reviews_by_agent`.

> **Note:** `_extract_findings`, `_extract_recommendations`, and `_assess_risk_level` in `base_agent.py` are currently placeholders returning hardcoded values. Implement parsing logic there to make the risk assessment meaningful.

---

## Key Conventions

### LLM Provider Switching
Most apps hardcode OpenAI (`gpt-4o` or `gpt-4-turbo-preview`). `DocGenReflect` is the most flexible — it has all providers imported and several options commented out for easy switching. Follow that pattern when adding LLM flexibility.

### Environment Variables
Always use `python-dotenv` and `load_dotenv()` at module entry. Never hardcode API keys. Reference `.env_example` for the full set of supported keys.

### Output Files
All generated documents go to `GeneratedDocs/`. Do not change output paths without updating the corresponding app's hardcoded path string.

### Running Location
**All apps must be run from the repo root directory.** Relative paths (e.g., `OpenDocGen/sections.md`, `GeneratedDocs/`) are resolved relative to CWD. The one exception is `DocumentReviewer/src/main.py`, which uses module-relative imports and may need to be invoked differently (see above).

### Dependencies
- Root `requirements.txt` covers all apps.
- `DocumentReviewer/requirements.txt` mirrors root but adds `python-docx` and `pypdf` for document loading. Keep them in sync when adding packages.

### No Tests
There is no test suite. Validate changes by running the relevant script end-to-end with a real `.env` file.

---

## Common Tasks

**Change the document topic in DocGenTeam:**
Edit the `project_info` string in `DocGenTeam/DocGenTeam.py` → `if __name__ == "__main__":` block.

**Add a new reviewer perspective to Simple Document Reviewer:**
Create a new `.txt` file in `Simple Document Reviewer/agent_prompts/` with a `{document}` placeholder.

**Add a new specialist agent to DocumentReviewer:**
1. Create a new class in `DocumentReviewer/src/agents/` extending `BaseArchitectAgent`.
2. Import and instantiate it in `DocumentReviewer/src/core/orchestrator.py`.
3. Add its key to `self.agent_order` and `self.agents`.

**Switch LLM provider in DocGenReflect:**
Comment/uncomment the LLM initialization lines near the top of `DocGenReflect/DocGenReflect.py` and reassign `GenLLM` and `ReflectLLM`.

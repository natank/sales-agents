# Sales Agents — File Manifest

Complete list of project files and their purposes.

## Root Level Files

### README.md
**Type:** Project overview  
**Purpose:** Quick start guide, tech stack, features, usage examples, limitations  
**Audience:** Everyone (entry point)  
**Read Time:** 10 minutes  
**Key Sections:**
- Quick Start
- Example Usage
- Project Structure
- Tech Stack
- Key Concepts
- Limitations & Future Enhancements

### INDEX.md
**Type:** Navigation guide  
**Purpose:** Complete documentation index and reading guide  
**Audience:** Everyone (reference)  
**Read Time:** 5 minutes  
**Key Sections:**
- Document roadmap
- Project structure overview
- Persona reference table
- Quick setup
- Success criteria
- Reading guide by role

### IMPLEMENTATION-CHECKLIST.md
**Type:** Execution plan  
**Purpose:** Phase-by-phase implementation tasks, success criteria, estimated effort  
**Audience:** Developers, project managers  
**Read Time:** 15 minutes  
**Key Sections:**
- Phase 1: Core Implementation
- Phase 2: Testing & Validation
- Phase 3: Documentation & Polish
- Phase 4: Deployment & Distribution
- Implementation notes
- Common pitfalls
- Testing strategy
- Estimated effort (5-9 hours)

### pyproject.toml
**Type:** Configuration file  
**Purpose:** Python project metadata and dependencies  
**Audience:** Developers, package managers  
**Key Sections:**
- Project metadata (name, version, description)
- Dependencies (openai, python-dotenv)
- Python version requirement (3.12+)

## Documentation Directory (docs/)

### SUMMARY.md
**Type:** Executive summary  
**Purpose:** High-level overview for quick context  
**Audience:** Managers, stakeholders, newcomers  
**Read Time:** 5 minutes  
**Key Sections:**
- At a Glance
- Problem & Solution
- System Architecture
- Personas (table)
- Documentation Map
- Key Features
- Tech Stack
- Success Criteria
- Scope (included/excluded)
- Example Output
- Next Steps

### OPERATIONAL-CONCEPT.md
**Type:** Requirements & vision document  
**Purpose:** Define the problem, solution, use case, and operational flow  
**Audience:** Product managers, business analysts, all stakeholders  
**Read Time:** 10 minutes  
**Key Sections:**
- Overview & Problem Statement
- Use Case (concrete scenario)
- System Flow (visual diagram)
- Key Concepts
- Success Criteria
- Non-Goals (out of scope)
- Fictional Company Context

### REQUIREMENTS.md
**Type:** Functional & technical requirements  
**Purpose:** Detailed specification of what the system must do  
**Audience:** Developers, QA engineers, project managers  
**Read Time:** 15 minutes  
**Key Sections:**
- Functional Requirements (FR1–FR6)
  - Multi-agent email generation
  - Three agent personas
  - Sales picker agent
  - CLI interface
  - Output format
  - Error handling
- Non-Functional Requirements (NFR1–NFR6)
  - Technology stack
  - Configuration & secrets
  - Observability
  - Code organization
  - Documentation
  - Execution model
- User Stories (US1–US3)
- Assumptions & Constraints
- Out of Scope (MVP)

### DESIGN.md
**Type:** Architecture & implementation guide  
**Purpose:** Detailed design, component descriptions, code structure  
**Audience:** Developers, architects  
**Read Time:** 20 minutes  
**Key Sections:**
- Architecture Overview
  - Components: CLI, Orchestrator, API
- Agent Definitions (4 agents)
  - Professional Agent
  - Witty Agent
  - Concise Agent
  - Sales Picker Agent
- Execution Flow
  - Email generation
  - Picker execution
  - Output formatting
- Tool-Free Design (MVP)
- Error Handling Strategy
- Output Format Specification
- Data Flow Diagram
- Example Walkthrough

### FILE-MANIFEST.md
**Type:** Reference guide (this file)  
**Purpose:** Document inventory and purpose reference  
**Audience:** Project managers, documentarians  
**Read Time:** 5 minutes

## Placeholder Directories

### src/
**Status:** To be implemented  
**Contents:** Three Python files (not yet created)

#### src/sales_agents.py (to implement)
**Type:** Main CLI entry point  
**Purpose:** User interface, workflow orchestration, output formatting  
**Expected Size:** 150-200 lines  
**Key Functions:**
- `main()` — CLI orchestration
- `orchestrate_emails(prospect_context)` — Run email generators
- `orchestrate_picker(emails, prospect_context)` — Run picker
- Input validation and error handling

#### src/agents_def.py (to implement)
**Type:** Agent definitions  
**Purpose:** Define all four agents and their orchestration functions  
**Expected Size:** 200-250 lines  
**Key Components:**
- `professional_agent` — Agent instance with system instructions
- `witty_agent` — Agent instance with system instructions
- `concise_agent` — Agent instance with system instructions
- `sales_picker_agent` — Agent instance with ranking instructions
- `generate_email(agent, prospect_context)` — Execute email agent
- `pick_best_email(emails, prospect_context)` — Execute picker agent

#### src/utils.py (to implement)
**Type:** Utility functions  
**Purpose:** Formatting, validation, error handling  
**Expected Size:** 150-200 lines  
**Key Functions:**
- `validate_prospect_input(...)` — Input validation
- `format_email_output(agent_name, persona, email_text)` — Email formatting
- `format_picker_output(chosen_agent, reasoning)` — Picker output formatting
- `get_prospect_input()` — CLI prompts
- Error logging and user-friendly messages

## Document Relationships

```
README.md (start here)
    ├─→ Quick Start → Implementation Checklist
    ├─→ Key Concepts → Design.md (agent definitions)
    └─→ Tech Stack → pyproject.toml

INDEX.md (navigation hub)
    ├─→ SUMMARY.md (overview)
    ├─→ OPERATIONAL-CONCEPT.md (problem/solution)
    ├─→ REQUIREMENTS.md (what to build)
    ├─→ DESIGN.md (how to build)
    └─→ IMPLEMENTATION-CHECKLIST.md (roadmap)

OPERATIONAL-CONCEPT.md
    └─→ Defines fictional company context
        ├─→ Used in DESIGN.md agent definitions
        └─→ Used in src/agents_def.py prompts

REQUIREMENTS.md
    ├─→ Defines what each agent must do
    ├─→ Defines CLI input/output format
    └─→ Defines error handling requirements

DESIGN.md
    ├─→ Specifies agent prompts (based on REQUIREMENTS.md)
    ├─→ Specifies component structure (implemented in src/)
    ├─→ Specifies output format (implemented in src/utils.py)
    └─→ Specifies error handling (implemented in src/sales_agents.py)

IMPLEMENTATION-CHECKLIST.md
    ├─→ References all three src/ files to be created
    ├─→ References testing against REQUIREMENTS.md
    └─→ References tracing observability from DESIGN.md
```

## Reading Paths by Role

### Product Manager / Stakeholder
1. README.md (overview)
2. SUMMARY.md (high-level summary)
3. OPERATIONAL-CONCEPT.md (problem/solution, use case)
4. REQUIREMENTS.md § 3 (user stories)
**Total Time:** 20 minutes

### Developer (Implementation)
1. README.md (quick reference)
2. DESIGN.md (architecture, agents, flow)
3. IMPLEMENTATION-CHECKLIST.md (phase-by-phase)
4. REQUIREMENTS.md (acceptance criteria)
5. pyproject.toml (dependencies)
**Total Time:** 40 minutes

### QA / Test Engineer
1. README.md (usage examples)
2. REQUIREMENTS.md (functional/non-functional requirements)
3. IMPLEMENTATION-CHECKLIST.md § Success Criteria (acceptance tests)
4. DESIGN.md § Output Format (what to expect)
**Total Time:** 25 minutes

### Researcher / Designer (Persona Development)
1. SUMMARY.md (personas table)
2. DESIGN.md § 2 (detailed persona definitions with prompts)
3. OPERATIONAL-CONCEPT.md (fictional company context)
**Total Time:** 15 minutes

### New Team Member (Onboarding)
1. INDEX.md (navigation guide)
2. README.md (project overview)
3. SUMMARY.md (high-level architecture)
4. Pick additional docs based on your role
**Total Time:** 30 minutes + role-specific docs

## File Statistics

| File | Type | Size | Read Time |
|------|------|------|-----------|
| README.md | Overview | ~300 lines | 10 min |
| INDEX.md | Navigation | ~250 lines | 5 min |
| SUMMARY.md | Executive | ~150 lines | 5 min |
| OPERATIONAL-CONCEPT.md | Vision | ~200 lines | 10 min |
| REQUIREMENTS.md | Spec | ~350 lines | 15 min |
| DESIGN.md | Architecture | ~500 lines | 20 min |
| IMPLEMENTATION-CHECKLIST.md | Roadmap | ~250 lines | 15 min |
| FILE-MANIFEST.md | Reference | ~250 lines | 10 min |
| pyproject.toml | Config | ~20 lines | 2 min |
| **Total** | **8 documents** | **~2,300 lines** | **90 min** |

## Maintenance & Updates

### When to Update Which File

- **README.md** → When quick start or usage changes
- **SUMMARY.md** → When architecture or key concepts change
- **OPERATIONAL-CONCEPT.md** → When problem statement or use case changes
- **REQUIREMENTS.md** → When functional/non-functional specs change
- **DESIGN.md** → When component design or agent prompts change
- **IMPLEMENTATION-CHECKLIST.md** → After each implementation phase
- **FILE-MANIFEST.md** → When files are added/removed/relocated
- **pyproject.toml** → When dependencies or Python version changes

### Version Control

All documents in `docs/` have a header with:
- **Document Version:** Incremented on significant changes
- **Last Updated:** Date of most recent update
- **Status:** Current status (e.g., "Complete", "Draft", "Ready to implement")

## Verification Checklist

- ✅ All files exist and are readable
- ✅ No broken internal links between documents
- ✅ All code examples in docs match intended implementation
- ✅ All URLs/references to external resources are valid
- ✅ Document dates are current and accurate
- ✅ All personas defined in DESIGN.md match SUMMARY.md
- ✅ All requirements in REQUIREMENTS.md addressed in DESIGN.md
- ✅ All tasks in IMPLEMENTATION-CHECKLIST.md map to DESIGN.md

---

**Manifest Version:** 1.0  
**Last Updated:** 2026-07-27  
**Status:** Complete & Verified

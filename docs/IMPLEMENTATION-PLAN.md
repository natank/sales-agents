# Sales Agents — Implementation Plan

**Created:** 2026-07-27  
**Status:** Ready for Implementation  
**Estimated Duration:** 5-9 hours  
**Target Completion:** 2026-07-28 (1 sprint)

## Overview

This document outlines the step-by-step implementation roadmap for the Sales Agents project, broken into 4 phases with clear deliverables, acceptance criteria, and PR structure.

## PR Workflow Policy (applies to every phase)

This policy is mandatory for all PRs in this project — no exceptions, including for solo/AI-assisted work.

1. **No direct commits to `main`.** All work happens on a feature branch cut from `main` (e.g. `feature/core-implementation`).
2. **Every PR must have a comprehensive description**, including at minimum:
   - `## Summary` — what changed and why
   - `## What Changed` — file-by-file breakdown
   - `## Test Plan` — how it was/will be verified
   - `## Acceptance Criteria` — checklist tied back to the phase's criteria in this document
3. **CI must be green before merge.** A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every PR and push to `main`, at minimum:
   - Dependency install (`uv sync`)
   - Lint (`ruff check`)
   - Format check (`black --check` or `ruff format --check`)
   - Any automated tests present (`pytest`, once added)
   - A basic import/smoke check that `src/` modules import cleanly
4. **Merge is blocked on red or pending CI.** Do not merge with failing or in-progress checks, and do not bypass branch protection to force a merge.
5. **Squash-merge preferred**, using the PR title as the squash commit message, then delete the feature branch.
6. **Branch protection on `main`** should require: PR review (or self-review sign-off for solo work), the CI check passing, and no direct pushes.

Every "Merge Criteria" list in this document is in addition to — not a replacement for — this policy. A phase is not done until its branch is merged into `main` via a reviewed PR with green CI.

## Phase Summary

| Phase | Title | Duration | PRs | Status |
|-------|-------|----------|-----|--------|
| 1 | Core Implementation | 2-3 hrs | 3 | 🔄 Ready |
| 2 | Testing & Validation | 1-2 hrs | 1 | 📋 Planned |
| 3 | Polish & Documentation | 1 hr | 1 | 📋 Planned |
| 4 | Deployment & Release | 1 hr | 1 | 📋 Planned |

---

## PHASE 1: Core Implementation (2-3 hours)

**Goal:** Implement the three core source files with all agent definitions and orchestration logic.

### 1.1 Create `src/agents_def.py`

**Objective:** Define all four agents and implement orchestration functions.

**Scope:**
- Define `professional_agent` (system instructions from DESIGN.md § 2.1)
- Define `witty_agent` (system instructions from DESIGN.md § 2.2)
- Define `concise_agent` (system instructions from DESIGN.md § 2.3)
- Define `sales_picker_agent` (system instructions from DESIGN.md § 2.4)
- Implement `generate_email(agent, prospect_context) → str`
- Implement `pick_best_email(emails, prospect_context) → tuple[str, str]`

**Acceptance Criteria:**
- ✅ All four agents instantiated with OpenAI Agents SDK `Agent` class
- ✅ System instructions match DESIGN.md specifications
- ✅ `generate_email()` accepts an agent and prospect context, returns email text
- ✅ `pick_best_email()` accepts dict of emails and prospect context, returns (agent_name, reasoning)
- ✅ Both functions handle OpenAI API errors gracefully (raise with descriptive messages)
- ✅ Type hints on all function signatures
- ✅ Module-level docstring and function docstrings present
- ✅ Imports organized (stdlib, third-party, local)

**PR Details:**
- **Title:** `feat: implement agent definitions and orchestration (Phase 1a)`
- **Scope:** New file only
- **File:** `src/agents_def.py` (~220 lines)
- **Dependencies:** `openai` SDK

**Implementation Checklist:**
- [ ] Import OpenAI SDK: `from agents import Agent, Runner`
- [ ] Define `professional_agent` with system instructions (formal, ROI-focused)
- [ ] Define `witty_agent` with system instructions (clever, conversational)
- [ ] Define `concise_agent` with system instructions (direct, scannable)
- [ ] Define `sales_picker_agent` with system instructions (expert ranker)
- [ ] Implement `generate_email()` using `Runner.run()`
- [ ] Implement `pick_best_email()` using `Runner.run()`
- [ ] Add error handling (API errors, model errors)
- [ ] Add type hints and docstrings
- [ ] Test imports work correctly
- [ ] Code review: check against DESIGN.md § 2

---

### 1.2 Create `src/utils.py`

**Objective:** Implement formatting, validation, and helper functions.

**Scope:**
- Implement `validate_prospect_input(company, industry, pain_point, outcome) → bool`
- Implement `format_email_output(agent_name, persona, email_text) → str`
- Implement `format_picker_output(chosen_agent, reasoning) → str`
- Implement `get_prospect_input() → dict`
- Implement error logging helpers
- Implement user-friendly error messages

**Acceptance Criteria:**
- ✅ Input validation returns `True` for valid input, raises `ValueError` for invalid
- ✅ Email formatting includes agent name, persona, subject line, body, dividers
- ✅ Picker formatting includes chosen agent name and reasoning (1-2 sentences)
- ✅ Input prompts are clear and user-friendly
- ✅ Error messages are concise and actionable (no stack traces)
- ✅ Type hints on all function signatures
- ✅ Docstrings present and clear
- ✅ Output matches DESIGN.md § 5 format specification

**PR Details:**
- **Title:** `feat: implement utilities and formatting (Phase 1b)`
- **Scope:** New file only
- **File:** `src/utils.py` (~180 lines)
- **Dependencies:** `sys`, `logging` (stdlib)

**Implementation Checklist:**
- [ ] Implement `validate_prospect_input()` (check non-empty strings)
- [ ] Implement `format_email_output()` with dividers and clear sections
- [ ] Implement `format_picker_output()` with recommendation header
- [ ] Implement `get_prospect_input()` with clear prompts
- [ ] Implement `log_error()` for internal logging
- [ ] Implement `user_error_message()` for error display
- [ ] Add type hints and docstrings
- [ ] Test formatting outputs look clean (visual inspection)
- [ ] Code review: check against DESIGN.md § 5

---

### 1.3 Create `src/sales_agents.py`

**Objective:** Implement CLI entry point and main orchestration workflow.

**Scope:**
- Implement `main()` function
- Implement CLI argument parsing (or interactive prompts)
- Implement `orchestrate_emails(prospect_context) → dict`
- Implement `orchestrate_picker(emails, prospect_context) → tuple`
- Wire up all components: agents_def + utils
- Implement error handling and graceful fallbacks

**Acceptance Criteria:**
- ✅ CLI accepts prospect input via interactive prompts or arguments
- ✅ Calls `orchestrate_emails()` to generate three emails
- ✅ Prints all three formatted emails with clear separators
- ✅ Calls `orchestrate_picker()` to rank emails
- ✅ Prints picker result with chosen agent and reasoning
- ✅ Handles errors gracefully (no stack traces to user)
- ✅ Validates input before passing to agents
- ✅ Exit code 0 on success, non-zero on error
- ✅ Type hints and docstrings present
- ✅ Can be run as: `uv run python src/sales_agents.py`

**PR Details:**
- **Title:** `feat: implement CLI and orchestration (Phase 1c)`
- **Scope:** New file only
- **File:** `src/sales_agents.py` (~160 lines)
- **Dependencies:** `agents_def`, `utils`, `os` (for OPENAI_API_KEY)

**Implementation Checklist:**
- [ ] Implement `main()` as entry point
- [ ] Add argument parsing (argparse or simple interactive)
- [ ] Implement `orchestrate_emails()` to call all three agents
- [ ] Implement `orchestrate_picker()` to call picker agent
- [ ] Add input validation using utils.validate_prospect_input()
- [ ] Add error handling for API errors
- [ ] Format and print emails using utils.format_email_output()
- [ ] Format and print picker result using utils.format_picker_output()
- [ ] Add graceful error messages (no stack traces)
- [ ] Test: run with sample input, verify output
- [ ] Code review: check against DESIGN.md § 3

---

### Phase 1 Deliverable: PR #1 (Core Implementation)

**PR Title:** `feat: core implementation of sales agents system`

**Description:**
```
## Summary
Implement the three core source files for the Sales Agents system:
- src/agents_def.py: Agent definitions and orchestration
- src/utils.py: Formatting, validation, error handling
- src/sales_agents.py: CLI entry point and workflow

## What Changed
- Added 4 agent definitions (Professional, Witty, Concise, Picker)
- Implemented generate_email() and pick_best_email() orchestration
- Added formatting and validation utilities
- Implemented CLI with interactive prospect input
- Error handling and graceful fallbacks

## Test Plan
- [ ] Run with sample prospect scenario (FinTech company)
- [ ] Verify 3 distinct emails are generated
- [ ] Verify picker selects one email with reasoning
- [ ] Verify output formatting is clean and readable
- [ ] Test error handling (invalid input, API errors)
- [ ] Check traces in OpenAI platform dashboard

## Acceptance Criteria
- All 3 files implement their design specifications
- Code quality: PEP 8, type hints, docstrings
- Error handling is graceful with user-friendly messages
- Output matches DESIGN.md specification
- All 4 agents produce distinct, coherent responses
```

**Branches & Commits:**
```
main
 └─ feature/core-implementation (from main)
     ├─ commit 1: Add agents_def.py with 4 agent definitions
     ├─ commit 2: Add utils.py with formatting and validation
     ├─ commit 3: Add sales_agents.py with CLI orchestration
     └─ [PR #1 created]
```

**Merge Criteria:**
- ✅ All code reviewed and approved
- ✅ Manual testing passed with 2+ scenarios
- ✅ Traces visible in OpenAI platform dashboard
- ✅ No security issues (no hardcoded keys, etc.)
- ✅ CI green on the PR (see PR Workflow Policy above) — merge blocked otherwise

---

### 1.4 Set up CI (`.github/workflows/ci.yml`)

**Objective:** Add the GitHub Actions workflow that gates all future merges, required by the PR Workflow Policy.

**Scope:**
- Trigger on `pull_request` (all branches → `main`) and `push` to `main`
- Steps: checkout → set up Python 3.12 → install `uv` → `uv sync` → `ruff check` → `ruff format --check` (or `black --check`) → smoke-import `src/` modules → run `pytest` if tests exist

**Acceptance Criteria:**
- ✅ Workflow file present at `.github/workflows/ci.yml`
- ✅ Workflow runs automatically on PR open/update
- ✅ Workflow fails the check on lint/format errors or import errors
- ✅ Branch protection on `main` set to require this check before merge

**PR Details:**
- Bundled into PR #1 (same branch, `feature/core-implementation`), as CI must exist before the first PR can be validly merged under this policy.

---

## PHASE 2: Testing & Validation (1-2 hours)

**Goal:** Comprehensively test the implementation with multiple scenarios and verify quality.

### 2.1 Manual Testing

**Objective:** Test the system end-to-end with diverse scenarios.

**Test Scenarios:**

**Scenario A: FinTech Company**
```
Company: Acme Financial
Industry: Finance
Pain Point: Manual reconciliation delays between payment systems
Outcome: Automate reconciliation to save 8 hours/week
```
Expected: Concise likely winner (quantitative buyers prefer bullets)

**Scenario B: Creative Startup**
```
Company: DesignFlow Studios
Industry: Design/Marketing
Pain Point: Team collaboration across multiple time zones
Outcome: Centralize all workflows in one platform
```
Expected: Witty likely winner (creative teams respond to personality)

**Scenario C: Enterprise Insurance**
```
Company: Guardian Insurance Corp
Industry: Financial Services
Pain Point: Compliance-heavy data workflows with error-prone manual steps
Outcome: Reduce compliance risk and audit time
```
Expected: Professional likely winner (enterprises value credentials)

**Test Checklist:**
- [ ] Run Scenario A: Verify output, check picker choice
- [ ] Run Scenario B: Verify output, check picker choice
- [ ] Run Scenario C: Verify output, check picker choice
- [ ] Verify emails are distinct and coherent
- [ ] Verify output formatting is clean and readable
- [ ] Verify error handling (try invalid input)
- [ ] Verify error messages are user-friendly

**Acceptance Criteria:**
- ✅ All 3 scenarios produce valid, distinct emails
- ✅ Picker choices align with scenario context
- ✅ Output is clean and easy to read
- ✅ No stack traces or technical errors shown to user
- ✅ Invalid input handled gracefully

---

### 2.2 Trace Inspection

**Objective:** Verify all agent runs appear in OpenAI Traces dashboard.

**Steps:**
1. Complete a full run of the app (Phase 2.1 Scenario A)
2. Log into OpenAI platform: https://platform.openai.com
3. Navigate to Traces dashboard
4. Filter by project/model (if applicable)
5. Verify 4 traces appear (3 email agents + 1 picker)
6. Inspect each trace:
   - Input prompt visible
   - Model name (`gpt-4-mini`)
   - Output text visible
   - Execution time reasonable

**Acceptance Criteria:**
- ✅ 4 traces visible in Traces dashboard
- ✅ Each trace shows full input/output
- ✅ No errors in traces
- ✅ Execution time reasonable (~10-30 sec for 4 calls)

---

### 2.3 Code Quality & Security

**Objective:** Verify code meets quality standards.

**Checklist:**
- [ ] PEP 8 compliance: Run `black` or `ruff format`
- [ ] Type hints: All functions have parameter and return types
- [ ] Docstrings: All public functions have docstrings
- [ ] Security: No hardcoded secrets (API keys, etc.)
- [ ] Error handling: All exceptions caught and handled gracefully
- [ ] Imports: Organized and no unused imports
- [ ] Performance: No obvious inefficiencies
- [ ] Logging: Appropriate logging for debugging

**Acceptance Criteria:**
- ✅ Code passes PEP 8 linter
- ✅ All functions have type hints
- ✅ All public functions have docstrings
- ✅ No hardcoded secrets
- ✅ No stack traces exposed to users

---

### 2.4 Agent Prompt Iteration (Optional)

**Objective:** Fine-tune agent prompts if needed based on output quality.

**If emails lack distinct styles:**
- Professional: Increase emphasis on credentials, compliance, ROI metrics
- Witty: Increase humor/relatability, ensure stays professional
- Concise: Reduce word count, emphasize bullet points

**If picker makes unexpected choices:**
- Review picker's reasoning
- Adjust picker agent instructions if ranking criteria unclear
- Consider adding explicit examples to picker instructions

**Acceptance Criteria:**
- ✅ All three emails have distinct, recognizable personas
- ✅ Emails are persuasive and ready-to-send (with minor tweaks)
- ✅ Picker's choices make intuitive sense for scenarios

---

### Phase 2 Deliverable: PR #2 (Testing & Iteration)

**PR Title:** `test: comprehensive testing and prompt iteration`

**Description:**
```
## Summary
Comprehensive testing of the implementation with multiple scenarios,
trace inspection, and optional prompt refinements based on quality.

## What Changed
- Tested with 3 diverse scenarios (FinTech, Creative, Enterprise)
- Verified traces in OpenAI Traces dashboard
- Code quality checks (PEP 8, type hints, docstrings)
- Iteration on agent prompts for consistency and quality

## Test Results
- Scenario A (FinTech): ✓ Pass
- Scenario B (Creative): ✓ Pass
- Scenario C (Enterprise): ✓ Pass
- Traces visible: ✓ Yes (4 traces per run)
- Code quality: ✓ Pass

## Files Modified (if any)
- src/agents_def.py: Minor prompt refinements

## Acceptance Criteria
- All test scenarios pass
- Output quality is high (distinct personas, persuasive)
- Traces visible in platform dashboard
- Code meets quality standards
```

**Test Report Attachment:**
Include a summary of all test scenarios and results:
```
TEST RESULTS SUMMARY
====================

Scenario A - FinTech (Acme Financial)
  Email 1 (Professional): Professional tone, ROI emphasis ✓
  Email 2 (Witty): Clever, conversational ✓
  Email 3 (Concise): Scannable bullet points ✓
  Picker Choice: Concise (expected for quant buyers) ✓

Scenario B - Creative (DesignFlow Studios)
  Email 1 (Professional): Formal, credentials ✓
  Email 2 (Witty): Witty, personality-driven ✓
  Email 3 (Concise): Direct, efficient ✓
  Picker Choice: Witty (expected for creative teams) ✓

Scenario C - Enterprise (Guardian Insurance)
  Email 1 (Professional): Formal, compliance-focused ✓
  Email 2 (Witty): Clever, professional ✓
  Email 3 (Concise): Scannable, efficient ✓
  Picker Choice: Professional (expected for enterprises) ✓

Traces Dashboard: 4 traces per run visible ✓
Code Quality: PEP 8 compliant ✓
Error Handling: Graceful, no stack traces ✓
```

**Merge Criteria:**
- ✅ All test scenarios pass
- ✅ Traces visible in OpenAI Traces dashboard
- ✅ Code quality verified
- ✅ Prompt quality acceptable
- ✅ CI green on the PR — merge blocked otherwise

---

## PHASE 3: Polish & Documentation (1 hour)

**Goal:** Update documentation with real examples and ensure project is ready for use.

### 3.1 Update README.md

**Additions:**
- Add real example output from Phase 2 testing
- Add troubleshooting section
- Update quick start with verified commands
- Add notes on model availability / fallback

**Example to Add:**
```markdown
## Example Run

[Insert real output from Scenario A test]

## Troubleshooting

**Issue:** "Invalid API key"
**Solution:** Ensure OPENAI_API_KEY env var is set correctly

**Issue:** "Rate limit exceeded"
**Solution:** Model is at rate limit. Retry in 60 seconds.

**Issue:** "Email generation failed for one agent"
**Solution:** Agent failed for a specific persona. Check traces in dashboard.
```

**Acceptance Criteria:**
- ✅ Example output is real and reflects actual system behavior
- ✅ Troubleshooting section covers common issues
- ✅ Quick start commands are verified to work

---

### 3.2 Update IMPLEMENTATION-CHECKLIST.md

**Update:**
- Mark completed phases as ✅
- Add notes on what was learned/changed
- Update status for each task

```markdown
## Phase 1: Core Implementation (2-3 hours) ✅ COMPLETE
- [x] src/agents_def.py
- [x] src/utils.py
- [x] src/sales_agents.py

## Phase 2: Testing & Validation (1-2 hours) ✅ COMPLETE
- [x] Manual testing (3 scenarios)
- [x] Trace inspection
- [x] Code quality verification
- [x] Prompt iteration

## Phase 3: Polish & Documentation (1 hour) ⏳ IN PROGRESS
```

**Acceptance Criteria:**
- ✅ All completed phases marked with ✅
- ✅ Checklist reflects actual work done
- ✅ Notes added on learnings/changes

---

### 3.3 Create EXAMPLE-RUNS.md

**Objective:** Document example runs for future reference.

**Content:**
```markdown
# Sales Agents — Example Runs

## Example 1: FinTech Company

### Input
- Company: Acme Financial
- Industry: Finance
- Pain Point: Manual reconciliation delays
- Outcome: Automate reconciliation to save 8 hours/week

### Output
[Full output from actual run]

### Analysis
- Professional email: Formal, ROI-focused, case studies
- Witty email: Clever, personable, humor
- Concise email: Bullet points, scannable, efficient
- Picker choice: Concise (quantitative buyers prefer efficiency)

[Repeat for Scenarios B & C]
```

**Acceptance Criteria:**
- ✅ 3 example runs documented with real output
- ✅ Analysis provided for each run
- ✅ File is useful reference for future users

---

### Phase 3 Deliverable: PR #3 (Polish & Documentation)

**PR Title:** `docs: update documentation with examples and troubleshooting`

**Description:**
```
## Summary
Update documentation with real example outputs, troubleshooting guide,
and example runs for future reference.

## What Changed
- Updated README.md with real example output
- Added troubleshooting section to README
- Updated IMPLEMENTATION-CHECKLIST.md with completion status
- Added EXAMPLE-RUNS.md with 3 documented scenarios

## Files Modified
- README.md
- IMPLEMENTATION-CHECKLIST.md
- docs/ (new file: EXAMPLE-RUNS.md)

## Acceptance Criteria
- Documentation is clear and helpful
- Examples reflect actual system behavior
- Troubleshooting section covers common issues
```

**Merge Criteria:**
- ✅ Documentation is clear and helpful
- ✅ Examples are real (from Phase 2 testing)
- ✅ No broken links or formatting issues
- ✅ CI green on the PR — merge blocked otherwise

---

## PHASE 4: Deployment & Release (1 hour)

**Goal:** Prepare project for release and make it publicly available.

### 4.1 Repository Setup

**Steps:**
- [ ] Initialize git repo (if not already done): `git init`
- [ ] Create `.gitignore`:
  ```
  .env
  __pycache__/
  *.pyc
  .venv/
  .DS_Store
  *.egg-info/
  .pytest_cache/
  .ruff_cache/
  ```
- [ ] Create `LICENSE` file (MIT License)
- [ ] Verify all files are tracked: `git status`
- [ ] Create initial commit: `git add . && git commit -m "Initial commit: Sales Agents project"`

**Acceptance Criteria:**
- ✅ Git repo initialized
- ✅ `.gitignore` created
- ✅ `LICENSE` file added
- ✅ Initial commit created

---

### 4.2 GitHub Integration (Optional)

**Steps:**
- [ ] Create GitHub repository: https://github.com/natank/sales-agents
- [ ] Add remote: `git remote add origin https://github.com/natank/sales-agents.git`
- [ ] Push to GitHub: `git push -u origin main`
- [ ] Add README badge (optional): Build status, Python version
- [ ] Verify GitHub Actions (if set up)

**Acceptance Criteria:**
- ✅ Repo pushed to GitHub
- ✅ README visible on GitHub
- ✅ All files accessible

---

### 4.3 Update Work Portfolio

**Steps:**
- [ ] Update `/Users/nati-home/Projects/agents/work/README.md`
- [ ] Add sales-agents to project list

```markdown
### [sales-agents](./sales-agents/)
A multi-agent cold email generator using the OpenAI Agents SDK.

**Demonstrates:**
- Multi-agent orchestration (3 agents with distinct personas)
- Expert ranking / selection layer
- Automatic tracing in OpenAI Traces dashboard
- LLM-driven content generation and decision-making
- CLI design and orchestration

**Tech stack:** Python, OpenAI API, OpenAI Agents SDK

**Status:** Complete and published
```

**Acceptance Criteria:**
- ✅ sales-agents added to work/README.md
- ✅ Description accurate and helpful

---

### Phase 4 Deliverable: PR #4 (Release & Deployment)

**PR Title:** `chore: repository setup and release preparation`

**Description:**
```
## Summary
Set up git repository, add project to work portfolio, and prepare
for public release.

## What Changed
- Created .gitignore
- Added LICENSE (MIT)
- Updated work/README.md with sales-agents entry
- Pushed to GitHub (optional)

## Files Added/Modified
- .gitignore
- LICENSE
- work/README.md

## Acceptance Criteria
- Repository initialized and clean
- Project added to work portfolio
- Ready for public use
```

**Merge Criteria:**
- ✅ All repository files in place
- ✅ Project discoverable via work portfolio
- ✅ No broken links or issues
- ✅ CI green on the PR — merge blocked otherwise

---

## Overall Implementation Timeline

```
Day 1 (2026-07-27 or 2026-07-28):
  Morning:   Phase 1 (2-3 hrs) → PR #1 Review & Merge
  Afternoon: Phase 2 (1-2 hrs) → PR #2 Review & Merge
  
Day 2 (2026-07-28 or 2026-07-29):
  Morning:   Phase 3 (1 hr) → PR #3 Review & Merge
  Afternoon: Phase 4 (1 hr) → PR #4 Review & Merge
  
Total: 5-9 hours
Status: Complete & Released
```

## PR Summary

| PR # | Title | Phase | Files | Duration | Status |
|------|-------|-------|-------|----------|--------|
| 1 | Core Implementation | Phase 1 | 3 new | 2-3 hrs | 📋 Pending |
| 2 | Testing & Iteration | Phase 2 | 0-1 mod | 1-2 hrs | 📋 Planned |
| 3 | Polish & Docs | Phase 3 | 3 mod | 1 hr | 📋 Planned |
| 4 | Release & Deploy | Phase 4 | 2 new | 1 hr | 📋 Planned |

## Success Criteria

**Global Success Criteria:**
- ✅ All 4 phases complete
- ✅ 4 PRs merged successfully, each via a feature branch with a comprehensive PR description and green CI (no direct commits to `main`)
- ✅ System works end-to-end
- ✅ Code quality high
- ✅ Documentation comprehensive
- ✅ Project released publicly (optional)

**Phase-Specific Success Criteria:**
- Phase 1: ✅ Core implementation complete, no errors
- Phase 2: ✅ Testing complete, traces visible, quality verified
- Phase 3: ✅ Documentation updated, examples real and helpful
- Phase 4: ✅ Repository clean, project discoverable

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| API errors during testing | Retry with exponential backoff, check rate limits |
| Agent prompts produce poor output | Iterate on system instructions, test with examples |
| Documentation outdated quickly | Keep docs aligned with code; update after each PR |
| Traces not visible in dashboard | Check OpenAI project settings, verify auth |

## Dependencies & Assumptions

**Dependencies:**
- Python 3.12+
- `openai` SDK with Agents SDK
- Valid OpenAI API key

**Assumptions:**
- `gpt-4-mini` model is available in OpenAI account
- Network connectivity to OpenAI API
- No rate limits blocking testing (Phase 2)
- Developers familiar with Python and git

## Rollback Plan

**If Phase 1 fails:**
- Discard branch, return to main
- Review design doc for misunderstandings
- Retry with corrected approach

**If Phase 2 fails:**
- Keep Phase 1 work, debug in a new branch
- Fix issues in agents_def.py or utils.py
- Re-test before merging

**If Phase 3/4 fails:**
- Documentation issues only; no code impact
- Easy to fix and re-merge

---

**Document Version:** 1.0  
**Last Updated:** 2026-07-27  
**Status:** Ready for Implementation  
**Next Step:** Start Phase 1 → Create `src/agents_def.py`

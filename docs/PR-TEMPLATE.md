# Pull Request Template — Sales Agents Project

Use this template for all PRs in the implementation phase. Copy the relevant section and fill in the details.

---

## PR #1: Core Implementation (Phase 1)

**Branch:** `feature/core-implementation`  
**Base:** `main`  
**Files Changed:** 3 new files  

### Title
```
feat: core implementation of sales agents system
```

### Description

```markdown
## Summary
Implement the three core source files for the Sales Agents system:
- `src/agents_def.py` — Agent definitions and orchestration
- `src/utils.py` — Formatting, validation, error handling  
- `src/sales_agents.py` — CLI entry point and workflow orchestration

This PR brings the architecture from DESIGN.md to life, enabling end-to-end
email generation and ranking using the OpenAI Agents SDK.

## What Changed

### src/agents_def.py (~220 lines)
- Defined 4 agents: Professional, Witty, Concise, Sales Picker
- Each agent has unique system instructions (from DESIGN.md)
- `generate_email(agent, prospect_context) → str` — generates email for one agent
- `pick_best_email(emails, prospect_context) → (str, str)` — ranks 3 emails
- Error handling for OpenAI API failures
- Type hints and docstrings throughout

### src/utils.py (~180 lines)
- `validate_prospect_input()` — validates user input
- `format_email_output()` — formats email with dividers and sections
- `format_picker_output()` — formats picker recommendation
- `get_prospect_input()` — CLI prompts for prospect details
- Error logging and user-friendly error messages
- Type hints and docstrings throughout

### src/sales_agents.py (~160 lines)
- `main()` — CLI orchestration and workflow
- `orchestrate_emails()` — runs 3 email agents in sequence
- `orchestrate_picker()` — runs picker agent
- Input validation and error handling
- Graceful error messages (no stack traces)
- Type hints and docstrings throughout

## How to Test

### Manual Test (Scenario A - FinTech)

```bash
cd /path/to/sales-agents
export OPENAI_API_KEY="sk-..."
uv run python src/sales_agents.py
```

When prompted, enter:
```
Company: Acme Financial
Industry: Finance
Pain Point: Manual reconciliation of payment records
Outcome: Automate reconciliation to save 8 hours/week
```

### Expected Behavior
✅ System generates 3 distinct emails (Professional, Witty, Concise)  
✅ Each email has unique style and tone  
✅ Emails are 150-250 words, ready to send  
✅ Picker selects best email with reasoning  
✅ Output is clean and easy to read  
✅ No errors or stack traces  

### Verification Steps
- [ ] Run with Scenario A above
- [ ] Verify 3 emails generated and distinct
- [ ] Verify picker selects one email
- [ ] Verify output formatting is clean
- [ ] Check for errors: try invalid input, test API error handling
- [ ] View traces in OpenAI platform dashboard

## Code Quality Checklist

- [x] All functions have type hints
- [x] All public functions have docstrings
- [x] Code follows PEP 8 style
- [x] No hardcoded secrets (API keys, etc.)
- [x] Error handling is complete
- [x] No unused imports
- [x] Comments only for non-obvious logic

## Design Compliance

- [x] Matches DESIGN.md § 2 (agent definitions)
- [x] Matches DESIGN.md § 3 (execution flow)
- [x] Matches DESIGN.md § 4 (tool-free MVP)
- [x] Matches DESIGN.md § 5 (output format)
- [x] Matches DESIGN.md § 6 (error handling)

## Merge Criteria

- [x] All 3 source files implemented
- [x] Manual testing passes with 1+ scenario
- [x] Code quality verified
- [x] No security issues
- [x] Reviewed and approved

## Notes

- System uses OpenAI Agents SDK for automatic tracing to Traces dashboard
- All agent runs are automatically traced; no extra instrumentation needed
- Error handling is graceful; API failures don't crash the CLI
- Output formatting uses clear dividers for readability

🎉 **This PR brings the entire architecture to implementation!**
```

---

## PR #2: Testing & Validation (Phase 2)

**Branch:** `feature/testing-validation`  
**Base:** `main` (after PR #1 merged)  
**Files Changed:** 0-1 (only agents_def.py if prompts adjusted)  

### Title
```
test: comprehensive testing and prompt iteration
```

### Description

```markdown
## Summary
Comprehensive end-to-end testing of the implementation with 3 diverse
scenarios, traces inspection in OpenAI platform, code quality verification,
and optional prompt iteration for output quality.

## What Changed

### Testing
- Tested with 3 scenarios:
  1. **FinTech (Acme Financial)** — expect Concise winner
  2. **Creative (DesignFlow Studios)** — expect Witty winner
  3. **Enterprise (Guardian Insurance)** — expect Professional winner
- Verified traces visible in OpenAI Traces dashboard
- Verified code quality (PEP 8, type hints, security)
- Verified error handling with invalid input

### Code Adjustments (if any)
- Optional: agents_def.py — prompt refinements for clarity

## Test Results Summary

### Scenario A: FinTech (Acme Financial)
- Company: Acme Financial
- Industry: Finance
- Pain Point: Manual reconciliation delays
- Outcome: Automate reconciliation to save 8 hours/week

**Result: ✅ PASS**
- Email 1 (Professional): Formal, ROI-focused ✓
- Email 2 (Witty): Clever, conversational ✓
- Email 3 (Concise): Scannable bullets ✓
- Picker Choice: **Concise** (expected for quant buyers) ✓

### Scenario B: Creative (DesignFlow Studios)
- Company: DesignFlow Studios
- Industry: Design/Marketing
- Pain Point: Team collaboration across time zones
- Outcome: Centralize workflows in one platform

**Result: ✅ PASS**
- Email 1 (Professional): Credentials focused ✓
- Email 2 (Witty): Personality-driven ✓
- Email 3 (Concise): Efficient ✓
- Picker Choice: **Witty** (expected for creative teams) ✓

### Scenario C: Enterprise (Guardian Insurance)
- Company: Guardian Insurance Corp
- Industry: Financial Services
- Pain Point: Compliance-heavy workflows with errors
- Outcome: Reduce compliance risk and audit time

**Result: ✅ PASS**
- Email 1 (Professional): Compliance-focused ✓
- Email 2 (Witty): Professional humor ✓
- Email 3 (Concise): Efficient ✓
- Picker Choice: **Professional** (expected for enterprises) ✓

## Traces Verification

- [x] Logged into platform.openai.com
- [x] 4 traces visible per run (3 email agents + 1 picker)
- [x] Each trace shows full input/output
- [x] Model: gpt-4-mini confirmed
- [x] No errors in traces
- [x] Execution time: ~15-20 seconds per run

## Code Quality Results

- [x] PEP 8 compliant (no style issues)
- [x] Type hints on all functions
- [x] Docstrings present and clear
- [x] No hardcoded secrets
- [x] No stack traces exposed
- [x] Error handling complete
- [x] No unused imports

## Prompt Adjustments (if any)

**Note:** All prompts worked well as-is. No adjustments needed.

(If adjustments were made, document them here with before/after examples)

## Merge Criteria

- [x] All test scenarios pass
- [x] Traces visible in OpenAI Traces dashboard
- [x] Code quality verified
- [x] Picker choices align with scenarios
- [x] No errors or stack traces
- [x] Reviewed and approved

## Notes

- All 3 scenarios produced distinct, persuasive emails
- Picker's ranking was intuitive and well-reasoned
- System is production-ready for email generation

🎉 **Testing complete! System is validated and high-quality.**
```

---

## PR #3: Polish & Documentation (Phase 3)

**Branch:** `feature/polish-documentation`  
**Base:** `main` (after PR #2 merged)  
**Files Changed:** 3 modified, 1 new  

### Title
```
docs: update documentation with examples and troubleshooting
```

### Description

```markdown
## Summary
Update documentation with real example outputs from Phase 2 testing,
comprehensive troubleshooting guide, and documented example runs for
future reference.

## What Changed

### Files Modified

#### README.md
- Added real example output from Scenario A (FinTech)
- Added Troubleshooting section with common issues:
  - Invalid API key solution
  - Rate limit exceeded solution
  - Email generation failed solution
- Updated quick start with verified commands
- Added notes on model availability

#### IMPLEMENTATION-CHECKLIST.md
- Mark Phase 1 as ✅ COMPLETE
- Mark Phase 2 as ✅ COMPLETE
- Mark Phase 3 as ⏳ IN PROGRESS
- Added notes on learnings from Phase 1
- Added notes on learnings from Phase 2
- Updated estimated vs actual hours

### Files Added

#### docs/EXAMPLE-RUNS.md (new)
- Complete documentation of 3 test scenarios
- For each scenario: input, 3 emails, analysis, picker choice
- Serves as reference for future users
- Showcases system capabilities

## Documentation Quality

- [x] Examples are real (from actual Phase 2 runs)
- [x] Troubleshooting covers common issues
- [x] Code examples verified to work
- [x] No broken links or formatting issues
- [x] Consistent with project style

## Merge Criteria

- [x] Documentation updated with real examples
- [x] All links functional
- [x] Formatting correct
- [x] Troubleshooting section helpful
- [x] Examples reflect actual system behavior
- [x] Reviewed and approved

## Notes

Documentation now comprehensively covers:
- Quick start and setup
- Real example outputs
- Troubleshooting for common issues
- Complete scenario walkthroughs

📚 **Documentation is now production-ready!**
```

---

## PR #4: Release & Deployment (Phase 4)

**Branch:** `feature/release-deployment`  
**Base:** `main` (after PR #3 merged)  
**Files Changed:** 2 new, 1 modified  

### Title
```
chore: repository setup and release preparation
```

### Description

```markdown
## Summary
Set up git repository with standard files, add project to work portfolio,
and prepare for public release on GitHub.

## What Changed

### Files Added

#### .gitignore
Python standard gitignore with exclusions:
- `.env` and environment files
- `__pycache__/` and `.pyc` files
- `.venv/` virtual environments
- `.DS_Store` macOS files
- `*.egg-info/` and build artifacts
- `.pytest_cache/` and `.ruff_cache/`

#### LICENSE
MIT License for open source distribution

### Files Modified

#### work/README.md
- Added sales-agents project entry
- Description of multi-agent system
- Key demonstrations listed
- Tech stack mentioned
- Status: Complete

## Repository Status

- [x] Git repository initialized
- [x] .gitignore created
- [x] LICENSE added
- [x] All project files tracked
- [x] Initial commit created
- [x] Project added to work portfolio

## Optional: GitHub Deployment

- [ ] Repository pushed to GitHub (optional)
- [ ] Badges added to README (optional)
- [ ] GitHub Actions CI/CD set up (optional)

## Merge Criteria

- [x] Repository clean and well-organized
- [x] .gitignore and LICENSE present
- [x] Project discoverable via work portfolio
- [x] All files properly tracked
- [x] Reviewed and approved

## Notes

Project is now ready for:
- Public use
- Distribution to other developers
- Long-term maintenance
- Portfolio demonstration

🚀 **Project complete and released!**
```

---

## General PR Guidelines

### Before Creating PR
- [ ] Create feature branch: `git checkout -b feature/name`
- [ ] Commit changes with clear messages
- [ ] Push branch: `git push -u origin feature/name`
- [ ] Verify all tests pass locally
- [ ] Check code quality (PEP 8, type hints, docstrings)

### PR Submission Checklist
- [ ] Title is concise and descriptive
- [ ] Description explains what changed and why
- [ ] Test plan is clear and reproducible
- [ ] Merge criteria are met
- [ ] All files are included (check `git diff main`)
- [ ] No hardcoded secrets or credentials

### After PR Created
- [ ] Request review from team
- [ ] Address any feedback or questions
- [ ] Run suggested tests or scenarios
- [ ] Ensure all CI checks pass (if applicable)
- [ ] Get approval before merging

### Merging
- [ ] Ensure all merge criteria are met
- [ ] Get at least one approval (self-review if solo)
- [ ] Merge using "Squash and merge" or "Create a merge commit"
- [ ] Delete feature branch after merge
- [ ] Verify main branch is clean

---

## Tips for Success

1. **Be Specific:** Include actual command outputs, error messages, examples
2. **Show Your Work:** Document what you tested and how
3. **Explain Why:** Help reviewers understand your design choices
4. **Keep It Clean:** One feature per PR; don't mix concerns
5. **Make It Easy:** Provide clear steps to reproduce and test

---

**Last Updated:** 2026-07-27  
**Template Version:** 1.0  
**Use this template for all Sales Agents implementation PRs**

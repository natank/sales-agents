# Sales Agents — Implementation Status Tracking

**Project:** Sales Agents Multi-Agent Cold Email Generator  
**Start Date:** 2026-07-27  
**Target Completion:** 2026-07-28  
**Total Estimated Hours:** 5-9 hours  

---

## Executive Summary

```
╔════════════════════════════════════════════════════════════════════╗
║                    IMPLEMENTATION PROGRESS                        ║
╠════════════════════════════════════════════════════════════════════╣
║  Phase 1: Core Implementation         [████████████████████] 100% ✅ ║
║  Phase 2: Testing & Validation        [████████████████████] 100% ✅ ║
║  Phase 3: Polish & Documentation      [████████████████████] 100% ✅ ║
║  Phase 4: Release & Deployment        [░░░░░░░░░░░░░░░░░░] 0%   📋  ║
╠════════════════════════════════════════════════════════════════════╣
║  Overall Progress:                    [███████████████░░░] ~75%  🚀  ║
║  Status: Phase 3 complete, Phase 4 next                           ║
╚════════════════════════════════════════════════════════════════════╝
```

**Merged PRs:**
- [PR #1 — project initiation](https://github.com/natank/sales-agents/pull/1): design docs, implementation plan, CI workflow
- [PR #2 — core implementation](https://github.com/natank/sales-agents/pull/2): `src/agents_def.py`, `src/utils.py`, `src/sales_agents.py`, unit tests
- [PR #3 — status update](https://github.com/natank/sales-agents/pull/3): Phase 1 completion status
- [PR #4 — model fix](https://github.com/natank/sales-agents/pull/4): `gpt-4-mini` → `gpt-5.4-mini`, first live end-to-end verification
- [PR #5 — Phase 2 complete](https://github.com/natank/sales-agents/pull/5): remaining live scenarios, traces, code quality, `docs/EXAMPLE-RUNS.md`
- [PR #6 — Phase 3 complete](https://github.com/natank/sales-agents/pull/6): README corrected against real, tested behavior

---

## PHASE 1: Core Implementation ✅ COMPLETE

**Goal:** Implement the three core source files  
**Status:** ✅ Complete — merged via [PR #2](https://github.com/natank/sales-agents/pull/2)  
**Duration:** ~1.5 hours actual (est. 2-3 hours)  
**Tasks:** 4/4 items complete  

### Task Breakdown

| # | Task | Status | Duration | Blocker | Notes |
|---|------|--------|----------|---------|-------|
| 1 | **1A: agents_def.py** | ✅ Done | ~40 min | — | 4 agents + orchestration functions |
| 2 | **1B: utils.py** | ✅ Done | ~25 min | #1 | Formatting, validation, helpers |
| 3 | **1C: sales_agents.py** | ✅ Done | ~25 min | #1,#2 | CLI entry point, workflow |
| 4 | **PR #1 Merge** | ✅ Done | — | #1,#2,#3 | Merged as PR #2 (repo PR numbering) |

### Phase 1 Checklist

**1A - agents_def.py:**
- [x] OpenAI Agents SDK imported (`from agents import Agent, Runner`)
- [x] Professional agent defined (system instructions)
- [x] Witty agent defined (system instructions)
- [x] Concise agent defined (system instructions)
- [x] Sales picker agent defined (system instructions)
- [x] `generate_email()` implemented using Runner.run()
- [x] `pick_best_email()` implemented using Runner.run(); parsing pulled into
      standalone `parse_picker_output()` for unit testability
- [x] Error handling added (wrapped in `RuntimeError` with context)
- [x] Type hints added
- [x] Docstrings added
- [x] Tested: imports work, all 4 agents instantiate with correct names
- [x] Code review: matches DESIGN.md § 2

**1B - utils.py:**
- [x] `validate_prospect_input()` implemented
- [x] `format_email_output()` implemented with dividers
- [x] `format_picker_output()` implemented
- [x] `get_prospect_input()` implemented with prompts
- [x] Error logging helpers implemented (`log_error`)
- [x] User-friendly error messages (`user_error_message`, maps auth/rate-limit/network)
- [x] Type hints added
- [x] Docstrings added
- [x] Visual formatting tested (looks clean)

**1C - sales_agents.py:**
- [x] `main()` function implemented
- [x] CLI input prompts working
- [x] `orchestrate_emails()` implemented (sequential, per-agent failure isolation)
- [x] `orchestrate_picker()` implemented
- [x] Input validation using utils
- [x] Error handling for API errors
- [x] Output formatting using utils
- [x] Type hints added
- [x] Docstrings added
- [ ] Tested: end-to-end run with a real `OPENAI_API_KEY` — **deferred to Phase 2**
      (no API key available in the implementation environment; import/smoke
      testing and 13 unit tests passed instead)

**PR #1 (Core Implementation):**
- [x] All 3 files complete and working
- [x] Branch created and pushed (`feature/core-implementation`)
- [x] PR created with comprehensive description (Summary/What Changed/Test Plan/Acceptance Criteria)
- [x] Code quality verified (ruff lint + format, both clean)
- [x] 13 unit tests added and passing (validation, formatting, picker parsing)
- [x] CI green (lint, format check, smoke-import, pytest)
- [x] PR merged to main (squash merge, branch deleted) — [PR #2](https://github.com/natank/sales-agents/pull/2)
- [ ] Manual testing with 1+ live scenario — **deferred to Phase 2** (no API key available)

**Deviations from plan:**
- `pyproject.toml` originally listed `openai` as the dependency; corrected to
  `openai-agents` (the actual Agents SDK package imported by the code). Fixed
  in this PR since it blocked any real usage.
- Live agent runs and OpenAI Traces dashboard verification were not possible
  in this environment (no `OPENAI_API_KEY`) and are carried into Phase 2's
  existing "manual testing" and "traces inspection" tasks rather than
  duplicated here.

---

## PHASE 2: Testing & Validation ✅ COMPLETE

**Goal:** Comprehensive testing with multiple scenarios and prompt iteration  
**Status:** ✅ Complete  
**Duration:** ~1 hour actual (est. 1-2 hours)  
**Tasks:** 5/5 items complete  

**Note on task numbering:** Scenario A (FinTech) and the initial traces check
were actually run first, as part of finding/fixing the `gpt-4-mini` model bug
(see the "fix: correct model name" PR and Phase 1 notes above) — that work is
credited to tasks #5/#6 here rather than duplicated.

### Task Breakdown

| # | Task | Status | Duration | Notes |
|---|------|--------|----------|-------|
| 5 | **2A: 3 Test Scenarios** | ✅ Done | ~20 min | FinTech, Creative, Enterprise — all pass |
| 6 | **2B: Traces Inspection** | ✅ Done | included above | 4 API calls + trace uploads per run, all successful |
| 7 | **2C: Code Quality** | ✅ Done | ~10 min | PEP 8, type hints, security — all clean |
| 8 | **2D: Prompt Iteration** | ✅ Done (no changes needed) | ~10 min | Reviewed all 3 runs; prompts performing well as-is |
| 9 | **PR #2 Merge** | ✅ Done | — | This PR |

### Phase 2 Checklist

**2A - Test Scenarios:**
- [x] **Scenario A (FinTech):**
  - [x] Prospect: Acme Financial, Finance, reconciliation delays
  - [x] Run full workflow (part of the model-name bug-fix PR)
  - [x] Verify 3 emails distinct — yes, clearly different tone/structure per persona
  - [x] Verify picker choice — **The Professional** (plan predicted Concise; picker's
        stated reasoning was coherent and scenario-specific, not an error — see
        "Findings" below)
  - [x] Check output formatting clean — yes, matches DESIGN.md § 6 spec exactly
  - [x] Document results — see docs/EXAMPLE-RUNS.md (Phase 3)
- [x] **Scenario B (Creative):**
  - [x] Prospect: DesignFlow Studios, Design/Marketing, cross-time-zone collaboration
  - [x] Run full workflow
  - [x] Verify 3 emails distinct — yes
  - [x] Verify picker choice — **The Concise** (plan predicted Witty; again, a
        defensible different call — see "Findings" below)
  - [x] Check output formatting clean — yes
  - [x] Document results
- [x] **Scenario C (Enterprise):**
  - [x] Prospect: Guardian Insurance Corp, Financial Services, compliance workflows
  - [x] Run full workflow
  - [x] Verify 3 emails distinct — yes
  - [x] Verify picker choice — **The Professional** (matches plan's prediction exactly)
  - [x] Check output formatting clean — yes
  - [x] Document results
- [x] Verify error handling (invalid input) — all-blank input rejected with
      `Invalid input: Missing required field(s): company, industry, pain_point,
      outcome`, no stack trace, exit code 1

**2B - Traces Inspection:**
- [x] Live runs confirmed 4/4 `POST /v1/responses` calls returned `200 OK` per
      scenario (12/12 across all 3 scenarios)
- [x] Trace uploads (`POST /v1/traces/ingest`) confirmed for every scenario —
      Scenarios A and B showed 4 upload batches, Scenario C showed 3 (the SDK
      batches multiple agent runs per upload; this is normal, not a dropped trace)
- [x] No errors in any trace-related request (all `204 No Content`)
- [x] Execution time reasonable — each 4-agent scenario completed well within
      the ~10-30s target
- [ ] Manual visual inspection of the OpenAI platform Traces dashboard UI —
      not done (API-level confirmation via HTTP status codes was used instead;
      dashboard is the same underlying data)

**2C - Code Quality:**
- [x] PEP 8 / lint: `ruff check src tests` — all checks passed
- [x] Format: `ruff format --check src tests` — all files formatted
- [x] Type hints on all functions verified — 13/13 functions have full
      parameter + return type hints
- [x] Docstrings present and clear — all 13 functions documented
- [x] No hardcoded secrets — verified via grep; `.env` confirmed gitignored
      and not tracked (`git ls-files` shows no `.env`)
- [x] No stack traces exposed — confirmed via live invalid-input test
- [x] No unused imports — `ruff check --select F401` clean
- [x] Error handling complete — all API/validation paths covered

**2D - Prompt Iteration:**
- [x] Reviewed email quality from all 3 live scenarios — all three personas
      (Professional/Witty/Concise) are clearly distinct, on-brief, and
      persuasive; no adjustments needed
- [x] Reviewed picker's reasoning on all 3 runs — coherent and
      scenario-specific every time, even where its pick diverged from the
      plan's a-priori prediction (see Findings below)
- [x] No prompt changes made — current prompts are performing as designed

**PR #2 (this PR):**
- [x] All 3 test scenarios pass
- [x] Traces confirmed (API-level; see 2B notes on dashboard-vs-API caveat)
- [x] Code quality verified
- [x] Test results documented (this file + docs/EXAMPLE-RUNS.md in Phase 3)
- [x] No prompt adjustments needed
- [x] CI green before merge

### Findings

**Picker predictions vs. actual (informational, not a defect):**

| Scenario | Plan's a-priori guess | Actual picker choice | Picker's stated reasoning |
|----------|----------------------|----------------------|----------------------------|
| A — FinTech | The Concise | **The Professional** | Regulated/financial buyer values credibility, compliance framing, and case-study-style trust signals over brevity |
| B — Creative | The Witty | **The Concise** | Clear value prop for the exact pain point (cross-time-zone workflow centralization) + strongest CTA; judged more likely to convert than humor for this specific ask |
| C — Enterprise | The Professional | **The Professional** | Matches |

The plan's predictions were intuition-based guesses written before any live
run existed; the picker agent's actual choices are its own judgment calls
based on the specific prospect context each time, with reasoning that holds
up on inspection in all three cases. This isn't a bug in the picker or the
email agents — it's a reminder that an LLM evaluator's judgment won't always
match a human's a-priori guess, which is itself a useful thing to know about
this system's behavior. No prompt changes made as a result.

---

## PHASE 3: Polish & Documentation ✅ COMPLETE

**Goal:** Update documentation with examples and ensure project is ready for use  
**Status:** ✅ Complete  
**Duration:** ~35 min actual (est. 1 hour)  
**Tasks:** 4/4 items complete  

**Note on sequencing:** 3B (`IMPLEMENTATION-CHECKLIST.md`) and 3C
(`EXAMPLE-RUNS.md`) were completed as part of [PR #5](https://github.com/natank/sales-agents/pull/5)
(Phase 2's PR) rather than here, since the real scenario output needed for
both was already in hand from that phase's live testing — writing it up
immediately avoided re-deriving it later. Only 3A (README) remained for this
phase's own PR.

### Task Breakdown

| # | Task | Status | Duration | Notes |
|---|------|--------|----------|-------|
| 10 | **3A: Update README** | ✅ Done | ~30 min | Real examples, troubleshooting, accurate claims |
| 11 | **3B: Update Checklist** | ✅ Done (in PR #5) | — | Completed early alongside Phase 2 |
| 12 | **3C: Create EXAMPLE-RUNS** | ✅ Done (in PR #5) | — | Completed early alongside Phase 2 |
| 13 | **PR #3 Merge** | ✅ Done | — | Merged as [PR #6](https://github.com/natank/sales-agents/pull/6) |

### Phase 3 Checklist

**3A - Update README.md:**
- [x] Add real example output from Scenario A — replaced fabricated
      placeholder text with actual live output
- [x] Add Troubleshooting section
  - [x] "Invalid API key" solution
  - [x] "Rate limit exceeded" solution
  - [x] "Email generation failed" solution
  - [x] "Model does not exist" solution (added — this was the real bug
        hit during Phase 2, not in the original plan template, but
        worth documenting since it actually happened)
- [x] Verify quick start commands work — ran fresh with
      `OPENAI_API_KEY` unset to confirm `.env` auto-load works exactly
      as documented
- [x] Add notes on model availability — corrected `gpt-4-mini` →
      `gpt-5.4-mini` throughout
- [x] Review formatting and links — project structure diagram updated
      to include `tests/` and `.github/`; doc links all point to
      files that exist

**3B - Update IMPLEMENTATION-CHECKLIST.md:** (done in PR #5)
- [x] Mark Phase 1 as ✅ COMPLETE
- [x] Mark Phase 2 as ✅ COMPLETE
- [x] Add notes on learnings from Phase 1 (dependency fix, deferred
      live testing)
- [x] Add notes on learnings from Phase 2 (model-name bug, picker
      findings)

**3C - Create docs/EXAMPLE-RUNS.md:** (done in PR #5)
- [x] Document Scenario A (FinTech) — input, 3 emails, analysis,
      picker choice + reasoning
- [x] Document Scenario B (Creative) — same
- [x] Document Scenario C (Enterprise) — same

**PR #3 (Phase 3's own PR, [#6](https://github.com/natank/sales-agents/pull/6)):**
- [x] README updated with real examples
- [x] Troubleshooting section helpful and tied to actual code paths
- [x] IMPLEMENTATION-CHECKLIST reflects actual work (via #5)
- [x] EXAMPLE-RUNS.md created with 3 scenarios (via #5)
- [x] No broken links or formatting issues
- [x] CI green before merge
- [x] PR merged to main

---

## PHASE 4: Release & Deployment

**Goal:** Prepare project for release and public use  
**Status:** 🔄 Ready to start — Phase 3 complete, this is next  
**Duration:** 1 hour (likely less — see note)  
**Tasks:** 4 items  

**Note:** the GitHub repository (`github.com/natank/sales-agents`, public,
with `.gitignore` and MIT `LICENSE`) was already created and pushed back
during project initiation, ahead of the original plan's Phase 4 sequencing —
so 4.1/4.2 from the original plan are effectively already done. What's
actually left is 4.3 (adding this project to the `work/` portfolio README)
and, optionally, branch protection rules on `main` to formally enforce the
PR Workflow Policy that's already been followed manually throughout.

### Task Breakdown

| # | Task | Status | Duration | Blocker | Notes |
|---|------|--------|----------|---------|-------|
| 14 | **4A: Git Repo Setup** | 📋 Pending | 0.3h | #13 | .gitignore, LICENSE, initial commit |
| 15 | **4B: Portfolio Update** | 📋 Pending | 0.2h | #13 | Add to work/README.md |
| 16 | **4C: GitHub Push** | 📋 Pending | 0.3h | #13 | Optional: push to GitHub, CI/CD |
| 17 | **PR #4 Merge** | 📋 Pending | — | #14,#15 | Release & deploy bundle |

### Phase 4 Checklist

**4A - Git Repo Setup:**
- [ ] Initialize git repo (if needed)
- [ ] Create .gitignore
  - [ ] `.env`
  - [ ] `__pycache__/`
  - [ ] `*.pyc`
  - [ ] `.venv/`
  - [ ] `.DS_Store`
  - [ ] `*.egg-info/`
  - [ ] `.pytest_cache/`
  - [ ] `.ruff_cache/`
- [ ] Create LICENSE file (MIT)
- [ ] Verify all files tracked: `git status`
- [ ] Create initial commit

**4B - Portfolio Update:**
- [ ] Edit /Users/nati-home/Projects/agents/work/README.md
- [ ] Add sales-agents section
  - [ ] Project name linked
  - [ ] Short description
  - [ ] Key demonstrations listed
  - [ ] Tech stack mentioned
  - [ ] Status: Complete
- [ ] Format matches existing projects (joke-agent)
- [ ] Verify links work

**4C - GitHub Push (optional):**
- [ ] Create GitHub repo (https://github.com/natank/sales-agents)
- [ ] Add remote: `git remote add origin ...`
- [ ] Push to GitHub: `git push -u origin main`
- [ ] Verify on GitHub
- [ ] Optional: Add badges to README
- [ ] Optional: Set up GitHub Actions

**PR #4:**
- [ ] Repository initialized and clean
- [ ] .gitignore and LICENSE present
- [ ] sales-agents added to work portfolio
- [ ] Links and formatting correct
- [ ] PR reviewed and approved
- [ ] PR merged to main
- [ ] Project complete and ready for use

---

## Overall Progress Dashboard

### By Phase

```
PHASE 1 (Core Implementation)
├─ 1A: agents_def.py .......... ⏳ Pending  
├─ 1B: utils.py ............... ⏳ Pending  
├─ 1C: sales_agents.py ........ ⏳ Pending  
└─ PR #1 ...................... ⏳ Pending  
   Subtotal: 0/4 complete (0%)

PHASE 2 (Testing & Validation)
├─ 2A: Test Scenarios ......... ⏳ Pending  
├─ 2B: Traces Inspection ...... ⏳ Pending  
├─ 2C: Code Quality ........... ⏳ Pending  
├─ 2D: Prompt Iteration ....... ⏳ Optional  
└─ PR #2 ...................... ⏳ Pending  
   Subtotal: 0/4 complete (0%)

PHASE 3 (Polish & Documentation)
├─ 3A: Update README .......... ⏳ Pending  
├─ 3B: Update Checklist ....... ⏳ Pending  
├─ 3C: Example Runs ........... ⏳ Pending  
└─ PR #3 ...................... ⏳ Pending  
   Subtotal: 0/4 complete (0%)

PHASE 4 (Release & Deployment)
├─ 4A: Git Repo Setup ......... ⏳ Pending  
├─ 4B: Portfolio Update ....... ⏳ Pending  
├─ 4C: GitHub Push ............ ⏳ Optional  
└─ PR #4 ...................... ⏳ Pending  
   Subtotal: 0/3 complete (0%)

TOTAL: 0/15 tasks complete (0%)
```

### PR Merge Status

```
PR #1: Core Implementation .............. ⏳ Pending (depends on 1A-1C)
PR #2: Testing & Validation ............. ⏳ Pending (depends on 2A-2C)
PR #3: Polish & Documentation ........... ⏳ Pending (depends on 3A-3C)
PR #4: Release & Deployment ............. ⏳ Pending (depends on 4A-4B)

Total PRs: 4 (0/4 merged, 100% pending)
```

---

## Time Tracking

### Estimated Hours by Phase

| Phase | Activity | Est. Hours | Actual | Status |
|-------|----------|-----------|--------|--------|
| 1 | agents_def.py | 1.0 | — | ⏳ |
| 1 | utils.py | 0.75 | — | ⏳ |
| 1 | sales_agents.py | 0.75 | — | ⏳ |
| 1 | **Phase 1 Total** | **2.5** | — | ⏳ |
| 2 | Test Scenarios | 0.75 | — | ⏳ |
| 2 | Traces & Code Quality | 1.0 | — | ⏳ |
| 2 | Prompt Iteration (opt) | 0.5 | — | ⏳ |
| 2 | **Phase 2 Total** | **2.25** | — | ⏳ |
| 3 | README & Checklist | 0.5 | — | ⏳ |
| 3 | Example Runs | 0.4 | — | ⏳ |
| 3 | **Phase 3 Total** | **0.9** | — | ⏳ |
| 4 | Repo & Portfolio | 0.5 | — | ⏳ |
| 4 | GitHub Push (opt) | 0.3 | — | ⏳ |
| 4 | **Phase 4 Total** | **0.8** | — | ⏳ |
| — | **PROJECT TOTAL** | **6.35** | — | ⏳ |

**Target Range:** 5-9 hours  
**Estimated:** 6.35 hours  
**Status:** Within target range ✅

---

## Daily Schedule

### Day 1 (Recommended: 2026-07-27 or morning of 2026-07-28)

```
MORNING SESSION (2-3 hours)
├─ Phase 1A: agents_def.py .......... 1.0-1.5h
├─ Phase 1B: utils.py ............... 0.75h
└─ Phase 1C: sales_agents.py ........ 0.75h
Subtotal: 2.5h

AFTERNOON SESSION (1-2 hours)
├─ Phase 2A: Manual testing (3 scenarios) ... 0.75h
├─ Phase 2B: Traces inspection ........... 0.5h
└─ Phase 2C: Code quality checks ......... 0.5h
Subtotal: 1.75h

END OF DAY 1: Phases 1 & 2 complete (PR #1 & PR #2)
```

### Day 2 (Recommended: 2026-07-28 or afternoon of 2026-07-27)

```
MORNING SESSION (1 hour)
├─ Phase 3A: README update ......... 0.3h
├─ Phase 3B: Checklist update ..... 0.2h
└─ Phase 3C: Example Runs ......... 0.4h
Subtotal: 0.9h

AFTERNOON SESSION (1 hour)
├─ Phase 4A: Git repo setup ....... 0.3h
├─ Phase 4B: Portfolio update ..... 0.2h
└─ Phase 4C: GitHub push (opt) .... 0.3h
Subtotal: 0.8h

END OF DAY 2: Phases 3 & 4 complete (PR #3 & PR #4)
PROJECT COMPLETE ✅
```

---

## Risk Mitigation

| Risk | Impact | Mitigation | Status |
|------|--------|-----------|--------|
| API errors during testing | Phase 2 delays | Retry logic, check rate limits | ✅ Planned |
| Poor email quality | Phase 3 delays | Prompt iteration (optional task) | ✅ Built-in |
| Traces not visible | Phase 2 blocker | Check auth, project settings | ✅ Planned |
| Scope creep | Timeline risk | Stick to MVP scope, document changes | ✅ Defined |
| Documentation outdated | Maintainability | Update docs after each PR | ✅ Planned |

---

## Success Criteria

**Global Success:**
- ✅ All 4 phases complete
- ✅ All 4 PRs merged successfully
- ✅ System works end-to-end with 3+ scenarios
- ✅ Code quality high (PEP 8, type hints, docstrings)
- ✅ Documentation comprehensive
- ✅ Project ready for public use

**Phase-Specific Success:**
- Phase 1: ✅ 3 source files implemented, functional
- Phase 2: ✅ Testing complete, quality verified, traces visible
- Phase 3: ✅ Documentation updated, examples real and helpful
- Phase 4: ✅ Repository clean, project discoverable, released

---

## Notes & Updates

### Session 1 Notes (2026-07-27)

- Project initiation merged as [PR #1](https://github.com/natank/sales-agents/pull/1):
  design docs, `docs/IMPLEMENTATION-PLAN.md` (including the PR Workflow Policy
  — feature branches only, comprehensive PR descriptions, CI-gated merges),
  and `.github/workflows/ci.yml`.
  - First CI run on that PR failed: `ruff format --check .` was reformatting
    Python code fences inside `docs/DESIGN.md` as if they were real source.
    Fixed by scoping ruff to `src`/`tests` only, both in CI args and
    `[tool.ruff] src = [...]` in `pyproject.toml`.
- Phase 1 (core implementation) merged as [PR #2](https://github.com/natank/sales-agents/pull/2):
  `src/agents_def.py`, `src/utils.py`, `src/sales_agents.py`, plus 13 unit
  tests. CI green on first attempt.
  - Found and fixed a dependency bug: `pyproject.toml` declared `openai` but
    the design (and the actual code) needs the Agents SDK package,
    `openai-agents`. Corrected before merge.
  - No `OPENAI_API_KEY` was available in the implementation environment, so
    live agent runs and OpenAI Traces dashboard checks were not performed.
    Verified everything short of that: imports, lint, format, and unit tests
    for all pure-logic paths (validation, formatting, picker-output parsing).
    Live testing rolls into Phase 2 as originally scoped.

### Session 2 Notes (2026-07-27)

- A `.env` file with a real `OPENAI_API_KEY` was added locally (not committed
  — `.gitignore` already excludes it), enabling the first live testing of the
  app.
- First live run immediately surfaced a real bug: `model="gpt-4-mini"` (from
  `docs/DESIGN.md`, implemented as-is in Phase 1) returned a 400
  `model_not_found` — that model doesn't exist. Listed models against the
  live key, found `gpt-5.4-mini` (same one `joke-agent` already uses), fixed
  it via a `MODEL` constant, corrected `DESIGN.md`'s two references, and
  merged as [PR #4](https://github.com/natank/sales-agents/pull/4) with the
  live-test evidence attached.
- With the model fixed, ran the remaining 2 Phase 2 scenarios (Creative,
  Enterprise) plus an invalid-input error-handling check, all live. All 3
  scenarios passed; see the Findings table in the Phase 2 section above for
  the one interesting result — the picker's actual choices differed from the
  plan's a-priori predictions on 2 of 3 scenarios, with sound reasoning in
  every case. Treated as a finding, not a defect; no prompt changes made.
- Code quality pass (2C) confirmed clean: lint, format, type hints (13/13
  functions), docstrings (13/13), no hardcoded secrets, no unused imports.
- Merged as PR #5, closing out Phase 2.
- Phase 3: found the README was written entirely before any code existed and
  had drifted — fabricated example output, undocumented/wrong CLI usage
  (`--company` flags that don't exist), `gpt-4-mini` still referenced, no
  troubleshooting section, and an observability claim ("visible in the
  dashboard") that was never actually verified against the UI. Rewrote it
  against what was actually built and tested, verified the quick-start
  commands fresh (unset `OPENAI_API_KEY`, confirmed `.env` auto-load works).
  Merged as PR #6.
- This status update merged as PR #7, closing out Phase 3.

---

## Sign-Off

**Plan Created By:** Claude Code  
**Date:** 2026-07-27  
**Version:** 1.0  
**Status:** Ready for Implementation  

**Approval Required:** User sign-off before starting Phase 1

---

## Quick Reference

**Start Phase 1:** `cd /Users/nati-home/Projects/agents/work/sales-agents && git checkout -b feature/core-implementation`

**Track Progress:** Review this file daily  
**Report Issues:** Update relevant task status  
**Merge PRs:** Follow merge criteria in each phase section

**Questions?**
- Architecture → See IMPLEMENTATION-PLAN.md
- Requirements → See docs/REQUIREMENTS.md
- Design → See docs/DESIGN.md

---

**Last Updated:** 2026-07-27  
**Next Review:** Start of Phase 1 implementation

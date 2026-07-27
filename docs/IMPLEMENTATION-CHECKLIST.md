# Implementation Checklist

This checklist tracks the implementation of the Sales Agents project from design to launch.

## Phase 1: Core Implementation ✅ COMPLETE (merged [PR #2](https://github.com/natank/sales-agents/pull/2))

- [x] **src/agents_def.py** — Agent definitions
  - [x] Import OpenAI Agents SDK classes (`Agent`, `Runner`)
  - [x] Define `professional_agent` with system instructions
  - [x] Define `witty_agent` with system instructions
  - [x] Define `concise_agent` with system instructions
  - [x] Define `sales_picker_agent` with system instructions
  - [x] Implement `generate_email(agent, prospect_context) → str`
  - [x] Implement `pick_best_email(emails, prospect_context) → (str, str)`
        (parsing extracted into standalone `parse_picker_output()`, unit tested)

- [x] **src/utils.py** — Utility functions
  - [x] Implement `validate_prospect_input(company, industry, pain_point, outcome) → bool`
  - [x] Implement `format_email_output(agent_name, persona, email_text) → str`
  - [x] Implement `format_picker_output(chosen_agent, reasoning) → str`
  - [x] Implement error logging / user-friendly error messages
  - [x] Implement input prompts for CLI

- [x] **src/sales_agents.py** — Main CLI entry point
  - [x] Import dependencies and local modules
  - [x] Implement `main()` function
  - [x] Implement CLI argument parsing (or interactive prompts)
  - [x] Implement `orchestrate_emails(prospect_context) → dict`
  - [x] Implement `orchestrate_picker(emails, prospect_context) → (str, str)`
  - [x] Implement main workflow:
    1. Collect prospect input
    2. Generate emails
    3. Print emails
    4. Run picker
    5. Print picker result
  - [x] Error handling and graceful fallbacks

**Notes:**
- `pyproject.toml` had the wrong dependency (`openai` instead of `openai-agents`) — fixed in this phase.
- 13 unit tests added (`tests/test_agents_def.py`, `tests/test_utils.py`) covering all pure-logic paths.
- Live agent runs and OpenAI Traces verification were not possible (no `OPENAI_API_KEY` in the implementation environment) — carried into Phase 2's existing scope, not a new task.

## Phase 2: Testing & Validation ✅ COMPLETE (merged [PR #4](https://github.com/natank/sales-agents/pull/4), [PR #5](https://github.com/natank/sales-agents/pull/5))

- [x] **Manual Testing** — 3 live scenarios run against a real `OPENAI_API_KEY`
  - [x] Run with sample prospect scenario (FinTech: Acme Financial)
  - [x] Run Creative scenario (DesignFlow Studios)
  - [x] Run Enterprise scenario (Guardian Insurance Corp)
  - [x] Verify three emails are generated and distinct — confirmed all 3 runs
  - [x] Verify picker selects one email with reasoning — confirmed all 3 runs
        (picker's actual choices differed from the plan's a-priori guesses on
        2/3 scenarios; reasoning was sound in every case — see
        `docs/STATUS-TRACKING.md` Phase 2 "Findings")
  - [x] Check output formatting is clean and readable — matches DESIGN.md § 6
  - [x] Verify error handling (invalid input) — blank input rejected cleanly,
        no stack trace, exit code 1
  - [x] Verify error handling (API errors) — surfaced for real during initial
        testing: `gpt-4-mini` doesn't exist, returned a proper user-facing
        error, not a crash; root cause then fixed (see below)

- [x] **Trace Visibility**
  - [x] Confirmed via API responses: `POST /v1/traces/ingest` returns
        `204 No Content` for every agent run across all 3 scenarios
  - [x] All agent runs produce successful trace uploads (12/12 email+picker
        calls across the 3 scenarios all returned `200 OK`)
  - [ ] Manual visual walkthrough of the OpenAI platform Traces dashboard UI —
        not done; API-level confirmation was used instead (same underlying data)

- [x] **Code Quality**
  - [x] PEP 8 compliance (`ruff check` + `ruff format --check`) — clean
  - [x] Type hints on all functions — 13/13
  - [x] Docstrings on all public functions — 13/13
  - [x] No hardcoded secrets (`.env` gitignored and untracked, verified)

**Bug found and fixed during this phase:** `docs/DESIGN.md` specified
`model="gpt-4-mini"`, which Phase 1 implemented as-is (no API key was
available then to catch it). First live run failed immediately with a 400.
Fixed to `gpt-5.4-mini` via a `MODEL` constant in `agents_def.py`; see
[PR #4](https://github.com/natank/sales-agents/pull/4).

## Phase 3: Documentation & Polish ✅ COMPLETE (merged [PR #5](https://github.com/natank/sales-agents/pull/5), [PR #6](https://github.com/natank/sales-agents/pull/6))

- [x] **README Updates**
  - [x] Verify quick start instructions work end-to-end — re-ran fresh with
        `OPENAI_API_KEY` unset to confirm `.env` auto-load matches what's
        documented
  - [x] Update example output with real run results — replaced fabricated
        placeholder text with the actual Scenario A output
  - [x] Add troubleshooting section — covers auth, rate limit, per-agent
        failure, and model-not-found (the last one wasn't in the original
        plan template, added because it's what actually happened)

- [x] **Design Documentation**
  - [x] Capture any deviations from design doc in DESIGN.md — done directly
        in [PR #4](https://github.com/natank/sales-agents/pull/4) when the
        `gpt-4-mini` → `gpt-5.4-mini` fix was made, not deferred to this phase
  - [x] Persona descriptions already matched the final prompts (no drift
        found on review)
  - [x] Error cases discovered during testing documented in
        `docs/STATUS-TRACKING.md` Phase 2 and in the README's new
        Troubleshooting section

- [x] **Example Scenarios**
  - [x] Created `docs/EXAMPLE-RUNS.md` with all 3 sample runs (done in PR #5,
        pulled forward from this phase since the real data was already
        captured during Phase 2 testing)
  - [x] Includes prospect context, generated emails, and picker choice for
        each scenario
  - [x] Documents the picker's reasoning for each scenario, plus a summary
        table comparing actual choices against the plan's original
        (pre-testing) predictions

## Phase 4: Deployment & Distribution

- [ ] **Repository Setup**
  - [ ] Initialize git repo (if standalone)
  - [ ] Create .gitignore (exclude .env, __pycache__, .venv)
  - [ ] Add LICENSE file
  - [ ] Create initial commit

- [ ] **CI/CD (Optional)**
  - [ ] Add GitHub Actions workflow for linting / type checking
  - [ ] Test against Python 3.12+

- [ ] **Publishing (Optional)**
  - [ ] Push to GitHub
  - [ ] Update work/README.md to reference sales-agents project
  - [ ] Add project to portfolio

## Implementation Notes

### Agent Prompt Tuning
Expect to iterate on system instructions:
- **Professional:** Adjust emphasis on ROI vs. compliance vs. case studies based on output quality
- **Witty:** Dial humor up/down; ensure it remains professional and inoffensive
- **Concise:** Experiment with bullet-point count, subject line phrasing, CTA specificity
- **Picker:** Clarify ranking criteria if picker is making unexpected choices

### Common Pitfalls to Avoid
- ❌ Hardcoding API key in code (always use environment variables)
- ❌ Ignoring rate limits (use sequential execution for MVP; handle 429 errors gracefully)
- ❌ Unhandled exceptions (always wrap API calls in try/except)
- ❌ Poor output formatting (use dividers, headers, whitespace liberally)
- ❌ Silent failures (log errors for debugging; show user-friendly messages)

### Testing Strategy
- **Manual:** Run with 3-4 different prospect scenarios; review output quality
- **Automated (Future):** Unit tests for utils, integration tests with mock API
- **Observability:** Check OpenAI Traces dashboard for every run

### Rate Limiting Considerations
- OpenAI applies per-minute token limits
- For MVP, use sequential execution (3 agents + 1 picker = 4 API calls)
- If hitting rate limits, add exponential backoff retry logic
- Future: Batch API calls or use async execution

## Success Criteria (Acceptance Tests)

### CR1: Three Emails Generated
```
Given a prospect scenario
When the app runs
Then three distinct emails are printed, each labeled with agent name and persona
And each email includes subject line and body
```

### CR2: Picker Selects Best Email
```
Given three emails
When the picker runs
Then it outputs one selected agent name and a 1-2 sentence reasoning
And the reasoning is coherent and aligned with prospect context
```

### CR3: Error Handling Works
```
Given invalid API key
When the app runs
Then a user-friendly error message is shown (not a stack trace)
```

### CR4: Traces Appear in Dashboard
```
Given a successful app run
When checking OpenAI platform Traces
Then all 4 agent runs (3 emails + 1 picker) appear as separate traces
And each trace shows the model name, input, and output
```

## Estimated Effort

- **agents_def.py:** 1-2 hours (agent definitions, LLM calls)
- **utils.py:** 1 hour (formatting, validation)
- **sales_agents.py:** 1-2 hours (CLI, orchestration, error handling)
- **Testing & validation:** 1-2 hours (manual testing, trace inspection, iteration)
- **Polish & documentation:** 1 hour (README examples, code quality)

**Total Estimate:** 5-9 hours (includes iteration and debugging)

---

**Last Updated:** 2026-07-27  
**Status:** Ready for implementation phase

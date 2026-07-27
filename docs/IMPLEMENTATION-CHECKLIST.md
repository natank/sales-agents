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

## Phase 2: Testing & Validation

- [ ] **Manual Testing**
  - [ ] Run with sample prospect scenario (e.g., FinTech company)
  - [ ] Verify three emails are generated and distinct
  - [ ] Verify picker selects one email with reasoning
  - [ ] Check output formatting is clean and readable
  - [ ] Verify error handling (invalid input, API errors)

- [ ] **Trace Visibility**
  - [ ] Log into OpenAI platform (platform.openai.com)
  - [ ] Navigate to Traces dashboard
  - [ ] Verify all agent runs appear as traces
  - [ ] Inspect trace details (input, model, output)

- [ ] **Code Quality**
  - [ ] PEP 8 compliance (run `black` or `ruff format`)
  - [ ] Type hints on all functions
  - [ ] Docstrings on all public functions
  - [ ] No hardcoded secrets (use environment variables)

## Phase 3: Documentation & Polish

- [ ] **README Updates**
  - [ ] Verify quick start instructions work end-to-end
  - [ ] Update example output with real run results
  - [ ] Add troubleshooting section if needed

- [ ] **Design Documentation**
  - [ ] Capture any deviations from design doc in DESIGN.md
  - [ ] Update agent persona descriptions with final prompts
  - [ ] Document any error cases discovered during testing

- [ ] **Example Scenarios**
  - [ ] Create example.md with 2-3 sample runs
  - [ ] Include prospect context, generated emails, and picker choice
  - [ ] Document reasoning behind picker's selection

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

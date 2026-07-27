# Sales Agents — Multi-Agent Cold Email Generator

A command-line application that demonstrates multi-agent LLM orchestration using the **OpenAI Agents SDK**. The system generates three distinct cold sales emails (from different personas), then uses an expert "sales picker" agent to recommend the best one for a given prospect scenario.

## Demonstrates

- **Multi-agent orchestration** — coordinating independent agents with distinct personas
- **LLM decision-making** — using an expert agent as a ranking/evaluation layer
- **Prompt engineering** — crafting distinct, coherent agent personas via system instructions
- **Automatic tracing** — all agent runs captured in OpenAI platform Traces dashboard
- **Error handling** — graceful fallbacks and user-friendly error messages
- **CLI design** — clean command-line interface for input and output

## Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager
- OpenAI API key (set as `OPENAI_API_KEY` environment variable or in a `.env` file)

### Setup

```bash
# Navigate to the project directory
cd /path/to/agents/work/sales-agents

# Install dependencies via uv
uv sync

# Set up your OpenAI API key (if not already set globally)
export OPENAI_API_KEY="sk-..."
```

### Run

```bash
uv run python src/sales_agents.py
```

The app prompts interactively for the four prospect fields (company name,
industry, pain point, desired outcome) — there are no CLI flags in this MVP.

## Example Usage

This is real output from a live run (see `docs/EXAMPLE-RUNS.md` for the full
text of all three emails and two more scenarios):

```
$ uv run python src/sales_agents.py

Enter prospect details:

Company name: Acme Financial
Industry: Finance
Pain point: Manual reconciliation of payment records
Desired outcome: Automate reconciliation to save 8 hours/week

=== GENERATED SALES EMAILS ===

═══════════════════════════════════════════════════════════════
AGENT: The Professional
PERSONA: Formal, credentials-focused, B2B expert
═══════════════════════════════════════════════════════════════

Subject: Reducing Manual Reconciliation Time at Acme Financial

Dear Acme Financial Team,

Manual reconciliation of payment records continues to consume valuable
finance team time and increases the risk of avoidable errors...

[The Witty and The Concise emails follow, each with a distinct tone —
see docs/EXAMPLE-RUNS.md for the full text]

═══════════════════════════════════════════════════════════════
SALES PICKER RECOMMENDATION
═══════════════════════════════════════════════════════════════

Best Email: The Professional

Reasoning: It best fits the finance industry and the seriousness of Acme
Financial's pain point, which increases credibility and trust. It clearly
connects automation to compliance, accuracy, and the promised 8+ hours
saved, with a persuasive CTA that feels appropriate for a regulated
financial buyer.
```

## Troubleshooting

**"Invalid API key" / `openai.AuthenticationError`**
Ensure `OPENAI_API_KEY` is set correctly — either exported in your shell or
in a `.env` file in the project root (loaded automatically via
`python-dotenv`). The key must have access to the `gpt-5.4-mini` model.

**"Rate limit reached. Please retry in a moment."**
The OpenAI API is rate-limiting your key. Wait and retry — the app runs the
three email agents sequentially rather than in parallel specifically to
reduce how often this happens.

**"[agent_key] email generation failed"**
One of the three email agents hit an error (shown above this message). The
other agents still run — the app degrades gracefully rather than aborting
the whole request. If all three fail, the app exits with a non-zero code and
skips the picker (nothing to rank).

**"The requested model '...' does not exist"**
The model name in `src/agents_def.py` (`MODEL` constant) isn't available to
your API key. `gpt-5.4-mini` is confirmed working as of this writing; if
OpenAI retires it, update the constant to a current equivalent.

## Project Structure

```
sales-agents/
├── README.md                    # This file
├── .github/workflows/ci.yml     # Lint, format check, smoke-import, pytest
├── src/
│   ├── sales_agents.py          # Main CLI entry point
│   ├── agents_def.py            # Agent definitions and orchestration
│   └── utils.py                 # Utility functions (formatting, validation)
├── tests/
│   ├── test_agents_def.py       # Unit tests for picker-output parsing
│   └── test_utils.py            # Unit tests for validation/formatting
├── docs/
│   ├── OPERATIONAL-CONCEPT.md   # Use case, problem statement, system flow
│   ├── REQUIREMENTS.md          # Functional and non-functional requirements
│   ├── DESIGN.md                # Architecture, agent definitions, data flow
│   └── EXAMPLE-RUNS.md          # Real output from 3 live test scenarios
└── pyproject.toml               # Project dependencies (uv)
```

## Documentation

All documentation is in the `docs/` folder:

- **[OPERATIONAL-CONCEPT.md](docs/OPERATIONAL-CONCEPT.md)** — What problem does this solve? What is the user flow?
- **[REQUIREMENTS.md](docs/REQUIREMENTS.md)** — Detailed functional (FR) and non-functional (NFR) requirements, user stories, assumptions.
- **[DESIGN.md](docs/DESIGN.md)** — Architecture, component descriptions, agent persona definitions, execution flow, output format spec.
- **[EXAMPLE-RUNS.md](docs/EXAMPLE-RUNS.md)** — Real, unedited output from 3 live test scenarios (FinTech, Creative, Enterprise), including the sales picker's actual reasoning.

**Implementation Planning:**
- **[IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md)** — Detailed 4-phase roadmap with PRs and merge criteria
- **[STATUS-TRACKING.md](docs/STATUS-TRACKING.md)** — Progress dashboard, phase-by-phase status, and notes on what was learned during implementation
- **[READY-TO-START.md](docs/READY-TO-START.md)** — Quick start guide for developers
- **[PR-TEMPLATE.md](docs/PR-TEMPLATE.md)** — Ready-to-use PR descriptions

## Tech Stack

- **Language:** Python 3.12+
- **LLM Framework:** OpenAI Agents SDK (`openai-agents`)
- **LLM Model:** `gpt-5.4-mini` (set via the `MODEL` constant in `src/agents_def.py`)
- **API:** OpenAI API
- **Package Manager:** `uv`
- **CI:** GitHub Actions — `ruff check`, `ruff format --check`, a smoke-import of all `src/` modules, and `pytest`, on every PR and push to `main`

## Key Concepts

### Three Sales Agent Personas

1. **"The Professional"** — Formal, corporate, ROI-focused. Emphasizes credentials, compliance, case studies.
2. **"The Witty"** — Clever, conversational, personality-driven. Uses humor and relatability to cut through clutter.
3. **"The Concise"** — Direct, scannable, data-driven. Bullet points and minimal words; respects busy inboxes.

### Sales Picker Agent

A fourth agent that reviews all three emails and selects the most compelling option for the given prospect scenario. Provides a brief rationale for its choice.

### Observability

All agent runs (3 email generators + 1 picker) are automatically traced via
the OpenAI Agents SDK — every run sends the trace to the OpenAI platform,
with no extra instrumentation needed:
- Navigate to [platform.openai.com → Traces](https://platform.openai.com/traces)
- View each agent's input, model call, and output
- Useful for debugging, auditing, and iterating on prompts

Verified during Phase 2 testing: every agent call's `POST /v1/traces/ingest`
request returned a successful `204 No Content` across all 3 test scenarios
(see `docs/EXAMPLE-RUNS.md`). This was confirmed at the API/HTTP level rather
than by visually checking the dashboard UI, since both report the same
underlying data.

## Error Handling

- **Invalid input:** Clear usage messages; exit gracefully.
- **OpenAI API errors:** User-friendly messages (e.g., "Invalid API key", "Rate limit exceeded").
- **Agent failures:** Graceful degradation; continue with other agents if one fails.
- **No stack traces** shown to end users; errors logged for debugging.

## Limitations & Future Enhancements

### MVP Scope
- No external tools or APIs (purely LLM-based).
- No email delivery integration.
- No A/B testing or conversion tracking.
- No persistent storage.

### Future Enhancements
- Prospect research tool (look up company info, funding, recent news).
- Email validation tool (grammar, tone, length checks).
- Parallel agent execution (current: sequential to avoid rate limits).
- Web UI for easier input and output display.
- Email delivery integration (SMTP, Mailgun, etc.).
- Persistent database of generated emails and picker decisions.

## Contributing

To extend or modify the system:

1. **Edit agent personas:** `src/agents_def.py` — update system instructions.
2. **Add new agents:** Define new `Agent` instances in `agents_def.py`, then update the orchestration in `sales_agents.py`.
3. **Add tools:** Define `@function_tool` decorated functions in a new `src/tools.py`, then pass them to agents.
4. **Update requirements:** Edit `docs/REQUIREMENTS.md` and `docs/DESIGN.md`.

## References

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python) (reference implementation)
- [OpenAI Platform — Traces Dashboard](https://platform.openai.com/traces)
- [Joke Agent Project](../joke-agent/) — similar orchestration pattern for reference

## License

This project is part of the Anthropic [Claude Code](https://claude.ai/code) portfolio demonstration. Use freely for learning and experimentation.

---

**Project Status:** Phases 1 & 2 complete (core implementation, live-tested against a real API key). Phase 3 (documentation polish) in progress; Phase 4 (release/deployment) not started.
**Last Updated:** 2026-07-27
**Repository:** [github.com/natank/sales-agents](https://github.com/natank/sales-agents)

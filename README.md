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
# Run the app with interactive prompts
uv run python src/sales_agents.py

# Or pass arguments directly (future enhancement)
uv run python src/sales_agents.py \
  --company "TechStartup Inc." \
  --industry "FinTech" \
  --pain-point "Manual data reconciliation between payment systems" \
  --outcome "Automate reconciliation to reduce errors and save 10 hours/week"
```

## Example Usage

```
$ uv run python src/sales_agents.py

Enter prospect company name: Acme Financial
Enter prospect industry: Finance
Enter prospect pain point: Manual reconciliation of payment records
Enter desired outcome: Automate reconciliation to save 8 hours/week

=== GENERATED SALES EMAILS ===

═══════════════════════════════════════════════════════════════
AGENT: The Professional
PERSONA: Formal, credentials-focused, B2B expert
═══════════════════════════════════════════════════════════════

Subject: TechFlow's Proven Reconciliation Automation for Financial Services

Dear Prospect,

[Professional email emphasizing ROI, compliance, case studies...]

───────────────────────────────────────────────────────────────

[Two more emails from "The Witty" and "The Concise" follow...]

═══════════════════════════════════════════════════════════════
SALES PICKER RECOMMENDATION
═══════════════════════════════════════════════════════════════

Best Email: The Concise

Reasoning: Finance buyers value time efficiency and clear ROI. The Concise email's
bullet-point format and focus on quantifiable time savings will resonate strongly
with busy operations managers.

───────────────────────────────────────────────────────────────
```

## Project Structure

```
sales-agents/
├── README.md                    # This file
├── src/
│   ├── sales_agents.py          # Main CLI entry point
│   ├── agents_def.py            # Agent definitions and orchestration
│   └── utils.py                 # Utility functions (formatting, validation)
├── docs/
│   ├── OPERATIONAL-CONCEPT.md   # Use case, problem statement, system flow
│   ├── REQUIREMENTS.md          # Functional and non-functional requirements
│   └── DESIGN.md                # Architecture, agent definitions, data flow
└── pyproject.toml               # Project dependencies (uv)
```

## Documentation

All documentation is in the `docs/` folder:

- **[OPERATIONAL-CONCEPT.md](docs/OPERATIONAL-CONCEPT.md)** — What problem does this solve? What is the user flow?
- **[REQUIREMENTS.md](docs/REQUIREMENTS.md)** — Detailed functional (FR) and non-functional (NFR) requirements, user stories, assumptions.
- **[DESIGN.md](docs/DESIGN.md)** — Architecture, component descriptions, agent persona definitions, execution flow, output format spec.

**Implementation Planning:**
- **[IMPLEMENTATION-PLAN.md](docs/IMPLEMENTATION-PLAN.md)** — Detailed 4-phase roadmap with PRs and merge criteria
- **[STATUS-TRACKING.md](docs/STATUS-TRACKING.md)** — Progress dashboard with 17 tracked tasks
- **[READY-TO-START.md](docs/READY-TO-START.md)** — Quick start guide for developers
- **[PR-TEMPLATE.md](docs/PR-TEMPLATE.md)** — Ready-to-use PR descriptions

## Tech Stack

- **Language:** Python 3.12+
- **LLM Framework:** OpenAI Agents SDK (`openai-agents`)
- **LLM Model:** `gpt-4-mini` (or latest equivalent)
- **API:** OpenAI API
- **Package Manager:** `uv`

## Key Concepts

### Three Sales Agent Personas

1. **"The Professional"** — Formal, corporate, ROI-focused. Emphasizes credentials, compliance, case studies.
2. **"The Witty"** — Clever, conversational, personality-driven. Uses humor and relatability to cut through clutter.
3. **"The Concise"** — Direct, scannable, data-driven. Bullet points and minimal words; respects busy inboxes.

### Sales Picker Agent

A fourth agent that reviews all three emails and selects the most compelling option for the given prospect scenario. Provides a brief rationale for its choice.

### Observability

All agent runs (3 email generators + 1 picker) are automatically traced via the OpenAI Agents SDK and visible in the OpenAI platform Traces dashboard:
- Navigate to [platform.openai.com → Traces](https://platform.openai.com/traces)
- View each agent's input, model call, and output
- Useful for debugging, auditing, and iterating on prompts

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

**Project Status:** MVP complete (documentation and design phase)  
**Last Updated:** 2026-07-27  
**Next Steps:** Implementation of `src/sales_agents.py`, `src/agents_def.py`, and `src/utils.py`

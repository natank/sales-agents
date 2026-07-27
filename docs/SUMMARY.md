# Sales Agents — Project Summary

## At a Glance

**Sales Agents** is a multi-agent LLM orchestration system that generates diverse cold sales emails and ranks them by conversion likelihood.

**Key Innovation:** Instead of a single email template, this system deploys three independent sales agents—each with a distinct persona and style—to generate parallel options. Then an expert "sales picker" agent evaluates all three and recommends the best fit for the prospect.

## Problem & Solution

### Problem
- Cold outreach templates are one-size-fits-all and often ineffective.
- Sales teams have different styles and approaches; a monolithic email wastes that diversity.
- Manually authoring multiple email variants is time-consuming.

### Solution
- **Automated multi-variant generation:** Three LLM agents produce emails in parallel (Professional, Witty, Concise).
- **Intelligent selection:** A fourth agent ranks them, providing a data-backed recommendation.
- **Observable & debuggable:** All runs traced in OpenAI platform dashboard for transparency and iteration.

## System Architecture

```
Prospect Input
 ↓
┌──────────────────────┐
│ Email Generators     │
├──────────────────────┤
│ • The Professional   │ → Email 1
│ • The Witty          │ → Email 2
│ • The Concise        │ → Email 3
└──────────────────────┘
 ↓
┌──────────────────────┐
│ Sales Picker Agent   │ → Best Email + Reasoning
└──────────────────────┘
 ↓
Output (emails + recommendation)
```

## Personas

| Agent | Style | Tone | Focus |
|-------|-------|------|-------|
| **The Professional** | Formal, corporate | Authoritative, trustworthy | ROI, credentials, risk mitigation |
| **The Witty** | Clever, conversational | Warm, approachable | Humor, relatability, emotional connection |
| **The Concise** | Direct, scannable | Efficient, punchy | Value prop, bullet points, time-respect |

## Documentation Map

| Document | Purpose |
|----------|---------|
| **[README.md](../README.md)** | Quick start, usage, tech stack, project structure |
| **[OPERATIONAL-CONCEPT.md](OPERATIONAL-CONCEPT.md)** | Use case, problem statement, system flow, fictional context |
| **[REQUIREMENTS.md](REQUIREMENTS.md)** | Functional (FR) & non-functional (NFR) requirements, user stories, assumptions |
| **[DESIGN.md](DESIGN.md)** | Architecture, agent definitions, execution flow, output format spec, error handling |

## Key Features

✅ **Multi-agent orchestration** — Parallel/sequential execution of independent agents
✅ **Distinct personas** — Each agent has a unique system prompt and style guide
✅ **Expert ranking** — A fourth agent selects the best email with reasoning
✅ **OpenAI Traces integration** — Automatic visibility into all agent runs
✅ **Graceful error handling** — User-friendly messages, no stack traces
✅ **CLI interface** — Simple input prompts, formatted output
✅ **Tool-free MVP** — Pure LLM reasoning, no external tools

## Tech Stack

- **Language:** Python 3.12+
- **Framework:** OpenAI Agents SDK
- **Model:** gpt-4-mini
- **Package Manager:** uv
- **Observability:** OpenAI platform Traces dashboard

## Success Criteria

1. **Output Quality** — Three emails are distinct, persuasive, and ready-to-send.
2. **Picker Accuracy** — Sales picker's choice aligns with expected "best email" for scenario.
3. **Clarity** — Output is easy to read and clearly labels each email.
4. **Observability** — All runs appear in OpenAI Traces dashboard.

## Scope

### Included (MVP)
- Three email-generation agents with distinct personas
- Sales picker agent for ranking emails
- CLI interface with prospect input
- Formatted output with all three emails and picker recommendation
- Automatic tracing via OpenAI Agents SDK
- Error handling and validation

### Excluded (Future)
- Email delivery integration (SMTP, Mailgun)
- A/B testing or conversion tracking
- Prospect research or CRM lookup
- Persistent storage or history
- Web UI / dashboard
- Multilingual support
- Tool-assisted email generation (validation, sentiment analysis)

## How to Use

```bash
# Install and run
cd sales-agents/
uv sync
export OPENAI_API_KEY="sk-..."
uv run python src/sales_agents.py

# Provide prospect details when prompted
# App generates three emails and picker recommendation
# Print results to stdout
```

## Example Output

```
=== GENERATED SALES EMAILS ===

[Email 1: The Professional]
- Formal, ROI-focused, with credentials and case studies

[Email 2: The Witty]
- Clever opening, conversational tone, humor and relatability

[Email 3: The Concise]
- Bullet points, quantifiable benefits, scannable in 30 seconds

═══════════════════════════════════════════════════════════════
SALES PICKER RECOMMENDATION
═══════════════════════════════════════════════════════════════

Best Email: The Concise

Reasoning: Finance buyers value efficiency. The Concise email's bullet-point format
and focus on time savings will cut through a busy inbox more effectively.
```

## Next Steps (Implementation)

1. Implement `src/sales_agents.py` — CLI entry point and orchestration
2. Implement `src/agents_def.py` — Agent definitions using OpenAI Agents SDK
3. Implement `src/utils.py` — Formatting and validation helpers
4. Test with sample prospect scenarios
5. Capture and review traces in OpenAI platform dashboard
6. Iterate on agent prompts based on output quality

## Related Projects

- **[Joke Agent](../joke-agent/)** — Similar orchestration pattern; single agent with tool calling
- **[Work Folder](../README.md)** — Portfolio of agent projects

---

**Project Status:** Documentation & Design Complete (Ready for Implementation)  
**Last Updated:** 2026-07-27  
**Next Phase:** Code Implementation

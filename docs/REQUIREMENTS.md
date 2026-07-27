# Sales Agents — Requirements

## 1. Functional Requirements

### FR1: Multi-Agent Email Generation
The system SHALL orchestrate three distinct sales agents, each generating a cold sales email for a given prospect scenario.

- **FR1.1:** Each agent receives identical input: prospect company name, industry, pain point, and desired outcome.
- **FR1.2:** Each agent produces a unique cold sales email (subject line + body) from its distinct persona.
- **FR1.3:** Email generation uses the OpenAI API (model `gpt-4-mini` or equivalent) via the OpenAI Agents SDK.

### FR2: Sales Agent Personas
The system SHALL define three distinct sales agent personas with unique styles and approaches.

- **FR2.1 — Agent 1 "The Professional":**
  - Style: Formal, corporate, credentials-focused.
  - Approach: Emphasizes ROI, risk mitigation, and proven case studies.
  - Tone: Authoritative, data-driven, trustworthy.
  
- **FR2.2 — Agent 2 "The Witty":**
  - Style: Clever, conversational, personality-driven.
  - Approach: Uses humor, relatability, and emotional connection to cut through inbox noise.
  - Tone: Warm, approachable, memorable.
  
- **FR2.3 — Agent 3 "The Concise":**
  - Style: Direct, scannable, data-driven.
  - Approach: Front-loads value proposition in bullets; respects reader's time.
  - Tone: Efficient, punchy, action-oriented.

### FR3: Sales Picker Agent
The system SHALL define a "sales picker" agent that reviews all three emails and selects the most compelling option.

- **FR3.1:** The picker receives all three emails and the original prospect context (company, industry, pain point, outcome).
- **FR3.2:** The picker evaluates emails based on likely conversion potential for the given scenario.
- **FR3.3:** The picker outputs: (a) which email is best (by agent name), and (b) a brief rationale (1–2 sentences).

### FR4: Command-Line Interface
The system SHALL provide a CLI for running the email generation and picker workflow.

- **FR4.1:** User provides prospect details via CLI arguments or interactive prompts:
  - Company name
  - Industry
  - Pain point / use case
  - Desired outcome
- **FR4.2:** System executes the workflow and prints all three emails to stdout, each clearly labeled with the agent name and persona.
- **FR4.3:** System prints the sales picker's decision and rationale.

### FR5: Output Format
The system SHALL output emails in a clear, readable format.

- **FR5.1:** Each email includes:
  - Agent name and persona ("The Professional," "The Witty," "The Concise")
  - Subject line
  - Email body (salutation, main body, call-to-action, signature)
- **FR5.2:** Emails are separated visually (e.g., divider lines, clear section headers).
- **FR5.3:** The picker's selection appears at the end with a clear header and reasoning.

### FR6: Error Handling
The system SHALL handle errors gracefully.

- **FR6.1:** OpenAI API errors (auth, rate limit, network) are caught and reported as user-friendly messages.
- **FR6.2:** Invalid user input (missing/malformed arguments) is rejected with a clear usage message.
- **FR6.3:** No stack traces are shown to the end user; errors are logged for debugging.

## 2. Non-Functional Requirements

### NFR1: Technology Stack
- **Language:** Python 3.12+
- **LLM Framework:** OpenAI Agents SDK (`openai-agents` package)
- **LLM Model:** `gpt-4-mini` (or latest equivalent at deployment time)
- **API:** OpenAI API
- **Orchestration:** Sequential or parallel execution of agents, depending on rate-limit constraints; not explicitly specified for MVP.

### NFR2: Configuration & Secrets
- **NFR2.1:** OpenAI API key read from environment variable (`OPENAI_API_KEY`), never hardcoded.
- **NFR2.2:** No other secrets or credentials required for MVP.

### NFR3: Observability
- **NFR3.1:** All agent runs (email generation for each agent + picker selection) are automatically traced via the OpenAI Agents SDK.
- **NFR3.2:** Traces are viewable in the OpenAI platform Traces dashboard (platform.openai.com → Traces) with no additional instrumentation.
- **NFR3.3:** Each trace includes: model name, input prompt, tool calls (if any), and final output.

### NFR4: Code Organization
- **NFR4.1:** Main CLI entry point: `src/sales_agents.py`.
- **NFR4.2:** Agent definitions and instructions: `src/agents_def.py`.
- **NFR4.3:** Utility functions (formatting, input validation): `src/utils.py`.
- **NFR4.4:** No external data files or databases; all agent prompts embedded in code.

### NFR5: Documentation
- **NFR5.1:** README.md with setup, usage, and examples.
- **NFR5.2:** Operational Concept document (describing the use case and flow).
- **NFR5.3:** Requirements document (this file).
- **NFR5.4:** Design document (architecture, agent prompts, example output).

### NFR6: Execution
- **NFR6.1:** Single-process Python CLI app; no server/daemon/background workers.
- **NFR6.2:** Synchronous execution; blocking calls to the OpenAI API.
- **NFR6.3:** No persistence across runs (in-memory only).

## 3. User Stories

### US1: Generate Sales Emails
**As a** sales manager,
**I want to** generate three distinct sales emails for a prospect,
**So that** I can evaluate different messaging approaches before deciding which to send.

**Acceptance Criteria:**
- I can run the app with prospect details (company, industry, pain point, outcome).
- The app generates and displays three emails, each in a distinct style.
- Each email is complete (subject + body) and ready to send (with minimal tweaks).

### US2: Get Sales Picker Recommendation
**As a** sales manager,
**I want to** see which of the three emails the picker recommends as most likely to convert,
**So that** I have a data-backed (LLM-backed) opinion to inform my choice.

**Acceptance Criteria:**
- After email generation, the picker's choice is displayed.
- The choice includes a brief, clear rationale.
- The rationale is aligned with the prospect scenario.

### US3: Audit and Debug Agent Runs
**As a** developer or sales ops analyst,
**I want to** see traces of every agent run in the OpenAI platform dashboard,
**So that** I can audit agent decisions and debug/improve prompts.

**Acceptance Criteria:**
- All agent runs (3 email generators + 1 picker) appear as separate traces.
- Traces are visible in platform.openai.com → Traces without manual logging.
- Each trace includes input, model chosen, and output.

## 4. Assumptions & Constraints

### Assumptions
- A1: User has a valid OpenAI API key with access to `gpt-4-mini`.
- A2: User has internet connectivity to call the OpenAI API.
- A3: The fictional company context (TechFlow Solutions) is sufficient for all agent examples; no real company data is used.
- A4: LLM-driven email generation is acceptable for this demo; no human-in-the-loop review is required (though recommended in production).

### Constraints
- C1: Cold sales emails MUST NOT impersonate real people or companies or make false claims.
- C2: Emails MUST be addressed to a generic "prospect" (not a real person by name) for this MVP.
- C3: No database persistence or long-term storage of generated emails.
- C4: API rate limits from OpenAI may necessitate sequential execution of agents rather than parallel.

## 5. Out of Scope (MVP)

- Email delivery integration (no SMTP, Mailgun, SendGrid).
- A/B testing or conversion tracking.
- Prospect research or CRM lookup.
- Multiple languages / localization.
- Web UI or dashboard.
- Persistent storage or history.
- Real-time collaboration or multiple users.

---

**Document Version:** 1.0  
**Last Updated:** 2026-07-27  
**Status:** Requirements finalized for MVP implementation

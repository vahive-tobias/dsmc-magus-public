# OpenClaw Stability Guide
## Fix Context Bloat, Ghost Overload & Agent Drift

**VaHive Systems Lab | v1.2 | 2026**

support@aivare.ai | [aivare.ai](https://aivare.ai)

---

> *The real reasons your OpenClaw agents slow down, overload, or drift — and how to fix them fast.*

---

If your OpenClaw setup feels unstable, you aren't alone. Right now, the most common issues builders run into — responses slowing down, skyrocketing token usage, or agents randomly forgetting their instructions — feel like mystery bugs. It is easy to assume the AI model is getting "dumb," the API is failing, or your hardware isn't keeping up.

But most OpenClaw problems aren't model, API, or hardware problems at all. They are context structure problems.

OpenClaw is incredibly flexible, but that flexibility means it will happily accumulate huge session transcripts, inject unnecessary context, leak memory between completely unrelated tasks, and inflate token usage over time. Eventually, the system collapses.

This guide is for builders who are tired of trial-and-error troubleshooting. Written by someone who builds drift-resistant AI governance layers, this guide explains:

- The most common failure patterns
- How to fix them quickly
- How to design more stable agent workflows

No code is required to understand or apply anything in this guide.

---

## Chapter 1: The Four Failure Patterns Most OpenClaw Users Hit

This chapter is about recognition. When you see your own exact problem described clearly, you know you aren't just dealing with a random bug — you are dealing with a predictable system behaviour. Once you can name it, you can fix it.

Here are the four ways OpenClaw agents typically break down in production.

---

### Failure Pattern 1: Context Explosion

**The symptoms:** Token usage slowly creeps up, response times get noticeably slower, and the model's reasoning quality takes a nosedive.

**The cause:** OpenClaw rebuilds context on every single request by reading the raw session transcript. If that transcript grows unchecked, every subsequent request becomes heavier and harder for the model to process.

**Real example:** A user in a Thai OpenClaw Facebook group perfectly diagnosed this without even looking at the code: *"ยิ่งบวมยิ่งโง่ลง"* — "The more bloated it gets, the dumber it becomes." They were exactly right.

---

### Failure Pattern 2: The "Ghost Overload" Loop

**The symptoms:** You get repeated "AI service temporarily overloaded" errors. Even incredibly simple prompts fail to execute. Restarting the OpenClaw gateway does absolutely nothing to fix it.

**The cause:** A single severely bloated session transcript file is being continuously re-injected on every request, creating an infinite API overload loop that survives system restarts.

**Real example:** A builder working on an Excel automation agent hit a wall where the agent locked up entirely. They assumed the API was down — but the agent was actually trying to swallow a massive hidden payload on every single ping.

---

### Failure Pattern 3: Memory Bleed & Identity Drift

**The symptoms:** The agent forgets its core instructions, starts referencing completely unrelated past tasks, and exhibits strange behaviour bleeding over between sessions.

**The cause:** Using global memory shared across tasks without strict boundaries. The agent's core identity instructions get buried under task messages, random memory retrievals, and reasoning traces.

**Real example:** A user tries to give their agent persistent memory, but the retrieval system keeps bringing back useless, irrelevant entries from an old project. The model's self-definition collapses because it is reasoning through garbage state.

---

### Failure Pattern 4: Tool Output Flooding

**The symptoms:** Massive token usage spikes immediately following a tool call. The context window grows rapidly out of control.

**The cause:** Agents dumping full, raw tool outputs directly back into the prompt instead of passing summarised, structured results.

**Real example:** An agent tasked with Amazon scraping successfully calls a tool to fetch a page — but returns the massive, unparsed JSON schema or raw HTML directly into the active context. Suddenly, a 20-token request becomes a 3,000-token nightmare.

---

## Chapter 2: Emergency Recovery

When your OpenClaw system crashes or slows to a crawl, you need immediate solutions. Here are the step-by-step interventions to get your agent running again before you fix the underlying architecture.

---

### Fix 1: Clearing the "Ghost Overload" Loop

Restarting the OpenClaw gateway won't help with ghost overload. OpenClaw rebuilds context from session transcripts — if a heavy prompt has bloated one file, the system will keep re-injecting that massive history on every single call.

**The recovery procedure:**

1. Stop the OpenClaw gateway.
2. Navigate to your sessions folder: `~/.openclaw/agents/<agentId>/sessions/`
3. Delete the bloated session `.jsonl` file.
4. Restart the gateway.
5. Start a fresh session.

---

### Fix 2: Proper Use of /new and /reset

The `/new` or `/reset` commands start a new session with a clean transcript from the user's side — but they do not magically erase old bloated files from your disk. The old transcript stays there unless you manually remove it.

**How to find and delete your transcripts without a terminal:**

**On Mac (Finder):** Press `Cmd + Shift + G` to open the Go to Folder bar. Type `~/.openclaw` and hit Enter. Open the `agents` folder, find your agent, and open the `sessions` folder to delete the heavy `.jsonl` files.

**On Windows (File Explorer):** Click the address bar at the top, type `%USERPROFILE%\.openclaw` and hit Enter. Navigate to `agents` → your specific agent → `sessions`, and delete the bloated files.

---

### Fix 3: Preventing Tool Output Flooding

When agents use tools, they often dump the full, raw output directly back into the prompt instead of returning summarised results. This is the fastest way to cause a token spike.

❌ **Bad — Tool Output Flooding:**
```
{ "status": 200, "data": { "items": [ {"id": "1A", "title": "...",
"desc": "...", "meta": "...", "tags": ["a", "b", "c"]} ] } }
<div><ul><li class="nav-item">...</li></ul></div>
(Imagine this raw code and data extending for another 100+ lines...)
```

✅ **Good — Summarised Results:**
```
• Found 3 relevant items.
• Item 1A is the best match.
• All items are currently in stock.
```

By forcing your tools to return clean summaries, you immediately stop the context window from exploding.

---

### Fix 4: Quick Session Rotation

Long sessions accumulate hidden context. Until you implement a proper memory governance layer, regularly rotating your sessions is the most effective manual control you have.

**A real-world scenario:** You spent 40 minutes having your agent research three competitors. The agent now has all that messy back-and-forth research history in its context. Do not use that same session to write your final email copy — the agent will be distracted by 40 minutes of random research notes.

Instead, type `/new`. Start a completely fresh session, and paste in a clean 3-sentence summary of the research you just did. Your agent will write a significantly better email.

---

## Chapter 3: How OpenClaw Actually Builds Context

To stop your agents from breaking, you need to understand what happens every time you send a message. When you send a simple 10-word message to your OpenClaw agent, it does not just send those 10 words to the AI. It packages up everything it knows into one request.

Every LLM call receives a context window composed of:

1. System prompt
2. Agent instructions
3. Memory files
4. Session transcript (everything said previously)
5. Latest user message

### The Context Explosion Math

Because of this structure, a transcript that grows indefinitely will eventually crush the system. Here is what that looks like in a real session:

**Run 1:**
- System prompt: ~600 tokens
- Agent instructions: ~800 tokens
- Memory files: ~1,200 tokens
- Session transcript: ~800 tokens
- Latest user message: ~200 tokens
- **Total sent to AI: 3,600 tokens**

**Run 2:** The agent responds, and that response gets permanently added to the transcript.
- System prompt + instructions + memory: ~2,600 tokens
- Session transcript (now including Run 1): ~1,800 tokens
- Latest user message: ~50 tokens
- **Total sent to AI: 4,450 tokens**

**Run 5:** You are asking quick follow-up questions, but the transcript has been compounding the whole time.
- System prompt + instructions + memory: ~2,600 tokens
- Session transcript: ~8,500 tokens
- Latest user message: ~30 tokens
- **Total sent to AI: 11,130 tokens**

You are asking a 30-token question, but your API is being forced to read 11,000+ tokens to answer it. This compounding math is why your agent slows down, costs more, and eventually crashes with a ghost overload error.

---

## Chapter 4: Transient History vs. Persistent State

Most users treat all of their agent's history as the same thing — they let the agent remember everything. Storing everything is the worst possible design choice for a long-running agent.

To fix context bloat, you need to understand the difference between two distinct types of memory.

### Transient History — The Scratchpad

Your session transcript (`.jsonl` files) is your transient history. Think of it as a messy scratchpad on your desk — it contains the back-and-forth brainstorming, the dead ends, the typos, and the casual questions.

**The rule:** The scratchpad is temporary. When the immediate task is done, the scratchpad should be discarded.

### Persistent State — The Rulebook

Your memory (`.md` files) is your persistent state. Think of it as the project's official Rulebook — it contains curated facts, active decisions, constraints, brand tone guidelines, and strict formatting rules.

**The rule:** The rulebook is intentionally injected into the prompt. It must be kept clean, small, and highly relevant.

Without a clean separation between the scratchpad and the rulebook, your system will almost always fall back to dumping the entire messy scratchpad into the context window.

### What Good Memory Actually Looks Like

❌ **Bad — Raw Transcript Dump:**
```
User said they wanted a Python script, then user asked about JavaScript,
then agent wrote a JavaScript function but there was an error on line 42,
so the user said to change the variable name...
(Imagine this rambling log extending for another 150+ lines...)
```

✅ **Good — Curated Active Decisions:**
```
project: accounting software research
language: python
current objective: write the database schema
constraint: must support multi-currency
```

Good memory is sparse, relevant, and curated. Everything else should end when the session ends.

---

## Chapter 5: Prevention Basics & Active-State Discipline

Now that you understand why systems break, here is how to prevent it. The answer is strict discipline over what gets injected into the prompt.

### The Summarisation Dilemma

The obvious answer to context bloat is to summarise the transcript instead of injecting it whole. However, if you are using an API like Claude or OpenAI, asking the model to summarise a 10,000-token transcript still costs you 10,000 input tokens.

**The zero-cost approach:** Advanced builders use a local AI handoff. They pass the heavy summarising tasks to a free local model running on their own machine — like Ollama or LM Studio — and hand the clean summary back to their OpenClaw API agent. The local model reads 10,000 tokens for free. The expensive API model only ever sees the 100-token summary.

**If you don't have local AI set up:** Use the Token-Efficient Task Prompt template in the appendix. It forces the model to extract only the facts, giving you much tighter summarisation without building any additional infrastructure.

### Task-Scoped Memory

Global memory — where the agent remembers everything across every task — causes memory bleed. An agent building a website should not be distracted by the email draft from yesterday.

❌ **Bad — Global Memory Bleed:**
```
project 1: accounting software
project 2: email to mum
project 3: python script
(Imagine this list extending to 50+ unrelated tasks...)
```

✅ **Good — Task-Scoped Memory:**
```
current task: python script
active constraints: use python 3.9+, no third-party libraries
```

### Pre-Tool Classification

One of the most dangerous sources of agent drift is when a model confuses a hypothetical thought with a strict instruction and then executes a tool based on it.

You can prevent this by explicitly tagging statements before the agent touches a tool.

❌ **Bad — No Classification:**
```
You: "What if we dropped the database tables and started over?"
Agent: "Okay, dropping database tables now." (Disaster)
```

✅ **Good — Pre-Tool Classification:**
```
You: "What if we dropped the database tables and started over?"
Governance Layer: Classifies input as [HYPOTHETICAL].
Agent: "If we did that, we would lose all user data. Should I proceed,
or are we just brainstorming?"
```

---

## Chapter 6: Stable Agent Architecture Principles

Moving from a system that constantly crashes to one that runs reliably requires a shift in how you design your workflows. Stable agents come from strict boundaries, not massive prompts.

### The "Do-Everything" Trap

Beginners often try to build one "God Agent" that handles everything — cram all instructions, tools, and formatting rules into one massive system prompt. When a model tries to juggle 50 rules at once, it drops them.

❌ **The Massive Prompt:**
```
You are an expert coder, copywriter, and database admin. Search the web
for competitors. Write a 50-page report. Format it in markdown. Always
use emojis. Never use the word 'synergy'. Remember my dog's name is
Buster...
(Imagine this extending for another 100+ lines of mixed instructions...)
```

### The Recommended Flow

Instead of one massive prompt, stable OpenClaw architecture uses a routed flow. One Orchestrator decides what needs doing and passes the job to a Specialised Agent with a small, clean set of instructions.

✅ **The Clean Architecture Flow:**
```
User Input
    ↓
Orchestrator Model (classifies the task)
    ↓
Task Router (sends it to the right agent)
    ↓
Specialised Agent (e.g. Research Agent or Coding Agent)
    ↓
Minimal State Memory (agent gets only the context it needs)
```

By splitting the work, the context window stays small, token costs stay low, and the agent stops getting confused.

---

## Chapter 7: Delegating Large Task Lists Without Silent Failures

Once you have basic context control working, a new problem tends to appear when you try to hand your agent a long list of tasks to run unattended — especially overnight.

The symptoms are always the same. The agent starts strong, makes solid progress on the first few tasks, then gets stuck somewhere in the middle and goes completely silent. No updates, no error messages, no sign of life until you check in the next morning and realise it stopped three hours ago.

---

### Why Prompt Tricks Don't Hold

The instinct is to solve this with stronger instructions: "report your progress every 10 steps," "set ETAs for each task," "check your state before moving on." These work briefly, and then they stop working.

The reason comes back to the same principle from Chapter 4. Self-check instructions live in the session transcript — transient history. Once the session grows, those instructions get diluted. The agent isn't ignoring you. It simply can't reliably hold onto a behavioural rule buried 40 messages deep in a growing transcript, especially when a tool hiccup or unexpected output has already disrupted its working state.

The fix follows the same persistent-state principle from Chapter 4. If the progress tracker lives in a persistent `.md` file that is injected on every request — just like `SOUL.md` and `AGENTS.md` — it cannot be buried or lost. The agent reads it fresh on every single call.

---

### Step 1: Create a `status.md` File in Your Workspace

This file becomes part of your Rulebook — persistent state, not scratchpad history. Add it to your workspace `.md` files so OpenClaw injects it on every request alongside your other persistent files.

The format is a simple table. Keep it small — only current and upcoming tasks. Completed tasks can be cleared out once you've reviewed them.

```
Task                          | Status      | Last Updated        | ETA     | Blocker
------------------------------|-------------|---------------------|---------|--------
1. Scrape competitor pricing  | In progress | 2026-03-07 02:15   | ~45 min | none
2. Analyse margins            | Not started | -                   | -       | -
3. Write summary email        | Not started | -                   | -       | -
```

---

### Step 2: Add One Rule to `AGENTS.md`

Paste this near the top of your operational rules — the section that governs how the agent works, not what it knows.

```
Every 8–10 tool steps OR every 15 minutes of runtime, you MUST:
1. Update the status.md table — set the current task's status,
   last-updated timestamp, and any blocker.
2. Output a one-line progress summary before continuing.
Never move to the next task until status.md has been updated.
```

Because this rule lives in `AGENTS.md`, it is part of the injected Rulebook — not a one-off instruction that gets buried. The agent re-reads it on every request.

---

### What This Looks Like in Practice

❌ **Without a persistent tracker:**
```
02:00 — Agent starts Task 1. Good progress.
02:30 — Agent encounters unexpected output from a scraping tool.
02:31 — Agent retries silently. No update.
02:45 — Agent appears stuck. No indication why.
Morning — You check in. No progress since 02:31. No record of what happened.
```

✅ **With status.md + the AGENTS.md rule:**
```
02:00 — Agent starts Task 1. Updates status.md: "In progress."
02:30 — Agent encounters unexpected output.
02:31 — Agent updates status.md: "Blocker: unexpected JSON structure
         in tool response. Retrying with modified parameters."
02:32 — Agent outputs: "Task 1 progress check: hit a tool output
         format issue, adjusting approach now."
02:45 — Agent updates status.md: "Task 1 complete."
02:45 — Agent moves to Task 2. Updates status.md: "Task 2 in progress."
Morning — You review status.md. Full trace of what happened and when.
```

The difference isn't agent intelligence — it's whether the progress tracking has somewhere persistent to live.

---

### Connecting It to Your Existing Setup

At the start of any long-running session, use the Rulebook Context Block from Appendix A as normal and add one line to the active decisions section:

```
Active status tracker: status.md — update before every major step.
```

Because `status.md` is a persistent workspace file, it survives session rotation. If you need to restart mid-task, the agent picks up from the last state it recorded — not from a blank slate.

---

## Chapter 8: Resources & Next Steps

If your OpenClaw setup feels unstable, the first thing to audit is your context injection, your transcript growth, and your memory scope. In almost every case, fixing your underlying structure fixes the problem.

**The final key principle: Stable AI systems come from structure, not from constantly switching models.**

If this guide helped you, please share it with other builders who might be stuck.

### Free Tools

- **DSMC Minimal — GitHub:** A lightweight open-source script implementing the Active Decisions and context management concepts from this guide. Zero dependencies, drop into any existing Python or TypeScript agent.
  Access: [github.com/vahive-tobias/dsmc-magus-public](https://github.com/vahive-tobias/dsmc-magus-public)

- **The Prompting Layers — Foundation Guide:** How to write prompts that models actually understand without wasting tokens. Free from the Gumroad store.
  Access: [puititiya.gumroad.com/l/prompt-foundations](https://puititiya.gumroad.com/l/prompt-foundations)

- **The Formal Architecture — MAGUS v3.0:** The governance patterns this guide is derived from are formally specified in MAGUS v3.0, a published research architecture for structural alignment drift in long-running AI agents.
  📄 [DOI: 10.5281/zenodo.19013833](https://doi.org/10.5281/zenodo.19013833)

### Taking the Next Step — DSMC Agent Engine v2.0

If you have read this guide and thought "I understand this now, but I don't want to build all these safety rails from scratch" — there is a direct next step.

---

**Why the Agent Engine exists:**

My OpenClaw agent deleted a folder I needed.

Not the archive folder. The actual working folder. Files I hadn't backed up.

The agent did exactly what the loop told it to do. No error. No hesitation. It just executed.

That was the moment I realised I'd been thinking about this wrong. I was trying to make my agents smarter. What I actually needed was a hard stop between "agent decides" and "agent actually does it."

I pulled the zero-trust execution boundary from MAGUS — a formally published AI governance architecture. I packaged it as the MAGUS Guardian inside DSMC Agent Engine v2.0.

Now every high-risk tool call — delete, send email, API call, payment, anything destructive or irreversible — gets paused and sent to your phone on Telegram, WhatsApp, or LINE before it executes.

You reply:
- **1** = block
- **2** = allow once
- **3** = allow always

Reply 3 and it cryptographically hashes that exact action into a permanent allowlist. It never asks again. Zero context bloat.

A live dashboard shows every active decision, risk score, and drift warning in real time.

---

**What the full engine adds over this guide:**

| Feature | This Guide | DSMC Agent Engine v2.0 |
|---|---|---|
| Context management patterns | ✅ Manual | ✅ Automated |
| Message classification | ✅ Prompt-based | ✅ Confidence-scored with review queue |
| Drift detection | ✅ Concepts | ✅ Real-time alerts |
| Revision trail | ❌ | ✅ SQLite, persistent |
| HITL execution intercept | ❌ | ✅ MAGUS Guardian |
| Phone approval routing | ❌ | ✅ Telegram / WhatsApp / LINE |
| Cryptographic allowlist | ❌ | ✅ O(1), permanent |
| Live dashboard | ❌ | ✅ Gradio UI |
| Session archiving | ✅ Manual steps | ✅ Automatic |
| 3-layer failover | ❌ | ✅ |
| Works with Ollama / LM Studio / Claude / GPT-4o / Gemini | ✅ Concepts | ✅ All providers, one toggle |

👉 [DSMC Agent Engine v2.0 — $49](https://puititiya.gumroad.com/l/dsmc-agent-engine)

---

## Appendix A: Free Prompt Templates

Two foundational templates you can copy and paste into your OpenClaw setup today.

---

### Template 1: The "Rulebook" Context Block

Use this at the start of any working session where you will be making decisions you need the model to hold onto. This is your Persistent State block.

```
PROJECT CONTEXT — maintain this throughout our conversation.

Project: [What you're working on]

Active decisions (hold these — do not suggest alternatives):
- [Decision 1]
- [Decision 2]

Constraints (absolute):
- [Constraint 1]

Current position: [Where you are in the project right now]

Working rule: When I explore hypotheticals or ask "what if" questions,
treat them as exploration only. Do not update the active decisions above
unless I say "this is now the decision."

Confirm you have understood this context block before we begin.
```

**The State Check Prompt** — use this periodically to catch memory bleed:

```
Without me prompting you, list every active decision we have made in
this session so far. If you are uncertain about any of them, flag it.
```

---

### Template 2: Token-Efficient Task Prompt

Use this when you need a precise, specific output — like summarising a messy transcript — and want the model to follow instructions exactly without wasting tokens.

```
Role: [One sentence — role and relevant expertise].

Task: [Direct statement of what you need. No hedging].

Input: [The material to work with, if any].

Output:
- Format: [Exactly what format, e.g. 3 bullet points]
- Length: [Specific word or sentence count]
- Tone: [Specific tone requirement]

Priority instruction: [The single most important thing, restated].
```

---

## Appendix B: The OpenClaw Workspace Files

OpenClaw loads a small set of workspace `.md` files into the system prompt on almost every request. These files shape how the agent fundamentally runs — its personality, its rules, and its context. If you want your agent to feel stable and reliable from the very first message, this is where you focus your editing time.

### Core Baseline Files

These are always loaded. Changing these changes everything about how the agent feels.

| File | Location | What it controls | Priority |
|---|---|---|---|
| `SOUL.md` | `~/.openclaw/workspace/` | Personality, core values, philosophy, tone, long-term identity, and boundaries — *who the agent is* | ★★★★★ |
| `AGENTS.md` | `~/.openclaw/workspace/` | Operational rules, safety, task execution standards, when to ask for confirmation, tool usage policy — *how the agent works* | ★★★★★ |
| `USER.md` | `~/.openclaw/workspace/` | Your personal context — name, timezone, preferences, work style, communication quirks — *who it's talking to* | ★★★★ |
| `IDENTITY.md` | Workspace or per-agent folder | External presentation and specific role instructions — *how it presents itself* | ★★★ |

### Secondary Files

- **`MEMORY.md`** — Long-term curated facts, decisions, and preferences. Not always fully injected, but actively searched and pulled in.
- **`memory/YYYY-MM-DD.md`** — Daily conversation and memory logs (your recent context).
- **`TOOLS.md`** — Tool-specific instructions and usage rules.

### The Golden Rule

`SOUL.md` and `AGENTS.md` generate 90% of your agent's consistent behaviour. They are read on every single request.

The session transcript (the `.jsonl` file) is not a baseline file — it is transient conversation history. That is exactly why letting it grow unchecked causes context bloat and the ghost overload loop.

Your `.md` files are for persistent, curated memory. Keep them clean, keep them strict, and your agent will stop drifting.

---

## Appendix C: Telegram Setup for OpenClaw Agents

Telegram is the most flexible of the three messaging options and the recommended starting point if you have no preference. It handles high message volume cleanly, supports structured topic threads, and its bot API is well-documented and reliable.

---

### The Beginner Mistake: Testing With Your Personal Account

The most common setup error is trying to connect OpenClaw to a personal Telegram account rather than creating a dedicated bot. Telegram's bot API and the user API are completely separate systems. You need a bot.

**The correct starting point:**

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts to name your bot
3. BotFather gives you a **Bot Token** — save this, it goes in your `.env` file as `TELEGRAM_BOT_TOKEN`

---

### The Headache-Saver: Getting Your Chat ID Right

The second thing beginners get wrong is using a Telegram username where the Agent Engine needs a numeric Chat ID. These are different things and mixing them up causes silent failures — the bot authenticates fine, but messages never arrive.

**How to get your correct Chat ID:**

1. Start a conversation with your bot (send it any message)
2. Open this URL in your browser, replacing `YOUR_BOT_TOKEN` with your actual token:
   `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
3. Find the `"id"` field inside the `"chat"` object in the response
4. That number is your Chat ID — it goes in `.env` as `TELEGRAM_CHAT_ID`

It will be a number like `123456789` or `-100123456789` (negative numbers indicate group chats). Use the number exactly as it appears.

---

### Going Further: Structured Topics Instead of One Chaotic Stream

Once your bot is working, a single flat chat becomes hard to follow quickly — heartbeats, task updates, email notifications, and HITL approval requests all land in the same stream.

Telegram supports **Forum Mode**, which gives your bot a structured topic thread for each category of activity. This is significantly easier to manage for long-running agents.

**Step 1 — Enable Forum Mode**

Open BotFather, select your bot, and enable **Threaded Mode** (also called Forum Mode). This allows a single Telegram group chat to contain multiple named topics.

**Step 2 — Ask Your Agent to Create the Topics**

Tell your agent:

```
Set up forum topics in our Telegram chat.
First call getForumTopicIconStickers to retrieve available emoji IDs.
Then create topics using createForumTopic with icon_custom_emoji_id.
```

Example topics that work well for agent monitoring:

- 📧 Email Intake
- ⚙️ Cron Jobs
- 🧠 Agent Updates
- 📋 Tasks
- 🚨 HITL Approvals

> **Important:** After creating each topic, send at least one message inside it. Telegram will not display a topic in the sidebar until it contains a message.

**Step 3 — Route Activity to the Right Topic**

Once the topics exist, tell the agent:

```
Route cron jobs, heartbeats, and system notifications to the most
relevant topic. HITL approval requests always go to HITL Approvals.
```

**Bonus:** If you forward emails to your bot, it can process them inside the Email Intake topic thread. Long-running email conversations stay contained and easy to follow rather than buried in a general stream.

---

## Appendix D: LINE Setup for OpenClaw Agents

LINE is the right choice for builders in Thailand, Japan, Taiwan, and across Southeast Asia. If your primary users or your own workflow is on LINE, it makes more sense to use the platform you're already in than to add Telegram for agent notifications alone.

---

### The Beginner Mistake: Confusing the Channel Access Token and the Channel Secret

LINE gives you two different credentials when you set up a Messaging API channel, and they do different things. Mixing them up produces authentication errors that don't explain themselves clearly.

| Credential | What it is | Where it goes |
|---|---|---|
| **Channel Secret** | Validates incoming webhook signatures | Used to verify LINE is actually sending the request |
| **Channel Access Token** | Authorises outgoing messages from your bot | Goes in `.env` as `LINE_CHANNEL_ACCESS_TOKEN` |

Get both from the LINE Developers Console under your channel's **Messaging API** tab. The Channel Access Token is the long string you issue — you may need to click **Issue** to generate it the first time.

---

### The Headache-Saver: Webhook Timeouts Will Disable Your Endpoint Silently

LINE's webhook system requires your endpoint to respond within a short timeout window. If your agent is doing processing before it acknowledges the webhook — querying a database, waiting on a slow API, or running a classification step — LINE may mark your webhook as failing and disable it without a clear notification.

**The fix:** Acknowledge the webhook immediately, then process.

Your endpoint should return HTTP 200 as its first action, before any agent logic runs. Process the message content asynchronously after the acknowledgment is sent. If LINE receives no response within its timeout, it will retry and eventually stop sending events to your endpoint.

If your webhook stops receiving messages and you can't figure out why, check the LINE Developers Console under **Webhook settings** — it logs delivery failures there.

> **Note for Thai builders:** The LINE user ID format is `Uxxxxxxxxxxxxxxx` (uppercase U followed by a 32-character hex string). Group IDs start with `C`. Confirm which format your `.env` expects before filling it in.

---

### Going Further: LINE Groups as Structured Workspaces

LINE doesn't have a native topic-thread system equivalent to Telegram's Forum Mode. However, you can replicate structured routing by using separate LINE groups for each category of agent activity.

**The approach:**

Create separate LINE groups for each category:

- 📧 **Email Intake** — incoming email processing and replies
- ⚙️ **System** — cron jobs, heartbeats, status updates
- 🚨 **Approvals** — HITL intercept messages requiring your response
- 📋 **Tasks** — active task progress and completions

Add your bot to each group. Each group has its own `groupId`, which you retrieve from an incoming webhook payload after the bot receives a message in that group.

Tell your agent which group ID maps to which category, and route accordingly:

```
Route system heartbeats and cron confirmations to the System group.
Route all HITL approval requests to the Approvals group.
Route email processing updates to the Email Intake group.
```

This gives you the same structured visibility as Telegram's topic threads using LINE's existing group infrastructure.

---

## Appendix E: WhatsApp Setup for OpenClaw Agents

WhatsApp reaches more people globally than any other messaging platform. If your HITL approvals need to reach you on WhatsApp, or if your workflow is already there, this is the right integration to use.

The Agent Engine connects via Twilio's WhatsApp API. Twilio is not the only path, but it is the most straightforward and the one the engine is configured for out of the box.

---

### The Beginner Mistake: Building on the Sandbox and Discovering Template Restrictions Later

Twilio offers a WhatsApp Sandbox for testing. It works immediately, requires no approval process, and will get your agent sending messages within minutes. This is exactly why it causes problems.

The Sandbox is for testing only. WhatsApp's production API has a rule that significantly changes how you can architect your agent:

**You can only send free-form messages to a user within 24 hours of them sending you a message first.**

After that 24-hour window closes, you can only send pre-approved **template messages** — fixed formats submitted to and approved by WhatsApp in advance, typically taking 1–3 business days.

**What this means practically:**

- ✅ User sends your agent a message → agent can reply freely for 24 hours
- ✅ Agent sends a template message to re-engage after 24 hours
- ❌ Agent proactively initiates a free-form conversation → blocked in production

If your agent needs to send unprompted notifications, heartbeats, or HITL approval requests, design your templates before you build. A template like `"Action required: {{1}} — reply YES to approve or NO to block"` covers most HITL use cases and is straightforward to get approved.

---

### The Headache-Saver: Sandbox Numbers Look Different From Production Numbers

In the Twilio Sandbox, your WhatsApp number is Twilio's shared sandbox number (`+14155238886`). In production, it's a dedicated number you provision through Twilio.

Your `.env` has:

```
WHATSAPP_FROM=whatsapp:+14155238886   ← sandbox number
WHATSAPP_TO=whatsapp:+your_number
```

When you move to production, `WHATSAPP_FROM` changes to your dedicated Twilio number. Keep the number in `.env` only — never reference it directly in agent instructions or system prompts. If you hard-code the sandbox number anywhere outside `.env`, you will have failed messages in production that are difficult to trace back to this.

---

### Going Further: Routing With WhatsApp's Limitations in Mind

WhatsApp does not support topic threads or group-based routing the way Telegram and LINE do. A single WhatsApp conversation is a flat stream, and that is the architecture you work within.

**The practical approach for agent monitoring:**

Use a prefix convention in outgoing messages to create visual structure in a flat stream:

```
[HITL] Delete 47 files from /projects/archive — reply 1 to block, 2 to allow once
[STATUS] Cron job completed — 12 emails processed, 3 flagged for review
[EMAIL] New message from contact@example.com — subject: Partnership inquiry
```

This gives you scannable structure without needing platform-level threading. The reply-number convention from the Agent Engine (1 block / 2 allow once / 3 allow always) maps cleanly to this format.

> **Honest note:** If you need structured routing across multiple activity categories and you're setting up from scratch, Telegram's Forum Mode gives you significantly more visibility with less manual convention-building. WhatsApp is the right choice when your contacts or your own daily workflow is already there — not because it's the most flexible option for agent monitoring.

---

*These appendices cover setup, common failure points, and practical routing patterns. Platform APIs change — if a specific step doesn't match what you see in the console, the underlying concept is correct even if the exact UI has shifted.*

---

We genuinely hope this guide brings clarity so you can take action with confidence.

Good luck in all your OpenClaw endeavours. 🦞

**VaHive Systems Lab**
support@aivare.ai | [aivare.ai](https://aivare.ai)

---

**Stay updated:** If you register your email with the Gumroad store, you will automatically receive all future updates to this guide as they are released — free, forever.

---

## Updates & Changelog

All changes are timestamped so you can always see exactly what's new since your original download.

---

**March 2026 — v1.2**

- Updated all contact details to support@aivare.ai and aivare.ai
- Chapter 8 substantially expanded with MAGUS Guardian story and full feature comparison table for DSMC Agent Engine v2.0
- Added MAGUS v3.0 Zenodo reference to free tools section
- Added Appendix C: Telegram Setup — including Forum Mode / topic threading walkthrough
- Added Appendix D: LINE Setup — including webhook timeout behaviour and group-based routing
- Added Appendix E: WhatsApp Setup — including the 24-hour messaging window constraint and prefix routing convention
- Minor link and product name corrections throughout

---

**March 7, 2026 — v1.1**

Added **Chapter 7: Delegating Large Task Lists Without Silent Failures**

This chapter addresses the problem of agents going silent during long or overnight task runs — making solid progress on the first few items, then stopping without explanation. It covers:

- Why progress-reporting prompt instructions fail over time (same root cause as context drift — they live in transient history, not persistent state)
- A simple persistent `status.md` tracker that becomes part of your Rulebook
- The exact operational rule to add to `AGENTS.md` for forced, reliable progress updates
- A worked ❌/✅ example showing what a stalled overnight run looks like versus a tracked one
- How to connect it to the existing Active-State Discipline system from Chapters 4 and 5

Also updated: the "Taking the Next Step" link in Chapter 8, and minor footer cleanup.

---

*Future updates will be added here with clear dates. The guide will continue to receive real-world fixes drawn from community experience.*

---

*© 2026 VaHive Systems Lab. All rights reserved.*

*This document is free to share and distribute in its original, unmodified form. You may apply the frameworks, templates, and principles in your own projects and commercial work. Modification, rebranding, or resale of this document — in whole or in part, in any format — is not permitted without written permission from the author.*

*VaHive Systems Lab 2026*

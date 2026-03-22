# START HERE
## DSMC Minimal — Free Governance Layer for OpenClaw

**VaHive Systems Lab**
vahivesystemslab@gmail.com | [aivare.ai](https://aivare.ai)

---

**中文用户：** 将以下提示词复制到您的AI助手中，同时附上此文件，并告诉AI助手"请用中文回复我"。

**ผู้ใช้ภาษาไทย:** คัดลอกข้อความด้านล่างนี้ไปใส่ใน AI assistant ของคุณ แนบไฟล์นี้ไปด้วย และบอก AI ว่า "กรุณาตอบเป็นภาษาไทย"

---

Welcome. This zip contains 3 files — that's it. No installation, no
configuration files, no dependencies to install.

```
dsmc_minimal.py          ← drop into any Python agent
dsmc_minimal_sidecar.py  ← HTTP bridge for TypeScript / OpenClaw
TOKEN_EFFICIENCY.md      ← explains the token overhead problem in detail
```

You do not need any technical knowledge to get started. All you need to
do is copy the prompt below, open your AI assistant (Claude, ChatGPT, or
Gemini), paste the prompt, and attach this file (START-HERE.md) to the
message. Your AI assistant will guide you through the rest — one step at
a time — and will ask you for any other files it needs as you go.

---

## Your Setup Prompt

*Copy everything below this line and paste it to your AI assistant.
Attach this file (START-HERE.md) to the same message. Then send it.*

---

```
I just downloaded DSMC Minimal — a free governance layer for OpenClaw agents.
I have attached the START-HERE.md file from the zip.

The zip contains 3 files:
- dsmc_minimal.py
- dsmc_minimal_sidecar.py
- TOKEN_EFFICIENCY.md

There are zero dependencies — no pip installs required.

Please:
1. Ask me whether I am using a Python agent or a TypeScript / OpenClaw agent
2. Ask me what I am trying to fix — context drift, example contamination,
   token overhead, or something else

Then act as my implementation guide. Walk me through dropping these files
into my existing setup one step at a time. Give me one instruction, wait
for me to confirm it worked, then give me the next step.

Important notes for you:
- I may not be an experienced developer. Explain every step in plain
  language before I do it.
- The files are already in my folder — I do not need to create them.
- If you need to read any of the files during setup, ask me to attach
  them one at a time. Do not ask for all files at once.
- If I get stuck or confused at any point, I will tell you and you
  should re-explain that step differently before moving on.
- If at any point you cannot read attached files or are unable to
  proceed, tell me the exact words: "The LLM cannot read attachments"
  and I will give you the next step manually.

Please start by asking which type of agent I am using.
```

---

## What This Does (Plain Language)

Every time you send a message to your OpenClaw agent, this tool quietly
classifies it — is it a decision, a correction, a question, or just
thinking out loud? — and keeps a clean record of only the things that
actually matter.

That record gets injected into your agent's context on every call.
The agent always knows the current ground truth, no matter how long
the session runs.

The result: less drift, fewer correction cycles, lower token costs.

---

## Limitations

This is intentionally minimal. It uses pattern-matching only — no AI
call, no cost. It works in memory and resets when the process stops.
There is no persistence, no confidence scoring, no drift detection, and
no dashboard.

If you find yourself wanting those things, they exist in the full engine:
👉 [DSMC Agent Engine v3.0](https://puititiya.gumroad.com/l/dsmc-agent-engine)
Use code **AGENT20** for 20% off.

---

**Questions:** vahivesystemslab@gmail.com

*VaHive Systems Lab 2026 — MIT Licensed*

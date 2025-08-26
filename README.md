# Backlog Buddy — Agentic PM Copilot (GitHub Issues)

Turn **messy tickets** into **INVEST-quality** user stories and open **GitHub Issues** — in **one click**, with a human in the loop.

[![Made with Python](https://img.shields.io/badge/Python-3.11%2B-blue)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](#)
[![Agentic AI](https://img.shields.io/badge/Agentic-Plan%E2%86%92Tools%E2%86%92Draft%E2%86%92Reflect-green)](#)

---

## ✨ What it does

- **Run All**: Plan → **Use Tools** (similar tickets, metrics) → **Draft** story → **Reflect** (INVEST/clarity) → **Create GitHub Issue** (labels + checklist).
- **Advanced mode**: the same steps, one button at a time for transparency.
- **Outputs**: clear **User Story**, checkbox **Acceptance Criteria**, **labels**, lightweight **estimate** — all posted to **GitHub Issues**.

---

## 🧭 Why it matters (for leaders)

- **Faster triage**: cut Time-to-Ready Story (TTRS) by **40–60%** (target).
- **Consistent quality**: INVEST stories, testable ACs; fewer clarifying loops.
- **Traceable**: everything lands in **GitHub**, your system of record.
- **Governed**: human approval, style guide + rubric, PII redaction.

---

## 🚀 Quickstart

> **Prereqs**: Python 3.11+, Git, and (optionally) a provider key (OpenAI-compatible).  
> Run these from the project root (same folder as `app/ui.py`).

```bash
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# create your .env
cp .env.example .env 2>/dev/null || true


import os, streamlit as st, pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from tools.similar import SimilarSearch
from tools.metrics import summarize_metrics
from tools.github_api import create_issue
from app.agent import plan, draft, reflect, revise, validate_story, read_text

load_dotenv()
st.set_page_config(page_title="Backlog Buddy (Agentic)", layout="wide")
st.title("Backlog Buddy — Agentic PM Copilot (GitHub Issues)")

@st.cache_resource
def load_similar(path): return SimilarSearch(path)
def two_cols(a=1, b=1): return st.columns([a,b])

with st.sidebar:
    st.subheader("Data & Config")
    tickets_csv = st.text_input("Past tickets CSV", "data/past_tickets.csv")
    metrics_csv = st.text_input("Metrics CSV", "data/metrics.csv")
    area = st.text_input("Feature/Area", "Export")
    tags = st.text_input("Tags", "export,performance")
    labels_raw = st.text_input("GitHub Labels (comma)", "backlog,generated")
    labels = [l.strip() for l in labels_raw.split(",") if l.strip()]
    style = read_text("docs/style_guide.md") if Path("docs/style_guide.md").exists() else ""
    rubric = read_text("docs/rubric.md") if Path("docs/rubric.md").exists() else ""

left, right = two_cols()

with left:
    st.subheader("1) Paste a new ticket")
    title = st.text_input("Title", "Export fails for large CSV")
    body  = st.text_area("Body", "Users report export timing out beyond 50k rows on analytics page.")
    ticket_text = f"{title}\n{body}"

    if st.button("2) Plan tools"):
        st.session_state.plan = plan(ticket_text, area, tags)
    if "plan" in st.session_state:
        st.caption("Plan (LLM decided which tools to use)")
        st.json(st.session_state.plan)

    if st.button("3) Execute tools"):
        ss = load_similar(tickets_csv)
        st.session_state.similars = ss.topk(title + " " + body, k=3)
        st.session_state.metrics = summarize_metrics(metrics_csv, feature=area)
    if "similars" in st.session_state:
        st.caption("Similar tickets (TF-IDF search)")
        st.json(st.session_state.similars)
        st.caption("Usage metrics summary")
        st.json(st.session_state.metrics)

    if st.button("4) Draft story"):
        story = draft(ticket_text, st.session_state.get("similars", []),
                      st.session_state.get("metrics", {}), style)
        st.session_state.story = story
    if "story" in st.session_state:
        st.caption("Draft story (JSON)")
        st.json(st.session_state.story)

with right:
    if st.button("5) Reflect (self-review)"):
        st.session_state.reflect = reflect(st.session_state.get("story", {}), rubric)
    if "reflect" in st.session_state:
        st.caption("Reflection result")
        st.json(st.session_state.reflect)

    if st.button("6) Revise if needed"):
        ref = st.session_state.get("reflect", {})
        if ref.get("status") == "FAIL":
            fixed = revise(st.session_state["story"], ref.get("revisions",""))
            st.session_state.story = fixed
            st.success("Revised story to satisfy the rubric.")
        else:
            st.info("Reflection PASSED; no revision needed.")
        st.json(st.session_state["story"])

    if st.button("Run All (Plan → Tools → Draft → Reflect → Create)"):
        import time
        try:
            t0 = time.perf_counter()

            # Plan
            st.session_state.plan = plan(ticket_text, area, tags)

            # Tools
            ss = load_similar(tickets_csv)
            st.session_state.similars = ss.topk(title + " " + body, k=3)
            st.session_state.metrics = summarize_metrics(metrics_csv, feature=area)

            # Draft
            t1 = time.perf_counter()
            st.session_state.story = draft(
                ticket_text,
                st.session_state.get("similars", []),
                st.session_state.get("metrics", {}),
                style
            )
            t2 = time.perf_counter()

            # Reflect + optional Revise
            ref = reflect(st.session_state["story"], rubric)
            if ref.get("status") == "FAIL":
                st.session_state["story"] = revise(
                    st.session_state["story"],
                    ref.get("revisions", "")
                )

            # Create issue
            validated = validate_story(st.session_state["story"])
            ac_lines = "\n".join([f"- [ ] {ac}" for ac in validated.acceptance_criteria])
            body_md = f"""### User Story
{validated.user_story}

### Acceptance Criteria
{ac_lines}

### Notes
- Estimate: {validated.estimate_points}
- Labels: {", ".join([l for l in validated.labels])}
"""
            url = create_issue(
                validated.story_title,
                body_md,
                labels=labels + validated.labels
            )

            from app.log import log_run
            log_run(title, (t1 - t0) * 1000, (t2 - t1) * 1000, ref.get("status", "PASS"), url)

            st.success(f"Issue created: {url}")
            st.write(url)

        except Exception as e:
            st.error(f"Auto run failed: {e}")

    if st.button("7) Create GitHub Issue"):
        validated = validate_story(st.session_state["story"])
        ac_lines = "\n".join([f"- [ ] {ac}" for ac in validated.acceptance_criteria])
        body_md = f"""### User Story
{validated.user_story}

### Acceptance Criteria
{ac_lines}

### Notes
- Estimate: {validated.estimate_points}
- Labels: {", ".join([l for l in validated.labels])}
"""
        url = create_issue(validated.story_title, body_md, labels=labels + validated.labels)
        st.success(f"Issue created: {url}")
        st.write(url)

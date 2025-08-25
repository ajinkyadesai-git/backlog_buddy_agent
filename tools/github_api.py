import os, requests
from dotenv import load_dotenv

# Load .env and override any stale variables from the shell
load_dotenv(override=True)

def _cfg():
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GH_OWNER")
    repo  = os.getenv("GH_REPO")
    if not token:
        raise RuntimeError("GITHUB_TOKEN missing in .env")
    if not owner or not repo:
        raise RuntimeError(f"GH_OWNER/GH_REPO missing in .env (got owner={owner!r}, repo={repo!r})")
    base = f"https://api.github.com/repos/{owner}/{repo}"
    head = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    return base, head

def ensure_labels(names):
    if not names: return
    base, head = _cfg()
    r = requests.get(f"{base}/labels?per_page=100", headers=head)
    r.raise_for_status()
    existing = {lbl["name"].lower() for lbl in r.json()}
    for n in names:
        if n and n.strip().lower() not in existing:
            requests.post(
                f"{base}/labels",
                json={"name": n.strip(), "color": "0ea5e9"},
                headers=head
            ).raise_for_status()

def create_issue(title, body, labels=None, assignees=None):
    base, head = _cfg()
    ensure_labels(labels or [])
    payload = {"title": title, "body": body}
    if labels: payload["labels"] = [l.strip() for l in labels if l.strip()]
    if assignees: payload["assignees"] = assignees
    r = requests.post(f"{base}/issues", json=payload, headers=head)
    r.raise_for_status()
    return r.json()["html_url"]

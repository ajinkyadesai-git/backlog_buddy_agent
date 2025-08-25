import csv, os, time
FIELDS = ["ts","title","plan_ms","draft_ms","reflect_status","issue_url"]
def log_run(title, plan_ms, draft_ms, reflect_status, issue_url):
    new = not os.path.exists("runs.csv")
    with open("runs.csv","a",newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new: w.writeheader()
        w.writerow({"ts":int(time.time()),"title":title,"plan_ms":plan_ms,"draft_ms":draft_ms,
                    "reflect_status":reflect_status,"issue_url":issue_url})

import json, pathlib
from app.llm import llm_json
from app.models import StoryModel

PLAN_SYS = {"role":"system","content":"You are a senior PM agent. When asked to PLAN, return ONLY JSON with keys: tools:[{name,args}], rationale:string."}
DRAFT_SYS = {"role":"system","content":"You are a senior PM. Return ONLY story JSON matching schema: {story_title,user_story,acceptance_criteria[],labels[],estimate_points}."}
REFLECT_SYS = {"role":"system","content":"You are a strict reviewer. Return ONLY JSON. If pass: {\"status\":\"PASS\"}. If fail: {\"status\":\"FAIL\",\"revisions\":\"...\"}."}

def read_text(p: str) -> str:
    return pathlib.Path(p).read_text(encoding="utf-8")

def plan(ticket_text:str, area:str, tags:str):
    user = {"role":"user","content": f"Ticket:\n{ticket_text}\nArea:{area}\nTags:{tags}\nTools available:\n- similar_search(query)\n- summarize_metrics(feature)\nReturn JSON."}
    return llm_json([PLAN_SYS, user])

def draft(ticket_text:str, similars, metrics, style:str):
    user = {"role":"user","content": json.dumps({"instruction":"Create INVEST story JSON.","ticket": ticket_text,"tool_outputs": {"similars":similars, "metrics":metrics},"style_guide": style})}
    return llm_json([DRAFT_SYS, user])

def reflect(story_json:dict, rubric:str):
    user = {"role":"user","content": json.dumps({"story":story_json, "rubric":rubric})}
    return llm_json([REFLECT_SYS, user])

def revise(story_json:dict, revisions:str):
    user = {"role":"user","content": json.dumps({"revise":revisions, "story":story_json})}
    return llm_json([DRAFT_SYS, user])

def validate_story(story_dict:dict) -> StoryModel:
    return StoryModel(**story_dict)

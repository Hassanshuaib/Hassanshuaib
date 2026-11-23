#!/usr/bin/env python3
"""Summarise a stream-json transcript: which agents ran, what each read, which calculator calls and Skill invocations happened."""
import json, re, sys
from collections import defaultdict
calls = defaultdict(list); agents = {}; res = None
for line in open(sys.argv[1]):
    try: e = json.loads(line)
    except Exception: continue
    if e.get("type") == "assistant":
        par = e.get("parent_tool_use_id") or "MAIN"
        for c in e["message"].get("content", []):
            if c.get("type") != "tool_use": continue
            i = c["input"]
            if c["name"] == "Agent": agents[c["id"]] = i.get("subagent_type"); calls["MAIN"].append("Agent -> %s" % i.get("subagent_type")); continue
            if c["name"] == "Skill": d = "SKILL " + i.get("skill", "")
            elif c["name"] == "Read": d = "Read " + re.sub(r".*/(skills|board)/", r"\1/", i.get("file_path", ""))
            elif c["name"] == "Bash":
                cmd = i.get("command", ""); fn = re.findall(r"boardcalc\.py\"?\s+(\w+)", cmd) + re.findall(r"bc\.(\w+)\(", cmd)
                d = "Bash boardcalc:" + ",".join(sorted(set(fn))) if fn else "Bash " + cmd[:70].replace("\n", " ")
            elif c["name"] in ("Write", "Edit"): d = c["name"] + " " + re.sub(r".*/board/", "board/", i.get("file_path", ""))
            else: d = c["name"]
            calls[par].append(d)
    if e.get("type") == "result": res = e
for k, v in calls.items():
    print("==", "MAIN (chief of staff)" if k == "MAIN" else agents.get(k, k))
    for d in v: print("   ", d)
if res: print("COST_USD", round(res.get("total_cost_usd", 0), 2)); print("=== FINAL ===\n" + str(res.get("result")))

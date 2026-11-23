import json,sys
calls=[];res=None;sid=None
for l in open(sys.argv[1]):
    try: e=json.loads(l)
    except: continue
    if e.get("type")=="system" and e.get("subtype")=="init": sid=e.get("session_id"); agents=e.get("agents"); 
    if e.get("type")=="assistant":
        for c in e["message"].get("content",[]):
            if c.get("type")=="tool_use":
                i=c["input"]; parent=e.get("parent_tool_use_id")
                d=i.get("subagent_type") or i.get("skill") or i.get("file_path") or i.get("command") or i.get("pattern") or ""
                calls.append(("  sub>" if parent else "MAIN ")+c["name"]+": "+str(d)[:110])
    if e.get("type")=="result": res=e
print("session:",sid)
print("TOOL CALLS:"); [print(" ",c) for c in calls]
if res: print("cost_usd:",res.get("total_cost_usd"),"turns:",res.get("num_turns"),"dur_s:",round(res.get("duration_ms",0)/1000)); print("=== RESULT ===\n"+str(res.get("result")))

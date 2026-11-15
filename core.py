"""CSV quiz marking, submission register and transparent item analysis."""
import csv
import io
import math
DEMO={"answer_key":{"Q1":"B","Q2":"A","Q3":"D","Q4":"C","Q5":"B"},"pass_mark":50,"responses_csv":"student_id,name,Q1,Q2,Q3,Q4,Q5\nDEMO001,Demo Student 1,B,A,D,C,B\nDEMO002,Demo Student 2,A,A,D,B,B\nDEMO003,Demo Student 3,B,C,A,C,\nDEMO004,Demo Student 4,C,B,D,A,C\nDEMO005,Demo Student 5,B,A,D,C,A\n"}

def analyse(data):
    key=data["answer_key"]
    if not isinstance(key,dict) or not 1<=len(key)<=200: raise ValueError("Answer key must contain 1–200 questions.")
    normal={str(q).strip():str(a).strip().upper() for q,a in key.items()}
    if len(normal)!=len(key) or any(not q or q in ("student_id","name") or a not in "ABCD" or len(a)!=1 for q,a in normal.items()): raise ValueError("Question names must be unique and answers must be A, B, C or D.")
    passed=data.get("pass_mark",50)
    if isinstance(passed,bool): raise ValueError("Pass mark must be numeric.")
    passed=float(passed)
    if not math.isfinite(passed) or not 0<=passed<=100: raise ValueError("Pass mark must be between 0 and 100.")
    raw=data["responses_csv"]
    if not isinstance(raw,str) or len(raw)>900000: raise ValueError("CSV must be text shorter than 900 KB.")
    reader=csv.DictReader(io.StringIO(raw.lstrip("\ufeff")))
    headers=reader.fieldnames or []
    if len(headers)!=len(set(headers)): raise ValueError("Duplicate CSV columns are not allowed.")
    required={"student_id","name",*normal}
    if not required.issubset(headers): raise ValueError("Missing CSV columns: "+", ".join(sorted(required-set(headers))))
    marks=[]; seen=set(); counts={q:{a:0 for a in ("A","B","C","D","blank")} for q in normal}
    for row in reader:
        if len(marks)>=5000: raise ValueError("At most 5,000 responses are supported.")
        if None in row or any(v is None for v in row.values()): raise ValueError("Malformed CSV row: check the number of columns.")
        sid=row["student_id"].strip(); name=row["name"].strip()
        if not sid or not name: raise ValueError("Every response needs student_id and name.")
        if sid.casefold() in seen: raise ValueError("Duplicate student ID: "+sid+". Resolve duplicate submissions before marking.")
        seen.add(sid.casefold()); score=0
        for q,correct in normal.items():
            answer=row[q].strip().upper()
            if answer and answer not in ("A","B","C","D"): raise ValueError("Invalid answer for "+sid+" / "+q+". Use A–D or blank.")
            counts[q][answer or "blank"]+=1
            score+=answer==correct
        pct=round(score*100/len(normal),2)
        marks.append({"student_id":sid,"name":name,"score":score,"total":len(normal),"percentage":pct,"result":"Pass" if score*100/len(normal)>=passed else "Below pass mark","submission":"Received"})
    if not marks: raise ValueError("CSV contains no responses.")
    items=[]
    for q,a in normal.items():
        correct=counts[q][a]; pct=round(100*correct/len(marks),2)
        items.append({"question":q,"answer":a,"correct":correct,"correct_pct":pct,"blank":counts[q]["blank"],"review_flag":"Review teaching or item" if pct<40 else "Check for easy item" if pct>90 else "Typical range",**{k:counts[q][k] for k in "ABCD"}})
    avg=sum(r["score"] for r in marks)*100/(len(marks)*len(normal))
    return {"summary":[["Submissions",str(len(marks))],["Class average",format(avg,".1f")+"%"],["Pass rate",format(100*sum(r["result"]=="Pass" for r in marks)/len(marks),".1f")+"%"],["Questions",str(len(normal))]],"rows":marks,"items":items,"chart":{"labels":[r["question"] for r in items],"values":[r["correct_pct"] for r in items],"label":"Correct answers by question (%)","reference":None},"notes":["One mark per correct answer. Blank answers score zero; there is no negative marking. Pass classification uses the unrounded score.","The submission register records received responses only. It does not prove classroom attendance or identify absentees without a full class roster.","Review flags use illustrative 40% / 90% thresholds; they do not establish item validity. Real student records stay in this local app; do not commit them to GitHub."]}

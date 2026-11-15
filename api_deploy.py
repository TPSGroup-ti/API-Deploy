from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, json, os

app = FastAPI(title="API Deploy ของพ่อ")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FILE = "tokens.json"

def load():
    if not os.path.exists(FILE): return {}
    return json.load(open(FILE, encoding="utf-8"))
def save(d): json.dump(d, open(FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

# พ่อกรอก Token ในเว็บหน้าเดียว → มาที่นี่
@app.post("/tokens/add")
def add_token(name: str, token: str, base_url: str):
    data = load()
    key = name.replace(" ","_")
    data[key] = {"name": name, "token": token, "base_url": base_url}
    save(data)
    return {"ok": True, "my_api": f"/api/{key}/skills"}

# ดูรายการที่พ่อ Deploy แล้ว
@app.get("/tokens/list")
def list_tokens():
    return list(load().values())

# พ่อเรียก API ใหม่ ไม่ต้องใส่ Token แล้ว ระบบใส่ให้พ่อเอง
@app.get("/api/{name}/skills")
def proxy_skills(name: str):
    t = load().get(name)
    if not t: return {"error": "ไม่เจอ Token นี้ค่ะพ่อ"}
    r = requests.get(f"{t['base_url']}/skills", headers={"X-API-Key": t['token']}, timeout=10)
    return r.json()

# หน้าเช็คว่าระบบติดไหม
@app.get("/")
def home(): return {"ok": True, "system": "API Deploy ของพ่อ พร้อมใช้แล้วค่ะพ่อ"}

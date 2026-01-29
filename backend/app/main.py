import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import httpx
import json

HAPI_BASE = os.getenv("HAPI_BASE_URL", "http://hapi:8080")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
BASIC_USER = os.getenv("BASIC_AUTH_USER", "admin")
BASIC_PASS = os.getenv("BASIC_AUTH_PASS", "change_this_password")

security = HTTPBasic()
app = FastAPI(title="Med Agent Prototype")

with open("drugs.json", "r", encoding="utf-8") as f:
    DRUGS = json.load(f)

def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == BASIC_USER and credentials.password == BASIC_PASS):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

class PatientIn(BaseModel):
    given_name: str
    family_name: str
    age: int
    weight_kg: float = None
    allergies: list[str] = []
    current_medications: list[str] = []
    symptoms: str = ""

@app.post("/patient", dependencies=[Depends(check_basic_auth)])
async def create_patient(payload: PatientIn):
    patient_resource = {
        "resourceType": "Patient",
        "name": [{"family": payload.family_name, "given": [payload.given_name]}],
        "extension": [{"url": "age", "valueInteger": payload.age}]
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{HAPI_BASE}/Patient", json=patient_resource)
        r.raise_for_status()
        created = r.json()
    return {"patient": created}

@app.post("/draft-prescription", dependencies=[Depends(check_basic_auth)])
async def create_draft(patient_id: str, drug_name: str, dose: str = None):
    drug = next((d for d in DRUGS if d["drug_name_en"].lower() == drug_name.lower()), None)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found in dataset")

    med_request = {
        "resourceType": "MedicationRequest",
        "status": "draft",
        "medicationCodeableConcept": {
            "text": drug["drug_name_en"]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "dosageInstruction": [{
            "text": dose or drug.get("typical_dose", "Follow standard dosing")
        }],
        "note": [{"text": f"Draft generated using dataset source: {drug.get('source_url','unknown')}"}]
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{HAPI_BASE}/MedicationRequest", json=med_request)
        r.raise_for_status()
        created = r.json()

    return {"draft": created, "warnings": []}

@app.post("/explain", dependencies=[Depends(check_basic_auth)])
async def explain_text(text: str, lang: str = "en"):
    if not OPENAI_KEY:
        raise HTTPException(status_code=500, detail="OpenAI key not configured")
    import openai
    openai.api_key = OPENAI_KEY
    prompt = f"Explain this to a patient in {lang}:\n\n{text}"
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300
    )
    return {"explanation": resp.choices[0].message["content"]}

@app.post("/sign-draft", dependencies=[Depends(check_basic_auth)])
async def sign_draft(med_request_id: str):
    update_patch = {"status": "active"}
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{HAPI_BASE}/MedicationRequest/{med_request_id}", json=update_patch)
        r.raise_for_status()
        updated = r.json()
    return {"signed": updated}

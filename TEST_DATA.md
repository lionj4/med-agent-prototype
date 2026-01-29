After deployment, you can test endpoints:

1) Create patient:
curl -u admin:change_this_password -X POST "http://localhost:8000/patient" -H "Content-Type: application/json" -d '{"given_name":"Test","family_name":"User","age":30,"allergies":[]}' 

2) Create draft prescription:
curl -u admin:change_this_password -X POST "http://localhost:8000/draft-prescription?patient_id=<id>&drug_name=Paracetamol"

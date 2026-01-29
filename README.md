# Med Agent Prototype

Prototype for a clinician-in-the-loop medication draft generator (EN + AR).

Important: This prototype generates DRAFT MedicationRequest resources for review by a licensed clinician. It MUST NOT be used to issue prescriptions without clinician validation and local regulatory approval.

Quickstart (local):

1. Ensure Docker and Docker Compose are installed.
2. Clone the repo.
3. Copy `.env.example` to `.env` and set your environment variables.
4. Start services:
   docker-compose up --build

Services:
- hapi: HAPI FHIR server
- backend: FastAPI backend
- frontend: React app (EN/AR)
- apify: actor template (scraper)

Development notes and next steps:
- Add clinician authentication and audit logging for production.
- Integrate authoritative local drug lists for UAE before any clinical use.
- The LLM is used only for translation and patient-friendly explanations — not for clinical decision-making.

License: MIT

# Med Agent Prototype

Prototype for a clinician-in-the-loop medication draft generator (EN + AR).

Important: This prototype generates DRAFT MedicationRequest resources for review by a licensed clinician. It MUST NOT be used to issue prescriptions without clinician validation and local regulatory approval.

Quickstart (local):

1. Ensure Docker and Docker Compose are installed.
2. Clone the repo.
<<<<<<< HEAD
3. Copy `.env.example` to `.env` and set your environment variables.
=======
3. Copy `.env.example` to `.env` and set the following environment variables locally or in GitHub Secrets for CI/deploy:
   - HAPI_BASE_URL (default: http://hapi:8080)
   - OPENAI_API_KEY (if using OpenAI for translation/explanations)
   - APIFY_TOKEN (if running Apify actors from CI)
>>>>>>> origin/main
4. Start services:
   docker-compose up --build

Services:
<<<<<<< HEAD
- hapi: HAPI FHIR server
- backend: FastAPI backend
- frontend: React app (EN/AR)
- apify: actor template (scraper)
=======
- hapi: HAPI FHIR server (stores FHIR resources)
- backend: FastAPI backend exposing endpoints to create Patient and MedicationRequest drafts
- frontend: React app (EN/AR) for data entry and clinician review
- apify: actor template to scrape/normalize public drug data
>>>>>>> origin/main

Development notes and next steps:
- Add clinician authentication and audit logging for production.
- Integrate authoritative local drug lists for UAE before any clinical use.
- The LLM is used only for translation and patient-friendly explanations — not for clinical decision-making.

License: MIT
<<<<<<< HEAD
=======

---
>>>>>>> origin/main

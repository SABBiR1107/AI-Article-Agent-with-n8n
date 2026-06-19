# Assignment Submission Checklist - Module 21

Use this checklist to ensure that you have prepared all required deliverables before submitting your Module 21 Assignment.

---

## 💻 1. Codebase Deliverables
- [ ] **FastAPI Backend Code**
  - [ ] Located inside `backend/main.py`.
  - [ ] Includes input validation for email and URLs.
  - [ ] Generates a random session ID using `uuid`.
  - [ ] Includes `x-agent-secret` header matching `.env` file credentials.
  - [ ] CORS middleware added.
- [ ] **Streamlit Frontend Code**
  - [ ] Located inside `frontend/app.py`.
  - [ ] Form input validations included (prevents empty submits, checks formats).
  - [ ] Spinner shows correctly while waiting for backend response.
  - [ ] Displays success/error states including the session ID.
- [ ] **Package Requirements**
  - [ ] `backend/requirements.txt` is complete.
  - [ ] `frontend/requirements.txt` is complete.
- [ ] **Environment Template**
  - [ ] `backend/.env.example` contains placeholders (do not include production secret keys!).

---

## ⚙️ 2. n8n Workflow Configuration
- [ ] **n8n Workflow Export JSON**
  - [ ] Export your active workflow from n8n (`Workflow settings` -> `Export workflow to file`).
  - [ ] Save the exported JSON file in your project root or as requested by the grading system.
  - [ ] Confirm no personal API keys are embedded inside the JSON file.

---

## 📝 3. Documentation
- [ ] **README File**
  - [ ] Setup and run instructions for both frontend and backend.
  - [ ] Environment variable guide.
  - [ ] Architecture diagram and workflow explanation.
- [ ] **Video Demo Script**
  - [ ] Script outlines intro, demo, execution, output verification, and conclusion.

---

## 📹 4. Demo Video
- [ ] **Recorded 3-5 Minute Video**
  - [ ] Shows working Streamlit interface.
  - [ ] Shows FastAPI console or swagger docs.
  - [ ] Shows n8n workflow execution logs with green completion checkmarks.
  - [ ] Shows the Google Sheet log with the matching session UUID.
  - [ ] Shows the received Gmail summary matching the same session UUID.
  - [ ] Host the video on Loom, Google Drive, or YouTube (make sure sharing permissions are set to "Anyone with link can view").

---

## 📸 5. Required Screenshots
Prepare a folder named `screenshots/` or embed them into your submission as required:
- [ ] **Screenshot 1: Frontend Form** (Empty state or pre-filled inputs).
- [ ] **Screenshot 2: FastAPI Swagger Docs** (Showing `/process-article` and `/` endpoints).
- [ ] **Screenshot 3: n8n Workflow Canvas** (Visualizing the full node graph in n8n editor).
- [ ] **Screenshot 4: n8n Successful Execution Log** (Inside the "Executions" panel, showing green indicators).
- [ ] **Screenshot 5: Google Sheets Updated Row** (Showing columns with UUID and article summary).
- [ ] **Screenshot 6: Email Received** (Showing your inbox with the markdown-formatted summary email).

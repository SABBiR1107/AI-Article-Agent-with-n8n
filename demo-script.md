# Module 21 Assignment Demo Video Script

**Target Duration:** 3 to 5 minutes  
**Objective:** Walk through the architecture, show the working frontend & backend code, and demonstrate a successful end-to-end run (from frontend form submit to Google Sheets logging and email receipt).

---

## Video Segments Table

| Time | Segment | Visual / On Screen | Audio / Speaking Script |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:45** | **1. Project Introduction** | Show the **Streamlit Frontend** UI (`http://localhost:8501`) in a browser. Open your code editor briefly showing the file structure. | "Hello, my name is **[Your Name]**, and today I am demonstrating my Module 21 AI Agent Assignment. The goal of this project is to build an E2E article scraper and AI insights pipeline. The project is split into a Streamlit frontend, a FastAPI backend, and an active n8n automation workflow. As you can see, our frontend dashboard is clean, styled, and ready. Let's look at how the data flows." |
| **0:45 - 1:15** | **2. Architecture & Tech Stack** | Show the system flow diagram in the `README.md` file or point to the sidebar of your Streamlit app showing the Tech Stack list. | "For the tech stack, we are using Streamlit on the frontend, which connects to a local FastAPI server. The backend validates our inputs, generates a unique session UUID, and forwards it securely to our active n8n webhook. n8n then manages website scraping with Firecrawl, runs Groq AI models for summary and insight extraction, writes to Google Sheets, and sends a styled email." |
| **1:15 - 1:45** | **3. Code & Configuration Walkthrough** | Show `backend/main.py` and `backend/.env` file. Highlight the `x-agent-secret` header addition and UUID generation. | "Looking at the backend codebase, we use FastAPI for high performance. Inside our `POST /process-article` endpoint, we generate a unique UUID session ID, attach the secret header `x-agent-secret` from our `.env` file, and forward the request to n8n. If n8n succeeds, we return the session ID and n8n's parsed response to the user." |
| **1:45 - 2:30** | **4. Live Demo: Form Entry** | Switch back to the Streamlit app. Type in your email (e.g. `your-email@gmail.com`) and paste a valid article URL (e.g., a Wikipedia page or a blog post). Click **Process Article**. Show the spinner turning. | "Let's test this live! I'm entering my email address here, and I'll paste this Wikipedia page about Artificial Intelligence. When I click 'Process Article', our frontend triggers the FastAPI backend, which initiates the webhook. We see the loading spinner active, meaning our n8n agent is actively fetching the web content and prompting Groq to analyze it." |
| **2:30 - 3:15** | **5. n8n Workflow & Success Response** | Switch to the active **n8n canvas / execution tab** to show the successful run green checkmarks. Switch back to Streamlit to show the green success banner and JSON response. | "Switching to my n8n canvas, we can see the execution was successful! Every single node—from Webhook and Firecrawl to Groq, Google Sheets, and Email—has completed successfully. Back on our frontend, we see the green success banner and our generated session UUID. Let's verify the output channels." |
| **3:15 - 3:45** | **6. Output Verification** | 1. Show the Google Sheets window with the newly appended row.<br>2. Open your email inbox and show the formatted summary email you just received. | "First, checking my Google Sheets spreadsheet, we see a new row was successfully appended, logging the exact timestamp, our unique session UUID, the article URL, and the Groq-generated summaries and bulleted insights. Next, checking my email inbox, I've received a beautifully styled email featuring the article summary and key actionable takeaways." |
| **3:45 - 4:00** | **7. Summary & Conclusion** | Show the Streamlit UI again. | "This concludes my Module 21 assignment submission. The project successfully demonstrates standard full-stack integration with FastAPI, Streamlit, and high-level workflow automation engines like n8n. Thank you for watching!" |

---

## 💡 Quick Tips for Recording:
1. **Prepare Tabs in Advance:** Before recording, have these open in your browser tabs:
   - Tab 1: Streamlit Frontend (`http://localhost:8501`)
   - Tab 2: FastAPI Swagger Docs (`http://127.0.0.1:8000/docs`)
   - Tab 3: n8n Execution History (showing green checkmarks)
   - Tab 4: Google Sheets spreadsheet
   - Tab 5: Your Email inbox (empty or filtered to see the new message)
2. **Set up Local Servers:** Make sure both `uvicorn` and `streamlit` are running and tested before hitting record.
3. **Pace Yourself:** Speak clearly, pause briefly during loading spinners to show they are working, and draw attention to the generated UUID session ID so the grader can see it matches across the backend, Google Sheets, and email.

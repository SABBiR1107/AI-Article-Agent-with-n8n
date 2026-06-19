import streamlit as st
import requests
import re

# Page configuration
st.set_page_config(
    page_title="AI Article Agent with n8n",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Font style override */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header layout */
    .header-container {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }
    
    .header-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF2E93, #FF8A00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Sidebar branding */
    .sidebar-section {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    
    /* Submit button style */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF2E93 0%, #FF8A00 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(255, 46, 147, 0.25);
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #FF1A7D 0%, #E67E00 100%);
        box-shadow: 0 6px 20px rgba(255, 46, 147, 0.4);
        transform: translateY(-2px);
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(0);
    }
    
    /* Custom status display */
    .session-card {
        background-color: #0f172a;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #334155;
        font-family: monospace;
        color: #38bdf8;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with Assignment Context
with st.sidebar:
    st.markdown("### 📋 Module 21 Assignment")
    st.markdown("**AI Agent Project with n8n**")
    st.divider()
    
    st.markdown("#### 🔗 Tech Stack:")
    st.markdown("- **Frontend:** Streamlit")
    st.markdown("- **Backend:** FastAPI")
    st.markdown("- **Workflow:** n8n")
    st.markdown("- **LLM:** Groq (within n8n)")
    st.markdown("- **Scraper:** Firecrawl (within n8n)")
    st.markdown("- **Log Store:** Google Sheets (within n8n)")
    st.markdown("- **Notifier:** Gmail / SMTP (within n8n)")
    
    st.divider()
    st.markdown("#### 🔄 Data Flow:")
    st.code("""
[Frontend Form]
      │ (Email & URL)
      ▼
[FastAPI Backend] 
      │ (Auth + Session UUID)
      ▼
[n8n Webhook]
      │
      ├─► [Firecrawl Scrape]
      ├─► [Groq Summary/Insights]
      ├─► [Google Sheets Append]
      ├─► [Send Email]
      ▼
[Response to Backend]
      │
      ▼
[Frontend Render]
    """, language="text")

# Main Header Container
st.markdown("""
    <div class="header-container">
        <div class="header-title">🤖 AI Article Agent with n8n</div>
        <div class="header-subtitle">
            Enter an article link and your email. The agent scrapes the content, 
            extracts insights using Groq LLM, logs them to Google Sheets, and sends you a summary email.
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Form Container
st.markdown("### 📝 Enter Input Parameters")

# Setting up form layout
with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        email_input = st.text_input(
            "📧 Email Address", 
            placeholder="your.email@example.com",
            help="Your email to receive the generated article summary and insights."
        )
        
    with col2:
        url_input = st.text_input(
            "🔗 Article URL",
            placeholder="https://example.com/article-path",
            help="The URL of the webpage or blog post you want to scrape and analyze."
        )
        
    st.write("")  # spacing
    submit_btn = st.form_submit_button(label="🚀 Process Article")

# Regular expressions for validation
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
URL_REGEX = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"

if submit_btn:
    # 1. Frontend validation
    if not email_input.strip() or not url_input.strip():
        st.error("⚠️ Please fill in both fields before submitting.")
    elif not re.match(EMAIL_REGEX, email_input.strip()):
        st.error("⚠️ Please enter a valid email address.")
    elif not re.match(URL_REGEX, url_input.strip()):
        st.error("⚠️ Please enter a valid HTTP or HTTPS article URL.")
    else:
        # FastAPI backend endpoint
        BACKEND_URL = "http://localhost:8000/process-article"
        
        # Prepare requests
        payload = {
            "email": email_input.strip(),
            "article_url": url_input.strip()
        }
        
        # Render a processing spinner while request resolves
        with st.spinner("⚡ Triggering AI Agent workflow. Scraping website and running Groq AI analysis..."):
            try:
                response = requests.post(BACKEND_URL, json=payload, timeout=40.0)
                
                # Check status and parse response
                if response.status_code == 200:
                    data = response.json()
                    st.success("🎉 Article successfully processed by AI Agent & n8n workflow!")
                    
                    st.markdown("#### 🔑 Execution Metadata")
                    st.markdown(f"A unique session UUID has been generated for your request:")
                    st.markdown(f'<div class="session-card">Session ID: {data["session_id"]}</div>', unsafe_allow_html=True)
                    
                    # Display n8n result if available
                    n8n_result = data.get("n8n_response", {})
                    with st.expander("👁️ View Workflow Response Details", expanded=True):
                        st.json(n8n_result)
                    
                    st.info("📨 **Next Steps:** Check your email inbox for the markdown summary and check your Google Sheets log for the updated row!")
                
                # Handle validation errors returned by backend (HTTP 400)
                elif response.status_code == 400:
                    error_data = response.json()
                    st.error("❌ Invalid input detected by backend server:")
                    if "errors" in error_data:
                        for err in error_data["errors"]:
                            st.write(f"- {err}")
                    else:
                        st.write(error_data.get("detail", "Unknown validation error."))
                        
                # Handle other backend server issues
                else:
                    try:
                        err_msg = response.json().get("detail", response.text)
                    except Exception:
                        err_msg = response.text
                    st.error(f"❌ Backend Server Error (Status {response.status_code}):")
                    st.code(err_msg)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed! Could not connect to the backend server at `http://localhost:8000`.")
                st.info("💡 **Troubleshooting:** Make sure your FastAPI backend is running. Run `uvicorn main:app --reload` in your terminal inside the `backend` folder.")
            except requests.exceptions.Timeout:
                st.error("❌ Timeout Error! The request to the backend took too long to complete.")
                st.info("💡 **Troubleshooting:** Scraping and AI summarization inside n8n can take up to 20-30 seconds. Try testing with a faster loading webpage.")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {str(e)}")

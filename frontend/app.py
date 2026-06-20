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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Font style override */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Background enhancement */
    .stApp {
        background-color: #0B0F19;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(111, 66, 193, 0.08), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(0, 212, 255, 0.08), transparent 25%);
    }

    /* Header Container - Glassmorphism */
    .header-container {
        text-align: center;
        padding: 45px 20px;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 40px;
        animation: fadeInDown 0.8s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .header-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        letter-spacing: -1px;
    }

    .header-subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        font-weight: 400;
        line-height: 1.6;
        max-width: 650px;
        margin: 0 auto;
    }
    
    /* Input Fields Styling */
    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #00C6FF !important;
        box-shadow: 0 0 0 2px rgba(0, 198, 255, 0.2) !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
    }

    /* Primary Submit Button with Pulse Effect */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF2E93 0%, #FF8A00 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        width: 100%;
        margin-top: 12px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(255, 46, 147, 0.3);
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 30px rgba(255, 46, 147, 0.5);
        background: linear-gradient(135deg, #FF1A7D 0%, #E67E00 100%);
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(0) scale(0.98);
    }

    /* Sidebar Glass Branding */
    .sidebar-section {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }

    /* Custom Result Card Display */
    .session-card {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
        padding: 22px;
        border-radius: 14px;
        border-left: 4px solid #00C6FF;
        font-family: 'Courier New', Courier, monospace;
        color: #38BDF8;
        font-size: 1.1rem;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)



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

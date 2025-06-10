import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

# --- CONFIGURE GEMINI ---
genai.configure(api_key="AIzaSyDgcIL6ECjp6xW5AgaQg2NU-LAHS7gEBzM")  # Replace with your key
model = genai.GenerativeModel('gemini-2.0-flash')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Email Generator", layout="centered")
st.title("📧 AI Email Generator with Gemini")

st.markdown("### Step 1: Enter your prompt")
user_prompt = st.text_area("Describe what the email should say:")

st.markdown("### Step 2: Choose tone and format")
tone = st.selectbox("Select tone:", ["Formal", "Friendly", "Professional", "Empathetic"])
format_ = st.selectbox("Select format:", ["Apology", "Request", "Follow-up", "Thank You", "General"])

generate_btn = st.button("🚀 Generate Email")

# Use session_state to allow re-generation without retyping
if 'email_content' not in st.session_state:
    st.session_state.email_content = ""

# Function to generate email using Gemini
def generate_email(prompt, tone, format_):
    system_prompt = (
        f"Write an email in a {tone.lower()} tone. Format it as a {format_.lower()} email. "
        f"Here is the context: {prompt}"
    )
    response = model.generate_content(system_prompt)
    return response.text.strip()

# Generate email
if generate_btn and user_prompt:
    with st.spinner("Generating email..."):
        email = generate_email(user_prompt, tone, format_)
        st.session_state.email_content = email

# Show generated email
if st.session_state.email_content:
    st.markdown("### ✉️ Generated Email:")
    st.text_area("Your Email:", st.session_state.email_content, height=250)

    # --- Regenerate Button ---
    if st.button("♻️ Regenerate with different tone/format"):
        if user_prompt:
            st.session_state.email_content = generate_email(user_prompt, tone, format_)
        else:
            st.warning("Please enter email content first.")

    # --- Download PDF ---
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmp_path.name)
        return tmp_path.name

    pdf_path = create_pdf(st.session_state.email_content)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download as PDF",
            data=f,
            file_name="generated_email.pdf",
            mime="application/pdf"
        )

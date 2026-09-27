"""
8_Help.py -- Help Page
==========================
Step-by-step usage guide (FAQ style) covering: getting a Groq API
key, uploading documents, generating a proposal, editing before
download, and troubleshooting common errors.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st  # noqa: E402

from frontend.components.sidebar import render_sidebar_footer  # noqa: E402
from frontend.components.theme import inject_custom_css, render_hero_banner  # noqa: E402
from frontend.state.session_state import init_session_state  # noqa: E402

st.set_page_config(page_title="Help | ProcureAI", page_icon="❓", layout="wide")
inject_custom_css()
init_session_state()

render_hero_banner("❓ Help & FAQ", "Everything you need to get the system running and generating proposals")

with st.expander("🔑 How do I get a Groq API key?", expanded=True):
    st.markdown(
        "1. Go to [Groq Console](https://console.groq.com/keys).\n"
        "2. Sign in (Google account works) and click **Create API Key**.\n"
        "3. Copy the key and paste it into your project's `.env` file as:\n"
        "```\nGROQ_API_KEY=your_key_here\n```\n"
        "4. Restart the Streamlit app (`streamlit run frontend/app.py`).\n\n"
        "Note: document embeddings run **locally** (no API key needed) — only the "
        "proposal-field extraction step uses the Groq API."
    )

with st.expander("📤 How do I add documents to the Knowledge Base?"):
    st.markdown(
        "Go to **Upload Documents**, choose the correct category (SPR, Registration, Purchase Order, "
        "Tender, or Vendor), and drag & drop your PDF/DOCX files. You can upload as many as you like — "
        "there's no hard limit. Documents are automatically text-extracted, chunked, embedded, and "
        "added to ChromaDB — ready to use immediately."
    )

with st.expander("🧾 How do I generate a proposal?"):
    st.markdown(
        "1. Go to **Proposal Generator**.\n"
        "2. Select a proposal type (Honeywell, Dassault, Common Vendor, Foreign Vendor, or General Notice).\n"
        "3. Enter the relevant reference numbers (SPR, Registration, PO, Tender) — these scope the AI's search.\n"
        "4. Click **Retrieve & Generate**. Watch the live progress bar as the AI reads your documents.\n"
        "5. Review the retrieved fields in the editable form — fix any field marked `NA`.\n"
        "6. Click **Finalize & Export** to produce the final DOCX and PDF.\n"
        "7. Preview it, then use **Download DOCX** or **Download PDF**."
    )

with st.expander("✏️ Can I edit the proposal before downloading?"):
    st.markdown(
        "Yes. After field retrieval, every field appears in an editable form on the Proposal Generator "
        "page. Edit any value (including fields marked `NA`) before clicking **Finalize & Export** — "
        "your edits are what gets written into the final document."
    )

with st.expander("📄 Will the downloaded DOCX open in Microsoft Word?"):
    st.markdown(
        "Yes. The file is a standard Word `.docx` (OpenXML WordprocessingML) file. Once downloaded, "
        "your operating system will open it with whichever application is set as the default handler "
        "for `.docx` files — normally Microsoft Word."
    )

with st.expander("⚠️ Troubleshooting: 'Groq API Unreachable'"):
    st.markdown(
        "- Confirm `GROQ_API_KEY` is set correctly in your `.env` file.\n"
        "- Check your rate limit hasn't been exceeded at [Groq Console](https://console.groq.com).\n"
        "- Confirm you have an active internet connection (the LLM call needs one; document "
        "indexing/embeddings still work offline since they run locally)."
    )

with st.expander("⚠️ Troubleshooting: A field always shows 'NA'"):
    st.markdown(
        "- Make sure the relevant source document (e.g. the Purchase Order) has actually been uploaded "
        "to the correct category in the Knowledge Base.\n"
        "- Try re-uploading with a clearer reference number in the Proposal Generator form so the search "
        "can find the right document.\n"
        "- You can always fix the value manually in the editable field form before exporting."
    )

render_sidebar_footer()

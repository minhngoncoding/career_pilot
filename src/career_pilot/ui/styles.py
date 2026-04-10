import streamlit as st


def apply_styles():
    """Apply custom Streamlit styles."""
    st.markdown(
        """
    <style>
    /* Main background */
    .stApp {
        background-color: #fafafa;
    }
    
    /* Chat input */
    .stChatInput input {
        border-radius: 20px;
        padding: 12px 20px;
    }
    
    /* Welcome box */
    .welcome-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Custom button */
    .stButton > button {
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    
    /* Hide default header */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Footer */
    footer {
        visibility: hidden;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

import streamlit as st
from typing import Optional


def render_welcome():
    """Render welcome message and capabilities."""
    st.markdown(
        """
    <div style="text-align: center; padding: 20px;">
        <h1>👋 Career Pilot</h1>
        <h3>Your AI Career Assistant</h3>
        <p style="color: #666; font-size: 16px;">
            Tôi có thể giúp bạn với các vấn đề về sự nghiệp
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Capabilities
    st.markdown("### 🚀 Tôi có thể giúp gì?")

    capabilities = [
        (
            "📝",
            "**Phân tích CV**",
            "Đánh giá CV của bạn, chấm điểm và đề xuất cải thiện",
        ),
        ("💼", "**Tìm việc phù hợp**", "Match CV của bạn với các job phù hợp"),
        ("📚", "**Phân tích kỹ năng**", "Chỉ ra kỹ năng còn thiếu và lộ trình học tập"),
        ("📄", "**Tạo CV mới**", "Viết CV phù hợp với job description cụ thể"),
        (
            "🎤",
            "**Mock Interview**",
            "Tập phỏng vấn với tôi - hỏi và đánh giá câu trả lời",
        ),
    ]

    for icon, title, desc in capabilities:
        st.markdown(f"{icon} **{title}** - {desc}")

    st.markdown("---")
    st.markdown("### 💬 Bắt đầu chat")
    st.markdown("Hãy cho tôi biết bạn cần gì nhé!")


def render_mode_selector() -> Optional[str]:
    """Render mode selector in sidebar (hidden in single chat mode)."""
    with st.sidebar:
        st.markdown("### 📋 Các tính năng")
        st.markdown("""
        - 📝 Phân tích CV
        - 💼 Tìm việc
        - 📚 Skill Gap
        - 📄 Tạo CV
        - 🎤 Mock Interview
        """)
        st.markdown("---")
        st.markdown("### ⚙️ Cài đặt")
        if st.button("🗑️ Xóa cuộc trò chuyện"):
            st.session_state.messages = []
            st.rerun()


def render_file_uploader() -> Optional[str]:
    """Render file uploader for CV."""
    uploaded_file = st.file_uploader(
        "📎 Upload CV (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
    )
    if uploaded_file:
        return uploaded_file.name
    return None


def render_cv_input() -> str:
    """Render CV text input area."""
    tab1, tab2 = st.tabs(["📋 Dán CV", "📎 Upload file"])

    with tab1:
        cv_text = st.text_area(
            "Dán nội dung CV vào đây:", height=250, key="cv_text_input"
        )

    with tab2:
        file_result = render_file_uploader()
        cv_text = ""

    return cv_text


def render_chat_message(role: str, content: str):
    """Render a chat message bubble."""
    if role == "user":
        st.chat_message("user").markdown(content)
    else:
        st.chat_message("assistant").markdown(content)


def render_score_display(score: float, max_score: float = 10.0):
    """Render a visual score display."""
    percentage = (score / max_score) * 100

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Điểm", f"{score}/{max_score}")
    with col2:
        st.progress(percentage / 100)

        if score >= 8:
            st.success("Xuất sắc! 🎉")
        elif score >= 6:
            st.warning("Khá tốt! 👍")
        else:
            st.error("Cần cải thiện 📝")


def render_skill_badge(skill: str, level: str):
    """Render a skill badge."""
    colors = {
        "high": "green",
        "medium": "orange",
        "low": "red",
    }
    color = colors.get(level.lower(), "gray")
    st.markdown(f":{color}[{skill}]")


def render_roadmap_timeline(roadmap: dict):
    """Render a visual roadmap timeline."""
    for period, task in roadmap.items():
        st.markdown(f"**{period}**: {task}")


def render_interview_question(question: str):
    """Render an interview question card."""
    st.info(f"**Câu hỏi:** {question}")


def render_feedback_card(feedback: str, score: int):
    """Render a feedback card."""
    st.success(f"**Điểm:** {score}/10")
    st.markdown(f"**Phản hồi:** {feedback}")

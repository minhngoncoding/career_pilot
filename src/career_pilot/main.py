import gradio as gr
from career_pilot.graph import run_graph
import uuid


# Global state to track thread_id per session
session_threads = {}


def chat(message, history, thread_id_state: gr.State):
    """Handle chat messages with LangGraph."""
    # Get or create thread_id from state
    thread_id = thread_id_state if thread_id_state else str(uuid.uuid4())

    # MultimodalTextbox returns dict: {'text': '...', 'files': [...]}
    if isinstance(message, dict):
        text = message.get("text", "") or ""
        files = message.get("files", []) or []
    else:
        text = message or ""
        files = []

    if not text and not files:
        return "", history, thread_id_state

    response = run_graph(text, files=files, thread_id=thread_id)
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": response})
    return "", history, thread_id


def welcome():
    """Welcome message."""
    return """## 👋 Career Pilot - AI Career Assistant

I can help you with: CV analysis, job matching, skill gaps, CV generation, and mock interviews.

**Getting Started:** Tell me what you need! Example: "Analyze my CV" """


# Build Gradio interface
with gr.Blocks(title="Career Pilot") as demo:
    gr.Markdown(welcome())

    # Hidden state to store thread_id per session
    thread_id_state = gr.State(value=None)

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="💬 Chat",
                height=500,
            )

            with gr.Column(scale=1):
                msg = gr.MultimodalTextbox(
                    label="✍️ Type your message",
                    placeholder="Type your message here...",
                    lines=2,
                    file_types=[".pdf", ".docx", ".txt"],
                    file_count="multiple",
                    interactive=True,
                )
            file_input = gr.File(
                label="📎 Upload CV",
                file_types=[".pdf", ".docx", ".txt"],
                visible=False,
            )

            with gr.Row():
                submit_btn = gr.Button("📤 Send", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")

        with gr.Column(scale=1):
            gr.Markdown("### 🚀 Features")
            gr.Markdown("""
            - 📝 **CV Analysis** - Analyze & score your CV
            - 💼 **Job Matching** - Find suitable jobs
            - 📚 **Skill Gap** - Identify missing skills
            - 📄 **CV Generator** - Generate tailored CV
            - 🎤 **Mock Interview** - Practice with AI
            """)

    # Event handlers
    submit_btn.click(
        chat,
        inputs=[msg, chatbot, thread_id_state],
        outputs=[msg, chatbot, thread_id_state],
    )
    msg.submit(
        chat,
        inputs=[msg, chatbot, thread_id_state],
        outputs=[msg, chatbot, thread_id_state],
    )
    clear_btn.click(lambda: (None, [], None), outputs=[msg, chatbot, thread_id_state])


if __name__ == "__main__":
    import os

    os.environ.setdefault("PYTHONPATH", "src")
    demo.launch(server_port=7860)

import gradio as gr
from career_pilot.graph import run_graph


def chat(message, history):
    """Handle chat messages with LangGraph."""
    if not message:
        return "", history

    history.append((message, ""))
    response = run_graph(message)
    history[-1] = (message, response)
    return "", history


def welcome():
    """Welcome message."""
    return """## 👋 Career Pilot - AI Career Assistant

I can help you with: CV analysis, job matching, skill gaps, CV generation, and mock interviews.

**Getting Started:** Tell me what you need! Example: "Analyze my CV" """


# Build Gradio interface
with gr.Blocks(title="Career Pilot") as demo:
    gr.Markdown(welcome())

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="💬 Chat",
                height=500,
            )

            msg = gr.Textbox(
                label="✍️ Type your message",
                placeholder="Type your message here...",
                lines=3,
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
    submit_btn.click(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear_btn.click(lambda: (None, []), outputs=[msg, chatbot])


if __name__ == "__main__":
    import os

    os.environ.setdefault("PYTHONPATH", "src")
    demo.launch(server_port=7860)

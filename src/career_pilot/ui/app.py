import gradio as gr
from career_pilot.ui.styles import get_custom_css


def chat(message, history):
    """Handle chat messages."""
    # TODO: Call orchestrator to detect intent and route to agent
    response = "Tính năng đang được phát triển... Bạn thử lại sau nhé!"
    history.append((message, response))
    return "", history


def welcome():
    """Welcome message."""
    return """## 👋 Career Pilot - AI Career Assistant

Tôi có thể giúp bạn với các vấn đề về sự nghiệp:

### 🚀 Các tính năng:

| Icon | Tính năng | Mô tả |
|------|-----------|-------|
| 📝 | **Phân tích CV** | Đánh giá CV của bạn, chấm điểm và đề xuất cải thiện |
| 💼 | **Tìm việc phù hợp** | Match CV của bạn với các job phù hợp |
| 📚 | **Phân tích kỹ năng** | Chỉ ra kỹ năng còn thiếu và lộ trình học tập |
| 📄 | **Tạo CV mới** | Viết CV phù hợp với job description cụ thể |
| 🎤 | **Mock Interview** | Tập phỏng vấn với tôi - hỏi và đánh giá câu trả lời |

### 💬 Bắt đầu:
Hãy cho tôi biết bạn cần gì nhé! Ví dụ: "Phân tích CV giúp tôi" hoặc "Tìm việc Python Developer"
"""


# Build Gradio interface
with gr.Blocks(title="Career Pilot", theme=gr.themes.Soft()) as demo:
    gr.Markdown(welcome())

    chatbot = gr.Chatbot(
        label="💬 Cuộc trò chuyện",
        height=500,
        avatar=("🤖", "👤"),
    )

    msg = gr.Textbox(
        label="✍️ Nhập tin nhắn",
        placeholder="Nhập tin nhắn của bạn...",
        lines=3,
    )

    with gr.Row():
        submit_btn = gr.Button("📤 Gửi", variant="primary")
        clear_btn = gr.Button("🗑️ Xóa")

    # Event handlers
    submit_btn.click(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear_btn.click(lambda: (None, []), outputs=[msg, chatbot])


if __name__ == "__main__":
    demo.launch(server_port=7860)

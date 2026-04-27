#!/usr/bin/env python
"""Seed TopCV AI Engineer jobs from search results data."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from career_pilot.tools.vector_store import get_jd_store


# Job data extracted from web search results
JOBS_DATA = [
    {
        "job_title": "AI Engineer",
        "company": "Viettel Digital",
        "location": "Hà Nội",
        "salary": "Negotiable",
        "description": """Mô tả công việc:
- Các bài toán cần triển khai: eKYC, Robo Advisor, Chatbot CSKH, Chatbot hỗ trợ nghiệp vụ, Chatbot quy trình
- Xây dựng bộ KPI, cách đo để xác định mức độ thành công của chương trình, dịch vụ hay sản phẩm
- Đánh giá và tối ưu các mô hình opensource
- Thu thập dữ liệu, làm sạch dữ liệu
- Triển khai hạ tầng, cài đặt các platform, frameworks open source cho các ứng dụng AI
- Nghiên cứu tìm hiểu các công nghệ AI đáp ứng các bài toán kinh doanh

Yêu cầu:
- Có kinh nghiệm sử dụng Python
- Có kinh nghiệm Machine Learning, Deep Learning
- Kinh nghiệm với TensorFlow, PyTorch, Hugging Face"""
    },
    {
        "job_title": "AI Engineer",
        "company": "CÔNG TY TNHH THƯƠNG MẠI ĐIỆN TỬ GOBUY VIỆT NAM",
        "location": "Hồ Chí Minh",
        "salary": "25-40 triệu",
        "description": """We are seeking a skilled and motivated AI Engineer to join our innovative team at Talent Fusion.

Mô tả:
- Design, develop, and deploy AI-driven solutions to enhance recruitment platform
- Work with NLP, NLU, and Named Entity Recognition (NER)

Yêu cầu:
- Bachelor's or Master's degree in Computer Science, AI, Data Science
- At least 5 years of experience with AI technologies
- Proficiency in Python and frameworks: TensorFlow, PyTorch, Hugging Face
- Experience with NLP libraries: spaCy, NLTK, transformers
- Knowledge of transformer-based models: BERT, RoBERTa, GPT"""
    },
    {
        "job_title": "AI Engineer",
        "company": "VNPAY - Công ty CP Giải pháp Thanh toán Việt Nam",
        "location": "Hà Nội",
        "salary": "Negotiable",
        "description": """Mô tả công việc:
- Nghiên cứu và phát triển các nền tảng liên quan tới fraud detection cho ngân hàng, Ví điện tử
- Nghiên cứu và phát triển các thuật toán Xử lý tiếng nói: xoá/lọc nhiễu, nhận dạng tiếng nói, tổng hợp tiếng nói, nhận dạng người nói

Yêu cầu:
- Tốt nghiệp đại học chuyên ngành Công nghệ thông tin, Toán tin
- Kinh nghiệm AI/ML
- Công nghệ: Python, Machine Learning, Deep learning, Tensorflow/Pytorch, Computer Vision hoặc NLP"""
    },
    {
        "job_title": "AI Engineer",
        "company": "TECHVIFY SOFTWARE., JSC",
        "location": "Hà Nội",
        "salary": "Negotiable",
        "description": """Mô tả công việc:
- Develop and fine-tune machine learning models using structured and unstructured data
- Collaborate with stakeholders to understand business requirements and convert them into technical solutions
- Conduct data preprocessing, feature engineering, and model evaluation
- Integrate AI models into production environments with APIs or embedded systems
- Research and apply state-of-the-art AI/ML techniques (NLP, CV, time series)
- Optimize models for performance, scalability, and maintainability

Yêu cầu:
- Bachelor's or Master's degree in Computer Science, Data Science, AI
- 2-3 years of hands-on experience in developing and deploying ML/AI models
- Familiar with model evaluation techniques and metrics
- Understanding of RESTful APIs and basic software engineering practices"""
    },
    {
        "job_title": "AI Engineer (Computer Vision)",
        "company": "FTECH CO., LTD - CÔNG TY TNHH CÔNG NGHỆ GIA ĐÌNH",
        "location": "Đà Nẵng, Hà Nội",
        "salary": "Negotiable",
        "description": """Mô tả công việc:
- Implement and provide best-practices for maintainable software development
- Driving research and development of latest technologies in deep learning and computer vision
- Design and develop computer vision and ML algorithms: real-time object tracking, reconstruction, face tracking, depth estimation, GANs, VAEs, NeRF

Yêu cầu:
- Working well with English
- Solid coding skills (Python/C++) and good understanding of algorithms and data structure
- Familiar with deep learning frameworks: Tensorflow, Keras, PyTorch
- Hand-on experience with deep learning-based computer vision applications
- Knowledge of machine learning, deep learning, image processing"""
    },
    {
        "job_title": "Nhân Viên AI",
        "company": "Emtech Vietnam",
        "location": "Bắc Ninh",
        "salary": "12-16 triệu",
        "description": """Mô tả công việc:
- Lập trình, cấu hình hệ thống camera Machine Vision vào thiết bị tự động
- Xử lý ảnh công nghiệp (ưu tiên có kinh nghiệm với VisionPro, VisionPro Deep Learning)
- Làm các bài toán trong lĩnh vực Thị giác máy tính, xử lý hình ảnh
- Kết hợp với team AI tại Hàn Quốc và Việt Nam

Yêu cầu:
- Tối thiểu 01 năm kinh nghiệm trong lĩnh vực machine vision cho thiết bị tự động
- Thành thạo phần mềm xử lý ảnh công nghiệp (Cognex VisionPro / Deep Learning)
- Có khả năng lập trình C#, Python
- Kỹ năng làm việc nhóm tốt
- Biết tiếng Hàn là lợi thế"""
    },
    {
        "job_title": "Senior AI Engineer",
        "company": "TopCV",
        "location": "Hà Nội, Hồ Chí Minh",
        "salary": "Negotiable",
        "description": """Yêu cầu:
- Bachelor's degree in Computer Science, AI, Data Science or related
- 3+ years of experience in AI/ML development
- Proficiency in Python
- Experience with TensorFlow, PyTorch, or similar frameworks
- Knowledge of NLP, Computer Vision, or other AI domains"""
    },
    {
        "job_title": "AI Engineer (LLM/NLP)",
        "company": "TopCV",
        "location": "Hà Nội, Hồ Chí Minh",
        "salary": "Negotiable",
        "description": """Mô tả:
- Work on Large Language Models and NLP solutions
- Build chatbot and conversational AI systems
- Fine-tune and optimize LLM models

Yêu cầu:
- Experience with LLMs, transformers
- Strong Python skills
- Experience with LangChain, LlamaIndex is a plus
- Knowledge of RAG systems"""
    },
    {
        "job_title": "AI Platform Engineer",
        "company": "Remote",
        "location": "Remote",
        "salary": "Negotiable",
        "description": """Mô tả:
- Build and maintain AI platform infrastructure
- Deploy ML models at scale
- Work with MLOps tools and practices

Yêu cầu:
- Experience with cloud platforms (AWS, GCP, Azure)
- Knowledge of Docker, Kubernetes
- Experience with ML model deployment"""
    },
    {
        "job_title": "AI System Engineer",
        "company": "TopCV",
        "location": "Hà Nội",
        "salary": "Negotiable",
        "description": """Yêu cầu:
- Experience in AI system design
- Strong background in software engineering
- Knowledge of distributed systems"""
    },
]


def main():
    print("=" * 50)
    print("Seeding TopCV AI Engineer Jobs")
    print("=" * 50)
    
    jd_store = get_jd_store()
    
    print(f"\nAdding {len(JOBS_DATA)} jobs to database...")
    
    for i, job in enumerate(JOBS_DATA, 1):
        text = f"""
Job Title: {job['job_title']}
Company: {job['company']}
Location: {job['location']}
Salary: {job['salary']}
Description: {job['description']}
"""
        metadata = {
            "job_title": job['job_title'],
            "company": job['company'],
            "location": job['location'],
            "salary": job['salary'],
            "source": "topcv",
        }
        
        jd_store.add_jd(text, metadata)
        print(f"[{i}/{len(JOBS_DATA)}] ✅ Added: {job['job_title']} @ {job['company']}")
    
    print("\n" + "=" * 50)
    print(f"✅ Added {len(JOBS_DATA)} jobs to database")
    print(f"📊 Total in DB: {jd_store.count()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
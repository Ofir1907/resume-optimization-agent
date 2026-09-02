# AI Resume Tailoring Agent

An automated, LLM-powered resume optimization agent that dynamically tailors a candidate's master CV against a target job description. Built with **LangChain**, **Groq (LPU-accelerated LLMs)**, **Streamlit**, and dual compilation engines for **ATS-compliant PDF and Word (`.docx`)** formats.

---

## Features

- **Strict Role Integrity:** Employs domain-specific system prompts ensuring the LLM highlights real experience without hallucinating tools, skills, or credentials.
- **Dynamic Skill Re-ranking:** Automatically extracts, classifies, and maps relevant technical competencies into structured categories matching the job requirements.
- **Strict 1-Page Layout Fit:** Custom typography rules engineered in **ReportLab** to guarantee a pixel-perfect, single-page PDF with custom theme accents (`#F372AE`).
- **Zero-Glitch Encoding:** Built-in Unicode sanitization engine eliminating non-breaking hyphens, en-dashes, and special symbols that cause rendering bugs in legacy fonts.
- **Dual Format Export:** Instant parallel compilation to both **PDF** and **Word (`.docx`)** formats directly stored in session state.
- **Direct `.docx` Ingestion:** Upload an existing master resume directly without manual copy-pasting.

---

## Tech Stack

- **UI Framework:** Streamlit
- **LLM Orchestration:** LangChain Core, Groq API (`llama-3.3-70b-versatile` / `gpt-oss-20b`)
- **Data Validation & Parsing:** Pydantic V2 (`PydanticOutputParser`)
- **PDF Engine:** ReportLab
- **Word Engine:** python-docx

---

## Repository Structure

```text
├── app.py              # Streamlit UI & event loop
├── chain.py            # LangChain setup, prompt templates & Groq integration
├── schemas.py          # Pydantic data schemas for validation
├── pdf_builder.py      # ReportLab layout engine & Unicode sanitization
├── docs_builder.py     # python-docx generation pipeline
├── .env.example        # Environment variable template
├── .gitignore          # Sensitive and temporary file exclusions
└── requirements.txt    # Project dependencies
```
--- 
## Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/Ofir1907/resume-optimization-agent.git](https://github.com/Ofir1907/resume-optimization-agent.git)
cd resume-optimization-agent
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---
## How It Works
Upload Base Resume: Upload your comprehensive master resume in .docx format.

Target Job Input: Paste the target job description or requirements.

Structured LLM Inference: The prompt pipeline evaluates requirements, selects the top 3 relevant roles, rewrites bullet points for maximum impact, and formats the output through Pydantic schemas.

Compile & Download: Download the tailored result as a publication-ready PDF or an editable Word document without losing state on re-renders.
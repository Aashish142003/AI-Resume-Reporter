# SmartResume AI Report Tool 🎯

SmartResume AI is an intelligent CLI and Streamlit web application designed to help job seekers optimize their resumes against specific job descriptions. By leveraging state-of-the-art Large Language Models (LLMs) like Google Gemini and OpenAI, this tool analyzes your resume to identify missing keywords, highlight skill gaps, and provide actionable formatting feedback to improve your ATS (Applicant Tracking System) compatibility.

## 🚀 Features

*   **PDF text extraction**: Automatically parses and extracts text from your PDF resumes.
*   **AI-Powered Analysis**: Uses advanced AI (Google Gemini Pro / Flash or OpenAI GPT-4o-mini) to compare your resume against a target Job Description.
*   **ATS Match Score**: Provides a clear 1 to 5 Star Rating matching your profile to the role.
*   **Detailed Feedback**:
    *   Keyword Match percentage and terms found.
    *   Explicit Skill Gaps.
    *   Professional formatting critiques.
    *   Top actionable recommendations.
*   **Dual Interfaces**:
    *   **Premium Web UI** (Streamlit): A modern, theme-adaptive (Light/Dark mode) interface with a glassmorphism aesthetic.
    *   **CLI Interface**: Run analyses quickly from your terminal.
*   **Professional PDF Export**: Download your analysis report as a cleanly formatted `.pdf` document.

## 🛠️ Tech Stack

*   **Python 3**
*   **Streamlit** (Web Frontend)
*   **Google Generative AI SDK** `google-generativeai` (Gemini API access)
*   **OpenAI SDK** `openai` (GPT model access)
*   **PyPDF** `pypdf` (Resume parsing)
*   **FPDF2** `fpdf2` (PDF report generation)
*   **python-dotenv** (Environment variable management)

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aashish142003/AI-Resume-Reporter.git
    cd AI-Resume-Reporter
    ```

2.  **Install dependencies:**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## 🎮 How to Use

### Using the Web Interface (Streamlit)

This is the recommended, premium way to use the application.

1.  Start the app:
    ```bash
    streamlit run app.py
    ```
2.  Open your browser to the local URL provided (usually `http://localhost:8501`).
3.  Upload your PDF resume.
4.  Paste the Job Description.
5.  Click **"EXECUTE AI ANALYSIS"**.
6.  View your score and download the custom PDF report.

### Using the Command Line Interface (CLI)

1.  Place your resume PDF and job description text file in the project folder.
2.  Run the main script:
    ```bash
    python3 main.py --resume "your_resume.pdf" --jd "jd.txt"
    ```
3.  The report will be outputted to the console and saved as `resume_report.md`.

## 🤝 Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements.

## 📝 License

This project is open-source and available under the MIT License.

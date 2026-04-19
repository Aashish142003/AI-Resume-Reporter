import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResumeAnalyzer:
    def __init__(self, provider="gemini", api_key=None):
        self.provider = provider
        self.api_key = api_key
        
        if self.provider == "gemini":
            import google.generativeai as genai
            self.api_key = self.api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("Google API key not found. Set GOOGLE_API_KEY in .env.")
            genai.configure(api_key=self.api_key)
            # Using Flash-Lite as requested (matches available models)
            self.model = genai.GenerativeModel('gemini-flash-lite-latest')
        else:
            from openai import OpenAI
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env.")
            self.client = OpenAI(api_key=self.api_key)
            self.model_name = "gpt-4o-mini"

    def analyze(self, resume_text, job_description):
        """
        Analyzes the resume against the job description.
        """
        prompt = f"""
        You are an expert HR and Career Coach. Analyze the following resume against the provided Job Description (JD).
        
        ### Job Description:
        {job_description}
        
        ### Resume:
        {resume_text}
        
        ---
        Please provide a detailed Report including:
        0. **Overall Match Score**: Provide a single number between 1 and 5 representing the star rating (e.g., "Star Rating: 4/5").
        1. **Keyword Matching**: A percentage score and a list of matching keywords found.
        2. **Skill Gaps**: Identify key skills, tools, or certifications mentioned in the JD that are missing or weak in the resume.
        3. **Professional Formatting**: Critique the resume's clarity, structure, and professional tone.
        4. **Recommendations**: Top 3 actionable steps to improve the resume for this specific role.

        Return the report in Markdown format.
        IMPORTANT: Start the report with the line "Star Rating: X/5" where X is the score.
        """
        
        if self.provider == "gemini":
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error during Gemini analysis: {e}"
        else:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a professional career coach."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error during OpenAI analysis: {e}"

if __name__ == "__main__":
    # Quick test
    analyzer = ResumeAnalyzer(provider="gemini")
    print(f"Analyzer initialized for {analyzer.provider}")

import argparse
import os
from parser import extract_text_from_pdf
from model import ResumeAnalyzer

def main():
    parser = argparse.ArgumentParser(description="SmartResume AI Report Tool")
    parser.add_argument("--resume", required=True, help="Path to the PDF resume file")
    parser.add_argument("--jd", required=True, help="Path to the Job Description text file")
    parser.add_argument("--output", default="resume_report.md", help="Path to save the generated report")
    
    args = parser.parse_args()

    # 1. Extract text from Resume
    print(f"[*] Extracting text from {args.resume}...")
    resume_text = extract_text_from_pdf(args.resume)
    if not resume_text:
        print("[!] Failed to extract text from resume. Exiting.")
        return

    # 2. Read Job Description
    print(f"[*] Reading Job Description from {args.jd}...")
    try:
        with open(args.jd, 'r') as f:
            jd_text = f.read()
    except Exception as e:
        print(f"[!] Error reading JD file: {e}")
        return

    # 3. Analyze with AI
    print("[*] Analyzing resume against JD using AI...")
    try:
        analyzer = ResumeAnalyzer()
        report = analyzer.analyze(resume_text, jd_text)
    except Exception as e:
        print(f"[!] Analysis failed: {e}")
        return

    # 4. Save/Print Report
    print(f"[*] Analysis complete. Saving report to {args.output}...")
    with open(args.output, 'w') as f:
        f.write(report)
    
    print("\n--- Summary Report ---")
    print(report[:1000] + ("..." if len(report) > 1000 else ""))
    print("\n[+] Report saved successfully.")

if __name__ == "__main__":
    main()

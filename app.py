from flask import Flask, request, send_file, render_template_string
import google.generativeai as genai
import os
from weasyprint import HTML
import tempfile

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    api_key = request.headers.get('x-api-key')
    if api_key != "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":
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "Prompt required"}, 400

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        resume_text = response.text

        # Format resume as HTML
        html_template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 30px; }}
                h1 {{ color: #007bff; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <h1>Resume</h1>
            <pre>{resume_text}</pre>
        </body>
        </html>
        """

        # Create temp PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            HTML(string=html_template).write_pdf(tmp.name)
            tmp.flush()
            return send_file(tmp.name, as_attachment=True, download_name="resume.pdf")

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run()

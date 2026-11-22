from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        resume = request.files.get("resume")
        job_description = request.form.get("job_description", "")

        if not resume or resume.filename == "":
            return render_template(
                "index.html",
                error="Please upload your resume."
            )

        if not resume.filename.lower().endswith(".pdf"):
            return render_template(
                "index.html",
                error="Please upload a PDF file."
            )

        resume_text = extract_text_from_pdf(resume)

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="Could not extract text from the PDF."
            )

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matching_skills = [
            skill for skill in resume_skills
            if skill in job_skills
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_skills
        ]

        if job_skills:
            match_percentage = round(
                len(matching_skills) / len(job_skills) * 100
            )
        else:
            match_percentage = 0

        return render_template(
            "index.html",
            resume_skills=resume_skills,
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            match_percentage=match_percentage
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
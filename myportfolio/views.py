import os

from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages


@app.route("/")
def bio():
    return render_template("bio.html")


@app.route("/timeline")
def timeline():
    projects = [
        {
            "date": "07-10-2024",
            "url": "https://www.parchment.com/u/award/ef2f17b678782a1f5b2b442ea0231623",
            "title": "Georgia Tech Grad",
        },
        {
            "date": "07-01-2023",
            "url": "https://github.com/Delpen9/Ian-Dover-Personal-Website/tree/main",
            "title": "Portfolio Website",
        },
        {
            "date": "06-25-2023",
            "url": "https://github.com/Delpen9/Underwriting-Challenge",
            "title": "Underwriting Challenge",
        },
        {
            "date": "04-29-2023",
            "url": "https://github.com/Delpen9/optimization_methods_final",
            "title": "Optimization Methods",
        },
        {
            "date": "04-20-2023",
            "url": "https://github.com/Delpen9/data_compression_experiments",
            "title": "Data Compression",
        },
        {
            "date": "04-01-2023",
            "url": "https://github.com/Delpen9/lasso_ridge_elastic_group_optimization",
            "title": "Group Optimization",
        },
        {
            "date": "03-20-2023",
            "url": "https://github.com/Delpen9/Lagrangian-Optimization-Algorithms/tree/main",
            "title": "Descent Algorithms",
        },
    ]

    # Enforce title length
    for project in projects:
        if len(project["title"]) > 25:
            raise ValueError(f"Title '{project['title']}' exceeds 25 characters")

    return render_template("timeline.html", projects=projects)


def send_email(name, email, message):
    # Replace these with your actual email credentials
    sender_email = "iantdover@gmail.com"
    receiver_email = "iantdover@gmail.com"
    password = base64.b64decode("a2NvYyBueXpoIHdpeWQgY2R6cw==").decode('utf-8')

    # Set up the MIME
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "New Contact Form Submission"

    # Create the body of the message
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    msg.attach(MIMEText(body, "plain"))

    # Set up the server and send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        send_email(name, email, message)
        return redirect(
            url_for("contact")
        )  # Redirects back to the contact page on successful email send
    except Exception as e:
        print(e)  # Optionally print the error to the console or log it
        return redirect(
            url_for("contact")
        )  # Redirects back to the contact page on error


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/resume")
def resume():
    return send_from_directory("static/content/resume", "Ian_Dover_Resume.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)

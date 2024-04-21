from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def bio():
    return render_template("bio.html")


@app.route("/timeline")
def timeline():
    projects = [
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
    return render_template("timeline.html", projects=projects)

@app.route('/resume')
def resume():
    return send_from_directory('static/content/resume', 'ian_dover_resume_04_20_24.pdf')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)

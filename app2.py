from flask import Flask, render_template, request
import os
from analysis import analyze_csv

from flask import Flask, render_template
@app.route("/")
def index():
    return render_template("index.html")

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        preview, stats, numeric_cols = analyze_csv(path)

        return render_template(
            "report.html",
            preview=preview.to_html(),
            stats=stats,
            numeric_cols=numeric_cols
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

import os
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Exemplo de rota de upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csvfile']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Chamar análise
    from analysis import process_csv
    report = process_csv(filepath)

    return render_template('report.html', report=report)


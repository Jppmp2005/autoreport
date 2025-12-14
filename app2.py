from flask import Flask, render_template, request
import os
from analysis import analyze_csv  # usa apenas analyze_csv

# Criar app Flask
app = Flask(__name__)

# Pasta para uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota principal: landing page + upload CSV
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file") or request.files.get("csvfile")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado")

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        # Chama analyze_csv
        preview, stats, numeric_cols = analyze_csv(path)

        return render_template(
            "report.html",
            preview=preview.to_html(),
            stats=stats,
            numeric_cols=numeric_cols
        )

    return render_template("index.html")

# Rodar localmente (apenas para testes)
if __name__ == "__main__":
    app.run(debug=True)



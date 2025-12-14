from flask import Flask, render_template, request
import os
from analysis import analyze_csv, process_csv  # ajusta se necessário

# Criar app Flask
app = Flask(__name__)

# Configuração pasta de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota principal (index + upload CSV)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file") or request.files.get("csvfile")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado")

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        # Aqui chama a análise
        preview, stats, numeric_cols = analyze_csv(path)  # ou process_csv(path)
        
        return render_template(
            "report.html",
            preview=preview.to_html(),
            stats=stats,
            numeric_cols=numeric_cols
        )

    return render_template("index.html")

# Rodar localmente
if __name__ == "__main__":
    app.run(debug=True)



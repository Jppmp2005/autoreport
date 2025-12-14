from flask import Flask, render_template, request
import os
from analysis import analyze_csv  # Usa o nome real da tua função

# Criar app Flask
app = Flask(__name__)

# Pasta de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota principal (landing page + upload CSV)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Pega arquivo enviado
        file = request.files.get("file") or request.files.get("csvfile")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado")

        # Salva arquivo na pasta uploads
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        # Chama análise do CSV
        preview, stats, numeric_cols = analyze_csv(path)

        # Retorna report.html com dados
        return render_template(
            "report.html",
            preview=preview.to_html(),
            stats=stats,
            numeric_cols=numeric_cols
        )

    # GET: mostra a landing page
    return render_template("index.html")

# Roda localmente (apenas para testes)
if __name__ == "__main__":
    app.run(debug=True)




from flask import Flask, render_template, request, redirect
import os
from analysis import analyze_csv
import stripe

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chaves Stripe (usar chave de teste)
stripe.api_key = "SUA_CHAVE_SECRETA_TESTE"

# Landing page
@app.route("/")
def index():
    return render_template("index.html")

# Upload e geração do relatório
@app.route("/", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    preview, stats, numeric_cols, insights = analyze_csv(path)

    return render_template(
        "report.html",
        preview=preview.to_html(),
        stats=stats,
        numeric_cols=numeric_cols,
        insights=insights
    )

# Rota Stripe para pagamento
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 500,  # $5.00
                    "product_data": {
                        "name": "Relatório Inteligente",
                        "description": "Relatório de faltas e produtividade"
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://autoreport-d21k.onrender.com/success",
            cancel_url="https://autoreport-d21k.onrender.com/cancel",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

# Páginas de sucesso e cancelamento
@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

if __name__ == "__main__":
    app.run(debug=True)





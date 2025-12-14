from flask import Flask, render_template, request, jsonify
import os
from analysis import analyze_csv
import stripe

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'upload')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

stripe.api_key = "SUA_SECRET_KEY"
PUBLISHABLE_KEY = "SUA_PUBLISHABLE_KEY"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado")
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        preview, stats, numeric_cols, insights = analyze_csv(path)

        # Envia para report.html
        return render_template(
            "report.html",
            preview=preview.to_html(index=False),
            stats=stats,
            numeric_cols=numeric_cols,
            insights=insights
        )
    return render_template("index.html")

# Stripe
@app.route("/checkout")
def checkout():
    return render_template("checkout.html", key=PUBLISHABLE_KEY)

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Relatório Inteligente'},
                'unit_amount': 500,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://SEU_DOMINIO/success',
        cancel_url='https://SEU_DOMINIO/cancel',
    )
    return jsonify(id=session.id)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

if __name__ == "__main__":
    app.run(debug=True)



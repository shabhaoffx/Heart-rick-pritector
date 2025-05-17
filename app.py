from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Dummy login credentials
USERNAME = 'admin'
PASSWORD = 'password123'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Heart Risk Predictor</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #fdfbfb, #ebedee);
            padding: 40px;
        }
        .container {
            width: 400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0px 0px 20px #ccc;
            border-radius: 10px;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        input, select, button {
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        button {
            background: #007bff;
            color: white;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 6px;
            background-color: #f0f0f0;
            font-weight: bold;
            color: #333;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not logged_in %}
        <h2>Login</h2>
        <form method="POST" action="{{ url_for('login') }}">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        {% else %}
        <h2>Heart Risk Prediction</h2>
        <form method="POST" action="{{ url_for('predict') }}">
            <input type="number" name="age" placeholder="Age" min="0" required />
            <select name="sex" required>
                <option value="" disabled selected>Select sex</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>
            <select name="chest_pain" required>
                <option value="" disabled selected>Chest Pain Type</option>
                <option value="typical">Typical Angina</option>
                <option value="atypical">Atypical Angina</option>
                <option value="non-anginal">Non-anginal</option>
                <option value="asymptomatic">Asymptomatic</option>
            </select>
            <input type="number" name="blood_pressure" placeholder="Blood Pressure" required />
            <input type="number" name="cholesterol" placeholder="Cholesterol" required />
            <button type="submit">Predict</button>
        </form>
        {% if result %}
        <div class="result">{{ result }}</div>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == USERNAME and password == PASSWORD:
        return render_template_string(HTML_TEMPLATE, logged_in=True)
    else:
        return "<h3 style='text-align:center;color:red;'>Invalid credentials</h3>"

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    sex = request.form['sex']
    chest_pain = request.form['chest_pain']
    bp = int(request.form['blood_pressure'])
    chol = int(request.form['cholesterol'])

    # Simple logic for prediction
    risk_score = 0
    if age > 50: risk_score += 1
    if bp > 140: risk_score += 1
    if chol > 240: risk_score += 1
    if chest_pain == 'asymptomatic': risk_score += 1
    if sex == 'male': risk_score += 1

    result = "High Risk" if risk_score >= 3 else "Low Risk"
    message = f"Based on your inputs, your heart disease risk is: {result}"

    return render_template_string(HTML_TEMPLATE, logged_in=True, result=message)

if __name__ == '__main__':
    app.run(debug=True)
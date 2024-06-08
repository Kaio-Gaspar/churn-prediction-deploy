from flask import Flask, request, jsonify, render_template
from pickle import load

app = Flask(__name__)

# Load the machine learning model
with open("churn-prediction\pickle\model.pkl", "rb") as f:
    model = load(f)

@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict churn based on form inputs."""
    # Get the form data
    account_weeks = int(request.form['accountweeks'])
    contract_renewal = 1 if request.form.get('contractrenewal') == 'on' else 0
    data_plan = 1 if request.form.get('dataplan') == 'on' else 0
    data_usage = int(request.form['datausage'])
    cust_serv_calls = int(request.form['custservcalls'])
    day_mins = float(request.form['daymins'])
    day_calls = int(request.form['daycalls'])
    monthly_charge = float(request.form['monthlycharge'])
    overage_fee = float(request.form['Overagefee'])
    roam_mins = int(request.form['roammins'])

    # Print form data for debugging
    print("Account Weeks:", account_weeks)
    print("Contract Renewal:", contract_renewal)
    print("Data Plan:", data_plan)
    print("Data Usage:", data_usage)
    print("Cust Serv Calls:", cust_serv_calls)
    print("Day Mins:", day_mins)
    print("Day Calls:", day_calls)
    print("Monthly Charge:", monthly_charge)
    print("Overage fee:", overage_fee)
    print("Roam Mins:", roam_mins)

    # Make prediction using the model
    prediction = model.predict([[account_weeks, contract_renewal, data_plan, data_usage, cust_serv_calls,
                                  day_mins, day_calls, monthly_charge, overage_fee, roam_mins]])
    prediction = str(list(prediction)[0])  # Convert prediction to string

    # Print prediction for debugging
    print(prediction)

    # Render index.html template with prediction
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

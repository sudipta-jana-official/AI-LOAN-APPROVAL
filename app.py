from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loan_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# DATABASE MODEL
# =========================
class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personal Info
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    dob = db.Column(db.String(20))         # new
    state = db.Column(db.String(50))       # new
    district = db.Column(db.String(50))    # new
    city = db.Column(db.String(50))        # new
    pinCode = db.Column(db.String(10))     # new
    credit_score = db.Column(db.Integer)
    education = db.Column(db.String(50))
    dependents = db.Column(db.Integer)
    collateral = db.Column(db.String(100))
    existingLoans = db.Column(db.String(100))

    # Financial
    employmentStatus = db.Column(db.String(50))
    employerName = db.Column(db.String(100))
    businessName = db.Column(db.String(100))
    grossIncome = db.Column(db.Float)
    additionalIncome = db.Column(db.Float)
    savingsBalance = db.Column(db.Float)
    fixedDeposits = db.Column(db.Float)
    totalDebt = db.Column(db.Float)

    # Loan
    loanType = db.Column(db.String(50))
    loanAmount = db.Column(db.Float)
    loanTerm = db.Column(db.Integer)
    interestRate = db.Column(db.Float)
    loanPurpose = db.Column(db.String(100))
    monthlyEMI = db.Column(db.Float)
    totalInterest = db.Column(db.Float)
    totalPayment = db.Column(db.Float)

    # Prediction
    approved = db.Column(db.Boolean)
    probability = db.Column(db.Float)
    confidence = db.Column(db.Float)
    application_id = db.Column(db.String(50))
# =========================
# CREATE DATABASE
# =========================
with app.app_context():
    db.create_all()

# =========================
# ROUTES (PAGES)
# =========================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply')
def apply():
    return render_template('personal_info.html')

@app.route('/financial')
def financial():
    return render_template('financial_details.html')

@app.route('/loan')
def loan():
    return render_template('loan_details.html')

@app.route('/review')
def review():
    app_data = LoanApplication.query.order_by(LoanApplication.id.desc()).first()

    return render_template('review_submit.html', data=app_data)

@app.route('/result')
def result():
    return render_template('result.html')


# =========================
# SAVE PERSONAL INFO
# ========================
@app.route('/api/save-personal-info', methods=['POST'])
def save_personal():
    try:
        # Read JSON data (JS sends JSON)
        data = request.get_json()

        # Ensure credit score is numeric
        credit_score = int(data.get('credit_score') or 0)

        # Create new LoanApplication record
        app_data = LoanApplication(
            full_name=data.get('full_name', '').strip(),
            email=data.get('email', '').strip(),
            phone=data.get('phone', '').strip(),
            dob=data.get('dob', '').strip(),
            state=data.get('state', '').strip(),
            district=data.get('district', '').strip(),
            city=data.get('city', '').strip(),
            pinCode=data.get('pinCode', '').strip(),
            credit_score=credit_score
        )

        db.session.add(app_data)
        db.session.commit()

        # Store user ID in session for next steps
        session['user_id'] = app_data.id

        return jsonify({"success": True, "next_step": "/financial"})

    except Exception as e:
        print("Error saving personal info:", e)
        return jsonify({"success": False, "message": "Failed to save personal info. Please check all fields."})
    
# =========================
# SAVE FINANCIAL INFO
# ========================
@app.route('/api/save-financial-info', methods=['POST'])
def save_financial():
    try:
            data = request.get_json()
            user_id = session.get('user_id')

            if not user_id:
                return jsonify({"success": False, "error": "Session expired. Please start again."}), 400

            app_data = LoanApplication.query.get(user_id)
            if not app_data:
                return jsonify({"success": False, "error": "Application not found."}), 404

            # Employment Details
            app_data.employmentStatus = data.get('employmentStatus')
            app_data.employerName = data.get('employerName')
            app_data.jobTitle = data.get('jobTitle')
            app_data.workDuration = float(data.get('workDuration') or 0)
            app_data.monthlySalary = float(data.get('monthlySalary') or 0)
            app_data.salaryAccountBank = data.get('salaryAccountBank')
            app_data.form16 = data.get('form16')

            # Self-Employed / Business
            app_data.businessName = data.get('businessName')
            app_data.businessType = data.get('businessType')
            app_data.businessAge = float(data.get('businessAge') or 0)
            app_data.annualTurnover = float(data.get('annualTurnover') or 0)
            app_data.netProfit = float(data.get('netProfit') or 0)
            app_data.itrFiled = data.get('itrFiled')

            # Income
            app_data.grossIncome = float(data.get('grossIncome') or 0)
            app_data.additionalIncome = float(data.get('additionalIncome') or 0)
            app_data.incomeType = data.get('incomeType')

            # Expenses
            app_data.housingExpense = float(data.get('housingExpense') or 0)
            app_data.utilityExpense = float(data.get('utilityExpense') or 0)
            app_data.transportationExpense = float(data.get('transportationExpense') or 0)
            app_data.debtExpense = float(data.get('debtExpense') or 0)

            # Assets
            app_data.savingsBalance = float(data.get('savingsBalance') or 0)
            app_data.fixedDeposits = float(data.get('fixedDeposits') or 0)
            app_data.totalDebt = float(data.get('totalDebt') or 0)

            db.session.commit()

            return jsonify({"success": True, "next_step": "/loan"})
        
    except Exception as e:
            print("Error saving financial info:", e)
            return jsonify({"success": False, "error": "Server error while saving financial info."}), 500

# =========================
# SAVE LOAN INFO
# ========================

@app.route('/api/save-loan-details', methods=['POST'])
def save_loan_details():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"})

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"success": False, "error": "User not found in session"})

        # Fetch existing application
        app_data = LoanApplication.query.get(user_id)
        if not app_data:
            return jsonify({"success": False, "error": "Application data not found"})

        # --- Update fields safely ---
        app_data.loanType = data.get('loanType') or getattr(app_data, 'loanType', None)
        app_data.loanAmount = float(data.get('loanAmount') or getattr(app_data, 'loanAmount', 0))
        app_data.loanTerm = int(data.get('loanTerm') or getattr(app_data, 'loanTerm', 0))
        app_data.loanPurpose = data.get('loanPurpose') or getattr(app_data, 'loanPurpose', None)
        app_data.interestRate = float(data.get('interestRate') or getattr(app_data, 'interestRate', 0))
        app_data.processingFee = float(data.get('processingFee') or getattr(app_data, 'processingFee', 0))
        app_data.monthlyEMI = float(data.get('monthlyEMI') or getattr(app_data, 'monthlyEMI', 0))
        app_data.totalInterest = float(data.get('totalInterest') or getattr(app_data, 'totalInterest', 0))
        app_data.totalPayment = float(data.get('totalPayment') or getattr(app_data, 'totalPayment', 0))
        app_data.processingFeeAmount = float(data.get('processingFeeAmount') or getattr(app_data, 'processingFeeAmount', 0))

        db.session.commit()
        return jsonify({"success": True, "next_step": "/review"})

    except ValueError as ve:
        print("Value error while saving loan details:", ve)
        return jsonify({"success": False, "error": "Invalid numeric value in data"})
    except Exception as e:
        print("Unexpected error saving loan details:", e)
        return jsonify({"success": False, "error": "Failed to save loan details"})


# =========================
# GET DATA FOR REVIEW PAGE
# =========================
@app.route('/api/get-application-data')
def get_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "error": "No active session"})

    app_data = LoanApplication.query.get(user_id)
    if not app_data:
        return jsonify({"success": False, "error": "Application not found"})

    try:
        # We use .get() or getattr() to avoid crashes if a field is missing
        response_data = {
            "personal": {
                "full_name": app_data.full_name,
                "dob": app_data.dob, # JS handles the string formatting
                "email": app_data.email,
                "phone": app_data.phone,
                "city": app_data.city,
                "district": app_data.district,
                "state": app_data.state,
                "pin": app_data.pinCode,  # JS expects 'pin'
                "education": app_data.education,
                "dependents": app_data.dependents,
                "credit_score": app_data.credit_score
            },
            "financial": {
                "employmentStatus": app_data.employmentStatus, # Matches JS camelCase
                "employerName": app_data.employerName,
                "businessName": app_data.businessName,
                "grossIncome": app_data.grossIncome or 0,
                "additionalIncome": app_data.additionalIncome or 0,
                "savingsBalance": app_data.savingsBalance or 0,
                "fixedDeposits": app_data.fixedDeposits or 0,
                "totalDebt": app_data.totalDebt or 0
            },
            "loan": {
                "loanType": app_data.loanType,
                "loanAmount": app_data.loanAmount or 0,
                "loanTerm": app_data.loanTerm,
                "loanPurpose": app_data.loanPurpose,
                "interestRate": app_data.interestRate,
                "monthlyEMI": app_data.monthlyEMI,
                "totalInterest": app_data.totalInterest,
                "totalPayment": app_data.totalPayment,
                "existingLoans": app_data.existingLoans or "no",
                "collateral": app_data.collateral or "no"
            }
        }

        return jsonify({"success": True, "data": response_data})

    except Exception as e:
        print("Error fetching application data:", e)
        return jsonify({"success": False, "error": str(e)})
    

# =========================
# FINAL SUBMIT + AI LOGIC
# =========================
@app.route('/api/submit-application', methods=['POST'])
def submit_application():

    app_data = LoanApplication.query.get(session.get('user_id'))

    credit = app_data.credit_score or 600
    income = app_data.grossIncome or 0

    # SIMPLE AI LOGIC
    probability = min(1, (credit / 900) + (income / 1000000))
    approved = probability > 0.5
    confidence = round(probability * 100, 2)

    app_data.approved = approved
    app_data.probability = probability
    app_data.confidence = confidence
    app_data.application_id = "KBL" + str(random.randint(100000, 999999))

    db.session.commit()

    return jsonify({
        "success": True,
        "next_step": "/result"
    })


# =========================
# GET RESULT DATA
# =========================
@app.route('/api/get-prediction-result')
def get_result():

    app_data = LoanApplication.query.get(session.get('user_id'))

    if not app_data:
        return jsonify({"success": False})

    return jsonify({
        "success": True,
        "prediction": {
            "approved": app_data.approved,
            "probability": app_data.probability,
            "confidence": app_data.confidence,
            "application_id": app_data.application_id,
            "interest_rate": app_data.interestRate,
            "monthly_emi": app_data.monthlyEMI,
            "explanation": [
                "Good credit score" if app_data.credit_score > 650 else "Low credit score",
                "Stable income" if app_data.grossIncome > 300000 else "Low income"
            ]
        }
    })


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
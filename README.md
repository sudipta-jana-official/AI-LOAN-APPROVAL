# AI Loan Approval Prediction System

## Overview

The AI Loan Approval Prediction System is a machine learning-powered web application designed to predict whether a loan application is likely to be approved based on an applicant's financial and personal information. The project aims to assist financial institutions and users by providing fast, data-driven loan approval predictions through an intuitive web interface.

## Features

* Loan approval prediction using Machine Learning and Deep Learning models
* User-friendly web interface for data entry
* Real-time prediction results
* Input validation and error handling
* Confidence score generation
* Interactive dashboard with applicant details
* Responsive design for desktop and mobile devices

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Machine Learning

* PyTorch
* Scikit-learn
* Pandas
* NumPy

## Input Parameters

The model evaluates several factors, including:

* Age
* Gender
* Marital Status
* Annual Income
* Loan Amount
* Credit Score
* Number of Dependents
* Employment Status
* Existing Loan Count

## How It Works

1. Users enter loan applicant details through the web interface.
2. The Flask backend processes and validates the input data.
3. The trained AI model analyzes the information.
4. The system predicts whether the loan is likely to be approved or rejected.
5. Results are displayed along with prediction confidence and supporting insights.

## Project Structure

```text
AI-Loan-Approval/
│
├── app.py
├── model/
├── templates/
├── static/
├── requirements.txt
├── loan_model.pth
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd AI-Loan-Approval
pip install -r requirements.txt
python app.py
```

## Future Enhancements

* Explainable AI (XAI) integration
* Loan risk analysis dashboard
* Multiple model comparison
* Database integration
* User authentication and profile management

## Author

Sudipta Jana

B.Tech CSE (AI & ML)

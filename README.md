# FinHealth: Financial Prediction for African SMEs

![Status](https://img.shields.io/badge/Status-Live-success)
![Platform](https://img.shields.io/badge/Platform-Web-blue)
![Target](https://img.shields.io/badge/Target-African%20SMEs-orange)

**FinHealth** is an AI-driven platform that assesses the financial health and risk of Small and Medium Enterprises (SMEs) across Africa. Using survey-based data and machine learning models, it predicts business stability and creditworthiness to assist insurers, lenders, and policymakers in decision-making.  

🔗 **Live Demo:** [https://financial-prediction.vercel.app/](https://financial-prediction.vercel.app/)

---

## 🚀 Overview

Many African SMEs operate in the informal economy, making traditional credit assessment difficult. **FinHealth** bridges this gap by leveraging alternative data points—from operational habits to psychometric indicators—to categorize businesses into **Low, Medium, or High Risk**.

Key outputs include:  
* **Risk Status:** Business classification (e.g., Stable, At Risk)  
* **Health Score:** Quantitative indicator of financial robustness  

---

## 📋 Survey & Data

The platform’s predictive model is trained on SMEs from **Eswatini, Lesotho, Malawi, and Zimbabwe**. Data is collected via a comprehensive survey across five domains:

### 1️⃣ Demographics & Profile
* **Location:** Country of operation  
* **Owner Details:** Age, Gender  
* **Business Maturity:** Years in operation, COVID-19 essential service status  

### 2️⃣ Financial Metrics
* **Cash Flow:** Income, turnover, expenses  
* **Banking:** Mobile money, bank accounts, loans, cards  
* **Record Keeping:** Financial documentation frequency  

### 3️⃣ Risk & Insurance
* **Insurance Uptake:** Motor, medical, funeral, business  
* **Perception:** Trust and affordability of insurance  
* **Security:** Risk assessments (e.g., theft of stock)  

### 4️⃣ Psychometrics & Attitude
* **Outlook:** Confidence in business environment  
* **Compliance:** Attitude toward tax obligations  
* **Satisfaction:** Current business achievement  

### 5️⃣ Operational Habits
* **Technology:** Mobile usage, online banking  
* **Credit Practices:** Offering credit to customers  
* **Funding Sources:** Reliance on informal lenders or savings  

---

## 🛠️ Features

* **Interactive Survey:** Dynamic questionnaire for SMEs  
* **Real-time Predictions:** Instant financial risk classification  
* **Dashboard Analytics:** Visual insights (debt ratios, growth potential)  
* **Mobile Responsive:** Accessible on any device  

---

## 📂 Project Structure

```bash
financial-prediction/
├── data/               # Anonymized datasets for training
├── models/             # Pickled machine learning models
├── src/                # Application source code
├── static/             # Assets: CSS, images, JS
├── templates/          # HTML templates for survey & dashboard
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
````

---

## 🔧 Installation & Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/financial-prediction.git
cd financial-prediction
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python app.py
```

4. **Open in browser**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🤝 Contributing

Contributions are welcome! Submit a Pull Request with improvements or bug fixes.

---


*Built with ❤️ to empower African SMEs.*

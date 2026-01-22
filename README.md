# FinHealth - Financial Health Prediction for Southern African SMEs

*Empowering Small & Medium Enterprises through AI-driven financial health assessment and risk prediction*

![Financial Health Dashboard](https://img.shields.io/badge/SMEs_Analyzed-9,618-brightgreen) ![Countries Covered](https://img.shields.io/badge/Countries-4-blue) ![Model Accuracy](https://img.shields.io/badge/Model_Accuracy-85%25-orange) ![Coverage](https://img.shields.io/badge/Insurance_Coverage-3%25-red)

## 🌍 **The Critical Challenge**

Small and Medium Enterprises (SMEs) form the backbone of Southern African economies, yet **65.3% of businesses** in our comprehensive study are classified as high financial risk. This represents a massive economic vulnerability affecting millions of entrepreneurs across Eswatini, Zimbabwe, Malawi, and Lesotho.

### **Key Findings from 9,618 Real SME Businesses:**

| Critical Gap | Current State | Impact |
|--------------|---------------|---------|
| **Financial Health Crisis** | Only 4.9% achieve high financial health | Economic instability for 95.1% of SMEs |
| **Insurance Protection Gap** | 3% have business insurance | 97% vulnerable to business risks |
| **Tax Compliance Challenge** | 13% comply with income tax | Lost government revenue & business legitimacy |
| **Digital Payment Success** | 50.7% use mobile money | Strong foundation for financial inclusion |
| **Income Inequality** | 5x income gap between healthy vs. struggling businesses | Systemic wealth disparity |

## 🎯 **How This Study Transforms SME Support**

### **For Small & Medium Enterprises:**
- **Early Warning System**: Identify financial health risks before they become critical
- **Personalized Recommendations**: Data-driven advice tailored to each business's unique situation
- **Benchmarking**: Compare performance against 9,618+ similar businesses across 4 countries
- **Growth Pathway**: Clear indicators of success factors (tax compliance, insurance, digital adoption)
- **Access to Capital**: Improved risk profiles can unlock better financing opportunities

### **For Insurance Companies & Financial Institutions:**
- **Risk Assessment Automation**: ML-powered evaluation replacing manual underwriting processes
- **Market Opportunity Identification**: 97% of SMEs lack insurance - massive untapped market
- **Premium Optimization**: Data-driven pricing based on actual risk factors, not assumptions
- **Portfolio Management**: Real-time monitoring of client financial health trajectories
- **Regulatory Compliance**: Standardized risk categorization supporting prudential requirements

### **For Policymakers & Development Organizations:**
- **Evidence-Based Policy**: Real data from 9,618 businesses informing SME support programs
- **Resource Allocation**: Target interventions where they're most needed (tax compliance, insurance education)
- **Economic Planning**: Understanding the 65.3% high-risk business landscape for strategic planning
- **Financial Inclusion**: Building on 50.7% mobile money adoption for broader financial services

## � Data Attribution & Licensing

### 🏛️ **Dataset Source & Rights**
This project uses data from a Zindi Africa competition focusing on Small and Medium Enterprises (SMEs) financial health prediction across Southern African countries.

**📋 Licensing & Compliance:**
- **Data License**: [Creative Commons Attribution–ShareAlike 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
- **Competition Rules**: [Zindi Competition Rules](https://zindi.africa/rules)

**✅ Compliance Measures:**
- ✅ Data source properly credited with required attribution
- ✅ License terms followed and linked as required by CC BY-SA 4.0
- ✅ Original training data removed to prevent redistribution during active competition
- ✅ Synthetic dummy data generated for development purposes
- ✅ Pre-trained model ensures functionality while maintaining legal compliance

**🙏 Acknowledgments:**
- **Zindi Africa**: For hosting the competition and providing access to this valuable dataset
- **Competition Organizers**: For creating and curating this comprehensive SME financial health dataset
- **Data Contributors**: Who enabled this research through the generous CC BY-SA 4.0 licensing
- **SME Business Owners**: Who participated in the original data collection across 4 countries

## �📊 **Research Impact & Scope**

This study represents the most comprehensive SME financial health analysis in Southern Africa:

### **Geographic Coverage**
- 🇸🇿 **Eswatini**: 2,674 businesses (27.8%)
- 🇿🇼 **Zimbabwe**: 2,612 businesses (27.2%)
- 🇲🇼 **Malawi**: 2,388 businesses (24.8%)
- 🇱🇸 **Lesotho**: 1,944 businesses (20.2%)

### **Critical Success Factors Identified**
| Factor | Low Risk Businesses | High Risk Businesses | Impact Factor |
|--------|-------------------|---------------------|---------------|
| **Average Income** | $882,802 | $254,095 | **5x difference** |
| **Tax Compliance** | 44.7% | 8.8% | **5x higher** |
| **Insurance Coverage** | 21.9% | 0% | **Infinite difference** |
| **Mobile Money Usage** | 73.0% | 46.3% | **1.6x higher** |

## 🚀 **Technology Stack & Features**

### **Frontend Application**
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with responsive design
- **Features**: 
  - Interactive 16-question financial health survey
  - Real-time ML predictions with confidence scores
  - Data visualization dashboards with actual dataset insights
  - Personalized recommendations based on risk assessment

### **Backend API**
- **ML Framework**: Scikit-learn with Random Forest classification
- **API**: Flask with CORS support for seamless integration
- **Data Processing**: Pandas for comprehensive data analysis
- **Model Performance**: 85% accuracy across 17 key financial indicators

### **Key Application Features**

1. **📋 Comprehensive Survey** 
   - 16 questions across 5 categories (demographics, financial, insurance, attitudes, operations)
   - Aligned with actual dataset variables for accurate predictions

2. **🤖 AI-Powered Assessment**
   - Random Forest model trained on 9,618 real business records
   - Real-time financial health categorization (Low/Medium/High risk)
   - Confidence scoring for prediction reliability

3. **📈 Data-Driven Insights**
   - Interactive charts showing regional business health trends
   - Comparative analysis across countries and risk categories
   - Success factor identification for business improvement

4. **💼 Business Intelligence**
   - Risk assessment automation for insurers
   - Portfolio management tools for financial institutions
   - Policy guidance based on real market data

## 🛠 **Getting Started**

### **Prerequisites**
- Node.js 18.17 or later
- Python 3.8+ with pip
- Git

### **Quick Start**

1. **Clone and Setup**
   ```bash
   git clone [repository-url]
   cd financial-prediction
   npm install
   ```

2. **Start Backend API**
   ```bash
   cd backend
   pip install -r requirements.txt
   python start_api.py
   ```

3. **Start Frontend**
   ```bash
   npm run dev
   ```

4. **Access Application**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:5000](http://localhost:5000)

### **API Endpoints**
- `GET /api/health` - Service health check
- `POST /api/predict` - Submit survey for ML prediction
- `POST /api/train` - Retrain model with new data

## 📈 **Real-World Impact Potential**

### **Economic Development**
- **SME Survival**: Early intervention for 65.3% of high-risk businesses
- **Financial Inclusion**: Build on 50.7% mobile money foundation
- **Government Revenue**: Improve 13% tax compliance rate through targeted support

### **Insurance Industry Transformation**
- **Market Expansion**: Address 97% uninsured SME market
- **Risk Management**: Data-driven underwriting reducing default rates
- **Product Innovation**: Tailored insurance products based on actual risk profiles

### **Research & Policy Innovation**
- **Evidence-Based Decisions**: Replace assumptions with data from 9,618 businesses
- **Regional Cooperation**: Cross-border insights across 4 Southern African countries
- **Sustainable Development**: Support UN SDG goals for economic growth and financial inclusion

## 🤝 **Contributing to SME Development**

This open-source project welcomes contributions from:
- **Researchers**: Expand dataset coverage and analytical depth
- **Developers**: Enhance ML models and user experience
- **Policymakers**: Integrate insights into SME support programs
- **Financial Institutions**: Pilot risk assessment automation
- **SME Organizations**: Provide feedback for business-relevant features

## 📄 **License & Citation**

This project is open source and available under MIT License.

**Cite this work:**
```
FinHealth SME Financial Health Prediction Platform (2026)
Southern African SME Risk Assessment Study
Dataset: 9,618 businesses across Eswatini, Zimbabwe, Malawi, Lesotho
```

---

*Transforming SME financial health assessment from guesswork to evidence-based insights, one prediction at a time.*

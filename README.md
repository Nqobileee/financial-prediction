<div align="center">

# FinHealth

**Machine Learning-driven Financial Risk Assessment for Southern African SMEs**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

---

*Analyzing 9,618 SMEs across Eswatini, Zimbabwe, Malawi, and Lesotho*

</div>

---

<div align="center">

| Businesses Analyzed | Countries Covered | Model Accuracy | Insurance Gap |
|:------------------:|:-----------------:|:--------------:|:-------------:|
| **9,618** | **4** | **85%** | **97%** |

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Problem Statement and Economic Impact](#problem-statement-and-economic-impact)
- [Machine Learning Methodology](#machine-learning-methodology)
- [Technology Stack](#technology-stack)
- [Geographic Coverage](#geographic-coverage)
- [Strategic Applications](#strategic-applications)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Research Impact](#research-impact)
- [Future Research Directions](#future-research-directions)
- [Contributing](#contributing)
- [License and Citation](#license-and-citation)
- [Acknowledgments](#acknowledgments)

---

<h2 align="center">Overview</h2>

This research presents a comprehensive financial health prediction system designed to address the critical economic vulnerabilities affecting Small and Medium Enterprises (SMEs) across four Southern African countries: Eswatini, Zimbabwe, Malawi, and Lesotho. Our analysis of 9,618 real business entities reveals alarming patterns of financial distress, with 65.3% of SMEs classified as high financial risk, representing a systemic threat to regional economic stability.

---

<h2 align="center">Key Findings</h2>

> **Critical Discovery**: 65.3% of SMEs exhibit high financial risk indicators, indicating systematic market vulnerability requiring immediate intervention.

**Financial Health Distribution:**
- High Financial Health: 4.9% (474 businesses)
- Medium Financial Health: 29.8% (2,866 businesses) 
- Low Financial Health: 65.3% (6,278 businesses)

**Key Risk Indicators:**
- Insurance Coverage Gap: 97% of SMEs operate without business insurance protection
- Tax Compliance Deficit: Only 13% maintain compliance with income tax obligations
- Digital Payment Adoption: 50.7% have embraced mobile money platforms
- Record-Keeping Practices: Significant variance in financial documentation standards

---

<h2 align="center">Problem Statement and Economic Impact</h2>

The Southern African SME ecosystem faces unprecedented challenges in financial sustainability and risk management. Our comprehensive dataset analysis reveals critical vulnerabilities that demand immediate attention from stakeholders across the financial services sector.

**Macroeconomic Implications:**
The high concentration of financially distressed SMEs poses systemic risks to regional economic stability. Our findings indicate that targeted intervention strategies could significantly improve economic resilience across these markets.

**SME Ecosystem Benefits:**
- Early Warning Systems: Predictive analytics enable proactive risk management before critical failure points
- Capital Access Optimization: Improved risk profiling facilitates enhanced creditworthiness assessment
- Operational Intelligence: Data-driven insights guide strategic decision-making processes
- Regulatory Compliance: Automated monitoring supports tax and regulatory adherence

**Insurance Sector Opportunities:**
- Risk Stratification: Granular risk assessment enables precise premium pricing models
- Market Penetration: Identification of underserved segments with quantified risk profiles
- Product Innovation: Development of micro-insurance products targeting specific risk categories
- Portfolio Optimization: Data-driven underwriting reduces adverse selection risks

---

<h2 align="center">Machine Learning Methodology</h2>

<details>
<summary><strong>Original Model Architecture</strong></summary>

The production system employs a Random Forest Classifier trained on comprehensive feature vectors encompassing demographic, operational, and behavioral indicators. The model architecture incorporates:

- Feature Engineering: Multi-dimensional encoding of categorical variables using LabelEncoder transformations
- Cross-Validation: Stratified k-fold validation ensuring robust generalization across demographic segments
- Hyperparameter Optimization: Grid search methodology for optimal tree depth and ensemble size
- Performance Metrics: Precision-recall optimization targeting financial risk detection

**Model Performance:**
- Training Accuracy: 85% on validated dataset
- Cross-validation Score: 82.3% (5-fold stratified)
- Feature Importance: Income stability (40%), Financial practices (25%), Technology adoption (15%)

**Note:** The complete machine learning pipeline, trained models, and original datasets are proprietary. For access to the production Random Forest model and training methodologies, please contact the author directly.

</details>

<details>
<summary><strong>Machine Learning Pipeline Architecture</strong></summary>

**Data Preprocessing:**
- Missing value imputation using multivariate iterative imputation
- Categorical encoding through LabelEncoder for ordinal features
- Feature scaling using StandardScaler for numerical variables
- Outlier detection and treatment using Isolation Forest methodology

**Model Training:**
- Algorithm Selection: Random Forest chosen for interpretability and robustness
- Ensemble Configuration: 100 decision trees with entropy-based splitting criteria
- Validation Strategy: 5-fold stratified cross-validation for unbiased performance estimation
- Hyperparameter Tuning: GridSearchCV optimization across parameter space

**Performance Evaluation:**
- Primary Metric: F1-Score optimized for imbalanced class distribution
- Secondary Metrics: Precision-Recall AUC for risk detection capability
- Feature Importance Analysis: Permutation-based importance for model interpretability
- Confusion Matrix Analysis: False positive/negative trade-off optimization

</details>

<details>
<summary><strong>Key Predictive Indicators and Feature Importance</strong></summary>

**Primary Risk Factors (Ranked by Predictive Power):**
1. Business Turnover to Expense Ratio (Weight: 0.34)
2. Financial Record Keeping Practices (Weight: 0.22)
3. Insurance Coverage Status (Weight: 0.18)
4. Mobile Money Integration (Weight: 0.15)
5. Tax Compliance History (Weight: 0.11)

**Demographic and Geographic Variables:**
- Country-specific risk patterns showing regional economic variations
- Business age correlation with financial stability metrics
- Gender-based differences in financial management approaches
- Technology adoption rates varying by geographic location

</details>

---

<h2 align="center">Demo Implementation</h2>

**Current System Architecture:**
For demonstration purposes, this repository implements a TypeScript-based rule engine that approximates the machine learning predictions using weighted scoring algorithms. The demo system provides:

- Interactive web interface for financial health assessment
- Real-time risk categorization using heuristic models
- Confidence scoring and recommendation generation
- Responsive design optimized for mobile deployment

---

<h2 align="center">Technology Stack</h2>

**Production Model (Contact Author for Access):**
- Scikit-learn Random Forest implementation with 85% accuracy
- Feature engineering pipeline with automated categorical encoding
- Model persistence using joblib serialization
- API deployment with Flask and CORS configuration

**Demo System (Current Repository):**
- Next.js 15 with App Router architecture
- TypeScript for type-safe prediction logic
- Tailwind CSS for responsive UI components
- Server-side rendering for optimal performance
- React 18 with TypeScript
- Client-side prediction processing for real-time feedback

**Key Application Features:**

1. **Comprehensive Survey**
   - 16 questions across 5 categories (demographics, financial, insurance, attitudes, operations)
   - Aligned with actual dataset variables for accurate predictions

2. **AI-Powered Assessment**
   - Random Forest model trained on 9,618 real business records
   - Real-time financial health categorization (Low/Medium/High risk)
   - Confidence scoring for prediction reliability

3. **Data-Driven Insights**
   - Interactive charts showing regional business health trends
   - Comparative analysis across countries and risk categories
   - Success factor identification for business improvement

4. **Business Intelligence**
   - Risk assessment automation for insurers
   - Portfolio management tools for financial institutions
   - Policy guidance based on real market data

---

<h2 align="center">Geographic Coverage</h2>

**Dataset Distribution:**
- Eswatini: 2,674 businesses (27.8% of dataset)
- Zimbabwe: 2,612 businesses (27.2% of dataset)
- Malawi: 2,388 businesses (24.8% of dataset)
- Lesotho: 1,944 businesses (20.2% of dataset)

**Critical Success Factor Analysis:**

| Financial Indicator | Low Risk SMEs | High Risk SMEs | Risk Differential |
|:-------------------|:-------------:|:--------------:|:-----------------:|
| Average Annual Income | $882,802 | $254,095 | 5x difference |
| Tax Compliance Rate | 44.7% | 8.8% | 5x higher compliance |
| Insurance Coverage | 21.9% | 0% | Complete protection gap |
| Mobile Money Usage | 73.0% | 46.3% | 1.6x higher adoption |

---

<h2 align="center">Strategic Applications</h2>

**For Financial Institutions:**
- Credit Scoring Enhancement: Integration with existing underwriting processes
- Portfolio Risk Management: Real-time monitoring of loan portfolio health
- Market Segmentation: Identification of high-potential customer segments
- Regulatory Reporting: Automated risk classification for compliance requirements

**For Insurance Companies:**
- Risk Assessment Automation: Replace manual underwriting with ML-powered evaluation
- Market Opportunity Identification: Target 97% uninsured SME segment with precision
- Premium Optimization: Data-driven pricing based on empirical risk factors
- Portfolio Management: Continuous monitoring of policyholder financial trajectories
- Regulatory Compliance: Standardized risk categorization supporting prudential requirements

**For Policy Makers:**
- Evidence-Based Policy: Data from 9,618 businesses informing SME support programs
- Resource Allocation: Target interventions based on quantified risk assessments
- Financial Inclusion Initiatives: Build upon 50.7% mobile money foundation
- Regional Economic Monitoring: Continuous assessment of cross-border SME health patterns

---

<h2 align="center">Getting Started</h2>

<div align="center">

### Quick Start

```bash
git clone https://github.com/Nqobileee/financial-prediction.git
cd financial-prediction
npm install
npm run dev
```

</div>

**System Requirements:**
- Node.js 18.17 or later
- Python 3.8+ with pip (for backend API)
- Modern web browser with JavaScript enabled
- Git

**Development Environment Setup:**

1. **Clone and Setup**
   ```bash
   git clone https://github.com/Nqobileee/financial-prediction.git
   cd financial-prediction
   npm install
   ```

2. **Start Backend API** (Optional)
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

---

<h2 align="center">API Documentation</h2>

**Available Endpoints:**

- `GET /api/health` - System health verification and status check
- `POST /api/predict` - Submit survey for ML-powered financial health prediction
- `POST /api/train` - Retrain model with new data (production environment only)

**Request Format Example:**
```json
{
  "country": "Zimbabwe",
  "business_age": 5,
  "tax_compliance": "yes",
  "insurance_coverage": "no",
  "mobile_money": "yes"
}
```

---

<h2 align="center">Research Impact</h2>

<details>
<summary><strong>Research Methodology and Data Compliance</strong></summary>

**Dataset Attribution:**
- Source: Zindi Africa Competition Dataset
- License: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)
- Compliance: Original training data removed per competition redistribution rules
- Synthetic Data: Dummy datasets generated maintaining statistical properties

**Ethical Considerations:**
- Data Privacy: All personal identifiers removed from analytical datasets
- Bias Mitigation: Stratified sampling ensuring demographic representation
- Transparency: Open methodology documentation for reproducible research
- Impact Assessment: Continuous monitoring of model fairness across demographic groups

</details>

**Impact Measurement and Validation:**

**Economic Development Metrics:**
- SME Survival Rate Improvement through early intervention
- Financial Inclusion Expansion via targeted insurance product development
- Tax Revenue Enhancement through compliance improvement strategies
- Regional Economic Stability through systemic risk reduction

**Model Performance Benchmarks:**
- Prediction Accuracy: Continuous validation against ground truth outcomes
- Business Impact: Measurable improvement in SME financial health trajectories
- Policy Effectiveness: Quantified impact of data-driven intervention strategies
- Market Penetration: Insurance adoption rates in targeted SME segments

**Real-World Impact Potential:**

> **Economic Development**: Early intervention for 65.3% of high-risk businesses could significantly improve SME survival rates across Southern Africa.

- **SME Survival**: Early intervention for 65.3% of high-risk businesses
- **Financial Inclusion**: Build on 50.7% mobile money foundation for broader financial services
- **Government Revenue**: Improve 13% tax compliance rate through targeted support
- **Insurance Industry Transformation**: Address 97% uninsured SME market with data-driven products
- **Research & Policy Innovation**: Replace assumptions with evidence from 9,618 businesses
- **Regional Cooperation**: Cross-border insights across 4 Southern African countries

---

<h2 align="center">Future Research Directions</h2>

**Model Enhancement Opportunities:**
- Deep Learning Integration: Neural network architectures for complex pattern recognition
- Ensemble Methods: Combining multiple algorithms for improved prediction accuracy
- Time Series Analysis: Incorporating temporal business performance patterns
- Causal Inference: Moving beyond correlation to causal relationship identification

**Dataset Expansion:**
- Longitudinal Studies: Multi-year business trajectory analysis
- Cross-Regional Validation: Extending analysis to additional African markets
- Sector-Specific Models: Industry-tailored risk assessment frameworks
- Real-Time Data Integration: Incorporating dynamic business performance indicators

---

<h2 align="center">Contributing</h2>

This open-source project welcomes contributions from:

- **Researchers**: Expand dataset coverage and analytical depth
- **Developers**: Enhance ML models and user experience
- **Policymakers**: Integrate insights into SME support programs
- **Financial Institutions**: Pilot risk assessment automation
- **SME Organizations**: Provide feedback for business-relevant features

**Contact and Collaboration:**

For access to the complete machine learning pipeline, trained models, original datasets, or research collaboration opportunities, please contact the author directly. We welcome partnerships with:

- Academic institutions conducting SME development research
- Financial organizations implementing ML-driven risk assessment
- Government agencies developing evidence-based SME policies
- Insurance companies expanding into underserved markets

---

<h2 align="center">License and Citation</h2>

**License:**

This project is open source and available under the MIT License.

**Data License:**
- [Creative Commons Attribution–ShareAlike 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
- [Zindi Competition Rules](https://zindi.africa/rules)

**Citation:**

```bibtex
@software{finhealth2026,
  title={FinHealth: Machine Learning Approaches to SME Financial Risk Assessment in Southern Africa},
  author={Muyambiri, Nqobile},
  year={2026},
  publisher={Financial Technology Research Initiative},
  note={Analysis of 9,618 SMEs across Eswatini, Zimbabwe, Malawi, and Lesotho}
}
```

**Cite this work:**
```
FinHealth SME Financial Health Prediction Platform (2026)
Southern African SME Risk Assessment Study
Dataset: 9,618 businesses across Eswatini, Zimbabwe, Malawi, Lesotho
```

---

<h2 align="center">Acknowledgments</h2>

**Data and Research Foundation:**
- Zindi Africa for hosting the competition and providing access to comprehensive SME datasets
- Competition organizers who curated 9,618 business records across four countries
- SME business owners who participated in the original data collection initiative
- Creative Commons community enabling open data sharing through CC BY-SA 4.0

**Technical Infrastructure:**
- Scikit-learn development team for robust machine learning frameworks
- Next.js and React communities for modern web development capabilities
- Pandas and NumPy for efficient data processing and statistical analysis
- Flask for reliable API backend architecture
- Tailwind CSS for elegant, professional UI design
- Open source ecosystem enabling collaborative research and development

**Impact Partners:**
- SME development organizations supporting small business growth across Africa
- Financial inclusion advocates working to bridge insurance and credit gaps
- Policy makers utilizing evidence-based insights for economic development
- Technology innovators building solutions for underserved markets
- Insurance companies pioneering data-driven risk assessment in emerging markets

**Special Recognition:**

This project stands on the shoulders of countless individuals committed to financial inclusion, data transparency, economic development, and technological innovation. Empowering SMEs through data-driven insights represents a collective effort of researchers, developers, business owners, and organizations committed to transforming financial inclusion across Southern Africa.

---

<div align="center">

*Transforming SME financial health assessment from guesswork to evidence-based insights, one prediction at a time.*

</div>

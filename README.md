#  Netflix Churn Prediction

This project predicts whether a Netflix user is likely to **churn** (unsubscribe) or not, based on features like age, subscription type, watch habits, login activity, and more.  

I used machine learning models like **Logistic Regression, Random Forest, and XGBoost** with and without **PCA (Principal Component Analysis)** to compare their performance.

---
##  Problem Statement

Churn prediction helps streaming platforms like Netflix identify users who are likely to leave the platform. With this info, the business can take action (like promotions or personalized content) to retain them.

---
##  Dataset Overview

**Columns used:**
- `age`, `gender`, `subscription_type`, `watch_hours`, `last_login_days`  
- `region`, `device`, `monthly_fee`, `payment_method`  
- `number_of_profiles`, `avg_watch_time_per_day`, `favorite_genre`  
- `churned` (target variable)

 The dataset was already clean and had no missing values.

---
##  Step-by-Step Workflow

### Setup and Views  
- Uploaded data to **Supabase**  
- Created 6 useful views in Supabase for exploratory analysis:
  - `churn_summary_by_age`
  - `churn_rate_by_subscription_region_genre`
  - `churn_rate_by_gender_genre`
  - `churn_rate_by_device_and_profiles`
  - `churn_rate_by_region_and_last_login`
  - `churn_rate_by_genre_and_fee`

###  Modeling  
1. Dropped `customer_id`  
2. Created a new feature:
   - `watch_time_level`: *"above average"* or *"below average"*
3. One-Hot Encoded all categorical columns → Resulted in **38 features**
4. Split data:
   - `X` = all features  
   - `y` = `churned`

---

##  PCA vs No PCA

I tried two approaches:
- **With PCA**: Transformed data into principal components, and selected 27 components using variance  
- **Without PCA**: Kept original one-hot encoded features

### ⚠️ Why PCA is NOT good for Tree-Based Models?
PCA creates **linear combinations** of features, which may remove important **non-linear relationships**. Tree models like Random Forest and XGBoost are designed to capture these.  
Also, PCA hurts **interpretability**, which is a key strength of decision trees.

---

##  Model Performance

| Metric     | Logistic (No PCA) | Logistic (PCA) | Random Forest (No PCA) | Random Forest (PCA) | XGBoost (No PCA) | XGBoost (PCA) |
|------------|------------------|----------------|--------------------------|----------------------|------------------|----------------|
| **Accuracy**   | 0.895            | **0.997**      | 0.981                    | 0.993                | 0.995            | 0.995          |
| **F1 Score**   | 0.897            | **0.997**      | 0.981                    | 0.993                | 0.995            | 0.995          |
| **Precision**  | 0.881            | **0.998**      | 0.984                    | 0.992                | **0.998**        | 0.994          |
| **Recall**     | 0.914            | **0.996**      | 0.978                    | 0.994                | 0.992            | **0.996**      |
| **ROC AUC**    | 0.968            | 0.998          | 0.998                    | **1.000**            | **1.000**        | **1.000**      |

###  Best Scores by Metric:
- **Accuracy:** 0.997 → Logistic Regression (PCA)  
- **F1 Score:** 0.997 → Logistic Regression (PCA)  
- **Precision:** 0.998 → Logistic Regression (PCA) & XGBoost (No PCA)  
- **Recall:** 0.996 → XGBoost (PCA) & Logistic Regression (PCA)  
- **ROC AUC:** 1.000 → XGBoost (both) & RF (PCA)

✅ **Best Model:** Logistic Regression (with PCA)

---

##  Experiment Tracking

Used **MLflow** to log all models and metrics.  
Saved the best model: **Logistic Regression with PCA**

---

## ⚙️ Why I Didn’t Use a Full Preprocessing Pipeline (And Went with PCA Inputs Instead)

I intentionally skipped building a full pipeline (with encoders, scalers, PCA steps) for this project. Here’s why:

-  The model was trained on **PCA-transformed data**, and I wanted to keep deployment **simple and consistent**, same format in, same format out.
-  Building a full pipeline would’ve meant:
  - Storing encoder categories and mappings
  - Ensuring category order consistency
  - Running the entire transformation stack during API calls
-  Since PCA already compressed everything into **27 numerical values**, it made sense to treat it as a clean input interface for deployment.
-  In short: **no pipeline = fewer moving parts**, especially when deploying to a fast, lightweight API.
-  This was a conscious choice to **prioritize speed, simplicity, and matching training–inference flow** over full feature interpretability.

If I were scaling this for production with real-time data, I would definitely modularize the pipeline and include preprocessing steps before PCA.

---

##  Deployment

###  Backend
- Built using **FastAPI**
- Takes 27 PCA values as input
- Returns churn prediction (`0 = Not Churned`, `1 = Churned`)

###  Frontend
- Made with **Streamlit**
- Simple form to paste PCA values and see prediction

##  Sample Input (So You Don’t Have to Guess an array of 27 Numbers 😅)

Getting 27 PCA-transformed values is not something anyone enjoys doing manually.

So here’s a ready-to-go input you can just copy and paste into the app:

2.9325004062562914, -0.20500038810534002, 0.5044890282438369, 1.5401265183637862, 1.2917933456801178, 1.866398586418571, -0.7219193399239652, -0.08217815011674472, 0.5177606825709633, -1.5010411968911705, 0.3993020772780832, 0.030077818175989927, -1.039055883209091, 2.418908600638633, -0.9524612587253355, -0.37109155676525163, 0.15531816592668204, -1.285229487777928, -1.7754378226137837, 0.5163062464221537, 1.4289352310846892, -0.5186619943678086, -1.7379385701945096, -0.10629869454466866, -0.44503573110240346, -0.9847922118204001, 0.08637611481827594



📌 Just paste it into the input box and hit **Predict**

🔗 **Live App:**  
[https://netflix-churn-1.onrender.com/](https://netflix-churn-1.onrender.com/)
⚠️ *Note:* The app is hosted on Render’s **free tier**, so it might take a while to load or may go to sleep sometimes. If it doesn’t open immediately, give it a minute or try again later.

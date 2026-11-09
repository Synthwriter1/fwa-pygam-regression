import pandas as pd
import numpy as np
import joblib
from pygam import LinearGAM, s, f
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

print("1. Loading specific columns to save memory...")
columns_to_keep = [
    'Tot_Benes', 'Tot_Srvcs', 'Avg_Sbmtd_Chrg', 
    'Avg_Mdcr_Alowd_Amt', 'Place_Of_Srvc', 'Rndrng_Prvdr_Type'
]
df = pd.read_csv("ca_medicare_claims.csv", usecols=columns_to_keep)

print("   Cleaning nulls and engineering features...")
numeric_cols = ['Tot_Benes', 'Tot_Srvcs', 'Avg_Sbmtd_Chrg', 'Avg_Mdcr_Alowd_Amt']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna(subset=['Tot_Srvcs', 'Avg_Sbmtd_Chrg', 'Avg_Mdcr_Alowd_Amt']).copy()

# Engineer features and log transformations
df['Charge_Variance'] = ((df['Avg_Sbmtd_Chrg'] - df['Avg_Mdcr_Alowd_Amt']) * df['Tot_Srvcs']).clip(lower=0)
df['Log_Tot_Srvcs'] = np.log1p(df['Tot_Srvcs'])
df['Log_Allowed_Amt'] = np.log1p(df['Avg_Mdcr_Alowd_Amt'])
df['Log_Variance'] = np.log1p(df['Charge_Variance'])

# Encode categoricals
df['Place_Of_Srvc_Idx'] = df['Place_Of_Srvc'].astype('category').cat.codes
top_specialties = df['Rndrng_Prvdr_Type'].value_counts().nlargest(30).index
df['Specialty_Clean'] = df['Rndrng_Prvdr_Type'].where(df['Rndrng_Prvdr_Type'].isin(top_specialties), 'Other')
df['Specialty_Clean_Idx'] = df['Specialty_Clean'].astype('category').cat.codes

print("2. Defining the PyGAM Model architecture...")
feature_cols = ['Log_Tot_Srvcs', 'Log_Allowed_Amt', 'Place_Of_Srvc_Idx', 'Specialty_Clean_Idx']
X = df[feature_cols].values
y = df['Log_Variance'].values

gam = LinearGAM(s(0) + s(1) + f(2) + f(3))

print("3. Tuning model on a 2% sample (this usually takes 1-3 minutes)...")
# Reduced to 2% to prevent CPU locking
X_sample = df[feature_cols].sample(frac=0.02, random_state=42).values
y_sample = df['Log_Variance'].sample(frac=0.02, random_state=42).values
gam.gridsearch(X_sample, y_sample)

print("4. Fitting optimized model on full dataset (almost done)...")
gam.fit(X, y)

print("5. Saving model to disk...")
joblib.dump(gam, 'billing_variance_model.pkl')
print("Success! Model saved as 'billing_variance_model.pkl'.")

print("6. Calculating model evaluation metrics...")
y_pred = gam.predict(X)
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
mae = mean_absolute_error(y, y_pred)
print(f"Model Metrics -> R2: {r2:.4f}, RMSE: {rmse:.4f}, MAE: {mae:.4f}")

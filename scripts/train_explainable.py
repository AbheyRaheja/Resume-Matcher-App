"""Train script intended to be short and easy to explain.
It does:
- load CSV with 'Resume' and 'Category' columns
- clean text, encode labels
- try three model families: LogisticRegression, XGBoost, LightGBM
- evaluate using weighted F1 and accuracy
- save best model to models/pipeline.pkl
- write experiments/results.csv with a row per model
- optionally log to MLflow if MLFLOW_TRACKING_URI is set in env
"""
import os, argparse, pickle, csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import mlflow, mlflow.sklearn

# Optional external classifiers
try:
    import xgboost as xgb
except Exception:
    xgb = None
try:
    import lightgbm as lgb
except Exception:
    lgb = None

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.utils.text import clean_resume


def load_data(path):
    df = pd.read_csv(path)
    df = df.drop_duplicates(subset=['Resume']).reset_index(drop=True)
    df['cleaned'] = df['Resume'].astype(str).apply(clean_resume)
    return df[['cleaned','Category']].rename(columns={'cleaned':'text','Category':'label'})

def run_one(X_train,X_val,y_train,y_val,estimator, name):
    pipe = make_pipeline(TfidfVectorizer(lowercase=True, ngram_range=(1,2), max_features=10000), estimator)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_val)
    acc = accuracy_score(y_val, preds)
    f1 = f1_score(y_val, preds, average='weighted')
    return pipe, acc, f1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default=os.getenv('DATASET_PATH','data/UpdatedResumeDataSet.csv'))
    args = parser.parse_args()
    df = load_data(args.data)
    X = df['text'].values
    le = LabelEncoder()
    y = le.fit_transform(df['label'].values)
    X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

    mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', None)
    if mlflow_uri:
        mlflow.set_tracking_uri(mlflow_uri)
    mlflow.set_experiment('resume_explainable')

    results = []
    best_score = -1
    best_model = None
    best_labels = None

    # 1) Logistic Regression baseline
    with mlflow.start_run(run_name='logreg'):
        pipe, acc, f1 = run_one(X_train,X_val,y_train,y_val, LogisticRegression(max_iter=1000), 'logreg')
        mlflow.log_metric('val_acc', float(acc)); mlflow.log_metric('val_f1', float(f1))
        results.append({'model':'logreg','acc':float(acc),'f1':float(f1)})
        if f1 > best_score:
            best_score = f1; best_model = pipe; best_labels = le

    # 2) XGBoost (if available)
    if xgb is not None:
        with mlflow.start_run(run_name='xgboost'):
            clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', n_estimators=100)
            pipe, acc, f1 = run_one(X_train,X_val,y_train,y_val, clf, 'xgboost')
            mlflow.log_metric('val_acc', float(acc)); mlflow.log_metric('val_f1', float(f1))
            results.append({'model':'xgboost','acc':float(acc),'f1':float(f1)})
            if f1 > best_score:
                best_score = f1; best_model = pipe; best_labels = le

    # 3) LightGBM (if available)
    if lgb is not None:
        with mlflow.start_run(run_name='lightgbm'):
            clf = lgb.LGBMClassifier(n_estimators=100)
            pipe, acc, f1 = run_one(X_train,X_val,y_train,y_val, clf, 'lightgbm')
            mlflow.log_metric('val_acc', float(acc)); mlflow.log_metric('val_f1', float(f1))
            results.append({'model':'lightgbm','acc':float(acc),'f1':float(f1)})
            if f1 > best_score:
                best_score = f1; best_model = pipe; best_labels = le

    # Save results CSV for easy inspection and interview demo
    os.makedirs('experiments', exist_ok=True)
    keys = ['model','acc','f1']
    with open('experiments/results.csv','w',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    # Save best model locally as a pickle bundle with label encoder for serving code
    os.makedirs('models', exist_ok=True)
    with open('models/pipeline.pkl','wb') as f:
        pickle.dump({'pipe':best_model, 'label_encoder': le}, f)

    print('Training complete. Results written to experiments/results.csv and best model saved to models/pipeline.pkl')

if __name__ == '__main__':
    main()

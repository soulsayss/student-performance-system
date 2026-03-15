"""
Train ML model for student performance prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
import joblib
import os

def load_dataset(filepath='ml/student_performance_dataset.csv'):
    """Load the student dataset"""
    df = pd.read_csv(filepath)
    print(f"Loaded dataset with {len(df)} records")
    return df

def prepare_features(df):
    """
    Feature engineering and preprocessing
    """
    # Select features for training
    feature_columns = [
        'attendance_percentage',
        'average_marks',
        'assignment_completion_rate',
        'quiz_average',
        'participation_score',
        'study_hours_per_week',
        'late_submissions'
    ]
    
    X = df[feature_columns].copy()
    
    # Target variable
    y_risk = df['risk_level'].copy()
    y_grade = df['predicted_grade'].copy()
    
    # Encode target variables
    risk_encoder = LabelEncoder()
    grade_encoder = LabelEncoder()
    
    y_risk_encoded = risk_encoder.fit_transform(y_risk)
    y_grade_encoded = grade_encoder.fit_transform(y_grade)
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)
    
    return X_scaled, y_risk_encoded, y_grade_encoded, scaler, risk_encoder, grade_encoder, feature_columns

def train_risk_model(X_train, X_test, y_train, y_test):
    """
    Train Random Forest Classifier for risk level prediction
    """
    print("\n" + "="*50)
    print("Training Risk Level Prediction Model")
    print("="*50)
    
    # Initialize model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['high', 'low', 'medium']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    return model, accuracy, f1

def train_grade_model(X_train, X_test, y_train, y_test):
    """
    Train Random Forest Classifier for grade prediction
    """
    print("\n" + "="*50)
    print("Training Grade Prediction Model")
    print("="*50)
    
    # Initialize model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return model, accuracy, f1

def save_models(risk_model, grade_model, scaler, risk_encoder, grade_encoder, feature_columns):
    """
    Save trained models and preprocessors
    """
    # Create models directory
    models_dir = 'ml/models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Save models
    joblib.dump(risk_model, f'{models_dir}/risk_model.pkl')
    joblib.dump(grade_model, f'{models_dir}/grade_model.pkl')
    joblib.dump(scaler, f'{models_dir}/scaler.pkl')
    joblib.dump(risk_encoder, f'{models_dir}/risk_encoder.pkl')
    joblib.dump(grade_encoder, f'{models_dir}/grade_encoder.pkl')
    joblib.dump(feature_columns, f'{models_dir}/feature_columns.pkl')
    
    print(f"\n✅ Models saved to {models_dir}/")

def main():
    """
    Main training pipeline
    """
    print("Student Performance Prediction - Model Training")
    print("="*50)
    
    # Load dataset
    df = load_dataset()
    
    # Prepare features
    X, y_risk, y_grade, scaler, risk_encoder, grade_encoder, feature_columns = prepare_features(df)
    
    # Split data
    X_train, X_test, y_risk_train, y_risk_test, y_grade_train, y_grade_test = train_test_split(
        X, y_risk, y_grade,
        test_size=0.2,
        random_state=42,
        stratify=y_risk
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train risk model
    risk_model, risk_accuracy, risk_f1 = train_risk_model(X_train, X_test, y_risk_train, y_risk_test)
    
    # Train grade model
    grade_model, grade_accuracy, grade_f1 = train_grade_model(X_train, X_test, y_grade_train, y_grade_test)
    
    # Save models
    save_models(risk_model, grade_model, scaler, risk_encoder, grade_encoder, feature_columns)
    
    print("\n" + "="*50)
    print("Training Complete!")
    print("="*50)
    print(f"Risk Model - Accuracy: {risk_accuracy:.4f}, F1-Score: {risk_f1:.4f}")
    print(f"Grade Model - Accuracy: {grade_accuracy:.4f}, F1-Score: {grade_f1:.4f}")

if __name__ == '__main__':
    main()

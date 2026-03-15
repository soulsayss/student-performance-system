"""
Generate synthetic student dataset for ML training
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_student_dataset(num_students=100):
    """
    Generate synthetic student data with various performance levels
    """
    np.random.seed(42)
    random.seed(42)
    
    students = []
    
    for i in range(1, num_students + 1):
        # Determine student category
        category = random.choices(
            ['excellent', 'good', 'average', 'below_average', 'at_risk'],
            weights=[15, 30, 35, 15, 5]
        )[0]
        
        # Generate features based on category
        if category == 'excellent':
            attendance_pct = np.random.uniform(95, 100)
            avg_marks = np.random.uniform(90, 100)
            assignment_completion = np.random.uniform(95, 100)
            quiz_avg = np.random.uniform(90, 100)
            participation_score = np.random.uniform(8, 10)
            risk_level = 'low'
            predicted_grade = random.choice(['A+', 'A'])
            
        elif category == 'good':
            attendance_pct = np.random.uniform(85, 95)
            avg_marks = np.random.uniform(80, 90)
            assignment_completion = np.random.uniform(85, 95)
            quiz_avg = np.random.uniform(80, 90)
            participation_score = np.random.uniform(7, 9)
            risk_level = 'low'
            predicted_grade = random.choice(['A', 'B+'])
            
        elif category == 'average':
            attendance_pct = np.random.uniform(75, 85)
            avg_marks = np.random.uniform(70, 80)
            assignment_completion = np.random.uniform(75, 85)
            quiz_avg = np.random.uniform(70, 80)
            participation_score = np.random.uniform(6, 8)
            risk_level = 'low'
            predicted_grade = random.choice(['B', 'B+', 'C+'])
            
        elif category == 'below_average':
            attendance_pct = np.random.uniform(60, 75)
            avg_marks = np.random.uniform(55, 70)
            assignment_completion = np.random.uniform(60, 75)
            quiz_avg = np.random.uniform(55, 70)
            participation_score = np.random.uniform(4, 6)
            risk_level = 'medium'
            predicted_grade = random.choice(['C', 'C+', 'D'])
            
        else:  # at_risk
            attendance_pct = np.random.uniform(30, 60)
            avg_marks = np.random.uniform(30, 55)
            assignment_completion = np.random.uniform(30, 60)
            quiz_avg = np.random.uniform(30, 55)
            participation_score = np.random.uniform(2, 5)
            risk_level = 'high'
            predicted_grade = random.choice(['D', 'F'])
        
        # Add some noise
        attendance_pct = max(0, min(100, attendance_pct + np.random.normal(0, 2)))
        avg_marks = max(0, min(100, avg_marks + np.random.normal(0, 3)))
        assignment_completion = max(0, min(100, assignment_completion + np.random.normal(0, 2)))
        quiz_avg = max(0, min(100, quiz_avg + np.random.normal(0, 3)))
        participation_score = max(0, min(10, participation_score + np.random.normal(0, 0.5)))
        
        # Additional features
        study_hours_per_week = {
            'excellent': np.random.uniform(15, 25),
            'good': np.random.uniform(10, 15),
            'average': np.random.uniform(7, 10),
            'below_average': np.random.uniform(4, 7),
            'at_risk': np.random.uniform(1, 4)
        }[category]
        
        late_submissions = {
            'excellent': np.random.randint(0, 2),
            'good': np.random.randint(0, 3),
            'average': np.random.randint(2, 5),
            'below_average': np.random.randint(4, 8),
            'at_risk': np.random.randint(6, 12)
        }[category]
        
        student = {
            'student_id': i,
            'attendance_percentage': round(attendance_pct, 2),
            'average_marks': round(avg_marks, 2),
            'assignment_completion_rate': round(assignment_completion, 2),
            'quiz_average': round(quiz_avg, 2),
            'participation_score': round(participation_score, 2),
            'study_hours_per_week': round(study_hours_per_week, 2),
            'late_submissions': late_submissions,
            'predicted_grade': predicted_grade,
            'risk_level': risk_level,
            'category': category
        }
        
        students.append(student)
    
    df = pd.DataFrame(students)
    
    # Print statistics
    print(f"Generated {num_students} student records")
    print(f"\nRisk Level Distribution:")
    print(df['risk_level'].value_counts())
    print(f"\nGrade Distribution:")
    print(df['predicted_grade'].value_counts())
    print(f"\nCategory Distribution:")
    print(df['category'].value_counts())
    
    return df

if __name__ == '__main__':
    # Generate dataset
    df = generate_student_dataset(150)
    
    # Save to CSV
    output_file = 'ml/student_performance_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Dataset saved to {output_file}")
    
    # Display sample
    print("\nSample records:")
    print(df.head(10))
    
    # Display statistics
    print("\nDataset Statistics:")
    print(df.describe())

"""
Comprehensive System Test Suite
Tests all backend endpoints, authentication, and data integrity
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_RESULTS = []

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_test(test_name, status, message=""):
    """Log test result"""
    symbol = "✓" if status == "PASS" else "✗"
    color = Colors.GREEN if status == "PASS" else Colors.RED
    
    result = {
        'test': test_name,
        'status': status,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    TEST_RESULTS.append(result)
    
    print(f"{color}{symbol} {test_name}{Colors.END}")
    if message:
        print(f"  {message}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Authentication Endpoints ==={Colors.END}")
    
    # Test 1: Register new user
    try:
        register_data = {
            "name": "Test Student",
            "email": f"test_student_{int(time.time())}@test.com",
            "password": "Test@123",
            "role": "student",
            "roll_number": f"TEST{int(time.time())}",
            "class": "10",
            "section": "A"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        
        if response.status_code == 201:
            log_test("Auth: Register new user", "PASS", f"Status: {response.status_code}")
            global test_user_email, test_user_password
            test_user_email = register_data['email']
            test_user_password = register_data['password']
        else:
            log_test("Auth: Register new user", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        log_test("Auth: Register new user", "FAIL", str(e))
    
    # Test 2: Login with credentials
    try:
        login_data = {
            "email": "admin@school.com",
            "password": "Admin@123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200 and 'access_token' in response.json():
            log_test("Auth: Login with valid credentials", "PASS")
            global admin_token
            admin_token = response.json()['access_token']
        else:
            log_test("Auth: Login with valid credentials", "FAIL", response.text)
    except Exception as e:
        log_test("Auth: Login with valid credentials", "FAIL", str(e))
    
    # Test 3: Login with invalid credentials
    try:
        login_data = {
            "email": "invalid@test.com",
            "password": "wrongpassword"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 401:
            log_test("Auth: Reject invalid credentials", "PASS")
        else:
            log_test("Auth: Reject invalid credentials", "FAIL", f"Expected 401, got {response.status_code}")
    except Exception as e:
        log_test("Auth: Reject invalid credentials", "FAIL", str(e))
    
    # Test 4: Get profile with token
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        
        if response.status_code == 200:
            log_test("Auth: Get profile with valid token", "PASS")
        else:
            log_test("Auth: Get profile with valid token", "FAIL", response.text)
    except Exception as e:
        log_test("Auth: Get profile with valid token", "FAIL", str(e))
    
    # Test 5: Access protected endpoint without token
    try:
        response = requests.get(f"{BASE_URL}/student/dashboard")
        
        if response.status_code == 401:
            log_test("Auth: Reject request without token", "PASS")
        else:
            log_test("Auth: Reject request without token", "FAIL", f"Expected 401, got {response.status_code}")
    except Exception as e:
        log_test("Auth: Reject request without token", "FAIL", str(e))

def test_student_endpoints():
    """Test student endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Student Endpoints ==={Colors.END}")
    
    # Login as student
    try:
        login_data = {
            "email": "student1@school.com",
            "password": "Student@123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        student_token = response.json()['access_token']
        headers = {"Authorization": f"Bearer {student_token}"}
        
        # Test 1: Get dashboard
        response = requests.get(f"{BASE_URL}/student/dashboard", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get dashboard", "PASS")
        else:
            log_test("Student: Get dashboard", "FAIL", response.text)
        
        # Test 2: Get attendance
        response = requests.get(f"{BASE_URL}/student/attendance", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get attendance", "PASS")
        else:
            log_test("Student: Get attendance", "FAIL", response.text)
        
        # Test 3: Get marks
        response = requests.get(f"{BASE_URL}/student/marks", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get marks", "PASS")
        else:
            log_test("Student: Get marks", "FAIL", response.text)
        
        # Test 4: Get predictions
        response = requests.get(f"{BASE_URL}/student/predictions", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get predictions", "PASS")
        else:
            log_test("Student: Get predictions", "FAIL", response.text)
        
        # Test 5: Get recommendations
        response = requests.get(f"{BASE_URL}/student/recommendations", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get recommendations", "PASS")
        else:
            log_test("Student: Get recommendations", "FAIL", response.text)
        
        # Test 6: Get achievements
        response = requests.get(f"{BASE_URL}/student/achievements", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get achievements", "PASS")
        else:
            log_test("Student: Get achievements", "FAIL", response.text)
        
        # Test 7: Get alerts
        response = requests.get(f"{BASE_URL}/student/alerts", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get alerts", "PASS")
        else:
            log_test("Student: Get alerts", "FAIL", response.text)
        
        # Test 8: Get career suggestions
        response = requests.get(f"{BASE_URL}/student/career-suggestions", headers=headers)
        if response.status_code == 200:
            log_test("Student: Get career suggestions", "PASS")
        else:
            log_test("Student: Get career suggestions", "FAIL", response.text)
            
    except Exception as e:
        log_test("Student: Endpoints", "FAIL", str(e))

def test_teacher_endpoints():
    """Test teacher endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Teacher Endpoints ==={Colors.END}")
    
    # Login as teacher
    try:
        login_data = {
            "email": "rajesh.kumar@school.com",
            "password": "Teacher@123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        teacher_token = response.json()['access_token']
        headers = {"Authorization": f"Bearer {teacher_token}"}
        
        # Test 1: Get dashboard
        response = requests.get(f"{BASE_URL}/teacher/dashboard", headers=headers)
        if response.status_code == 200:
            log_test("Teacher: Get dashboard", "PASS")
        else:
            log_test("Teacher: Get dashboard", "FAIL", response.text)
        
        # Test 2: Get students
        response = requests.get(f"{BASE_URL}/teacher/students", headers=headers)
        if response.status_code == 200:
            log_test("Teacher: Get students list", "PASS")
        else:
            log_test("Teacher: Get students list", "FAIL", response.text)
        
        # Test 3: Get analytics
        response = requests.get(f"{BASE_URL}/teacher/analytics", headers=headers)
        if response.status_code == 200:
            log_test("Teacher: Get analytics", "PASS")
        else:
            log_test("Teacher: Get analytics", "FAIL", response.text)
        
        # Test 4: Get at-risk students
        response = requests.get(f"{BASE_URL}/teacher/at-risk-students", headers=headers)
        if response.status_code == 200:
            log_test("Teacher: Get at-risk students", "PASS")
        else:
            log_test("Teacher: Get at-risk students", "FAIL", response.text)
            
    except Exception as e:
        log_test("Teacher: Endpoints", "FAIL", str(e))

def test_admin_endpoints():
    """Test admin endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Admin Endpoints ==={Colors.END}")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        # Test 1: Get analytics
        response = requests.get(f"{BASE_URL}/admin/analytics", headers=headers)
        if response.status_code == 200:
            log_test("Admin: Get analytics", "PASS")
        else:
            log_test("Admin: Get analytics", "FAIL", response.text)
        
        # Test 2: Get users
        response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
        if response.status_code == 200:
            log_test("Admin: Get users list", "PASS")
        else:
            log_test("Admin: Get users list", "FAIL", response.text)
        
        # Test 3: Get resources
        response = requests.get(f"{BASE_URL}/admin/resources", headers=headers)
        if response.status_code == 200:
            log_test("Admin: Get resources", "PASS")
        else:
            log_test("Admin: Get resources", "FAIL", response.text)
        
        # Test 4: Download CSV template
        response = requests.get(f"{BASE_URL}/admin/csv-template/students", headers=headers)
        if response.status_code == 200:
            log_test("Admin: Download CSV template", "PASS")
        else:
            log_test("Admin: Download CSV template", "FAIL", response.text)
            
    except Exception as e:
        log_test("Admin: Endpoints", "FAIL", str(e))

def test_parent_endpoints():
    """Test parent endpoints"""
    print(f"\n{Colors.BLUE}=== Testing Parent Endpoints ==={Colors.END}")
    
    # Login as parent
    try:
        login_data = {
            "email": "parent1@email.com",
            "password": "Parent@123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        parent_token = response.json()['access_token']
        headers = {"Authorization": f"Bearer {parent_token}"}
        
        # Test 1: Get dashboard
        response = requests.get(f"{BASE_URL}/parent/dashboard", headers=headers)
        if response.status_code == 200:
            log_test("Parent: Get dashboard", "PASS")
            # Get child ID for further tests
            dashboard_data = response.json()
            if dashboard_data.get('success') and dashboard_data.get('dashboard', {}).get('children'):
                child_id = dashboard_data['dashboard']['children'][0]['student_id']
                
                # Test 2: Get child performance
                response = requests.get(f"{BASE_URL}/parent/child/{child_id}/performance", headers=headers)
                if response.status_code == 200:
                    log_test("Parent: Get child performance", "PASS")
                else:
                    log_test("Parent: Get child performance", "FAIL", response.text)
                
                # Test 3: Get child alerts
                response = requests.get(f"{BASE_URL}/parent/child/{child_id}/alerts", headers=headers)
                if response.status_code == 200:
                    log_test("Parent: Get child alerts", "PASS")
                else:
                    log_test("Parent: Get child alerts", "FAIL", response.text)
                
                # Test 4: Get child recommendations
                response = requests.get(f"{BASE_URL}/parent/child/{child_id}/recommendations", headers=headers)
                if response.status_code == 200:
                    log_test("Parent: Get child recommendations", "PASS")
                else:
                    log_test("Parent: Get child recommendations", "FAIL", response.text)
        else:
            log_test("Parent: Get dashboard", "FAIL", response.text)
            
    except Exception as e:
        log_test("Parent: Endpoints", "FAIL", str(e))

def test_ml_endpoints():
    """Test ML endpoints"""
    print(f"\n{Colors.BLUE}=== Testing ML Endpoints ==={Colors.END}")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        # Test 1: Get model info
        response = requests.get(f"{BASE_URL}/ml/model-info", headers=headers)
        if response.status_code == 200:
            log_test("ML: Get model info", "PASS")
        else:
            log_test("ML: Get model info", "FAIL", response.text)
            
    except Exception as e:
        log_test("ML: Endpoints", "FAIL", str(e))

def test_error_responses():
    """Test error handling"""
    print(f"\n{Colors.BLUE}=== Testing Error Responses ==={Colors.END}")
    
    try:
        # Test 1: 401 Unauthorized
        response = requests.get(f"{BASE_URL}/student/dashboard")
        if response.status_code == 401:
            log_test("Error: 401 Unauthorized", "PASS")
        else:
            log_test("Error: 401 Unauthorized", "FAIL", f"Expected 401, got {response.status_code}")
        
        # Test 2: 404 Not Found
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/nonexistent/endpoint", headers=headers)
        if response.status_code == 404:
            log_test("Error: 404 Not Found", "PASS")
        else:
            log_test("Error: 404 Not Found", "FAIL", f"Expected 404, got {response.status_code}")
        
        # Test 3: 400 Bad Request
        response = requests.post(f"{BASE_URL}/auth/register", json={})
        if response.status_code == 400:
            log_test("Error: 400 Bad Request", "PASS")
        else:
            log_test("Error: 400 Bad Request", "FAIL", f"Expected 400, got {response.status_code}")
            
    except Exception as e:
        log_test("Error: Responses", "FAIL", str(e))

def generate_report():
    """Generate test report"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}TEST REPORT SUMMARY{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    total_tests = len(TEST_RESULTS)
    passed_tests = sum(1 for r in TEST_RESULTS if r['status'] == 'PASS')
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {passed_tests}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed_tests}{Colors.END}")
    print(f"Pass Rate: {pass_rate:.1f}%\n")
    
    if failed_tests > 0:
        print(f"{Colors.RED}Failed Tests:{Colors.END}")
        for result in TEST_RESULTS:
            if result['status'] == 'FAIL':
                print(f"  ✗ {result['test']}")
                if result['message']:
                    print(f"    {result['message']}")
    
    # Save to file
    with open('test_results.json', 'w') as f:
        json.dump({
            'summary': {
                'total': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'pass_rate': pass_rate,
                'timestamp': datetime.now().isoformat()
            },
            'results': TEST_RESULTS
        }, f, indent=2)
    
    print(f"\n{Colors.YELLOW}Full report saved to: test_results.json{Colors.END}")

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}STUDENT ACADEMIC SYSTEM - COMPREHENSIVE TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"Base URL: {BASE_URL}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        test_auth_endpoints()
        test_student_endpoints()
        test_teacher_endpoints()
        test_admin_endpoints()
        test_parent_endpoints()
        test_ml_endpoints()
        test_error_responses()
    except Exception as e:
        print(f"\n{Colors.RED}Critical Error: {str(e)}{Colors.END}")
    finally:
        generate_report()

if __name__ == "__main__":
    main()

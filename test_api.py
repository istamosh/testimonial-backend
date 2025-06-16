#!/usr/bin/env python3
"""
Test script for the testimonial API with the new form structure
"""
import requests
import json

def test_testimonial_api():
    """Test the testimonial API endpoint"""
    url = "http://localhost:5000/api/testimonial"
    
    # Test data with new form structure
    test_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "role_company": "Senior Developer at Tech Corp",
        "testimonial": "Working with Alfi was an amazing experience. He delivered high-quality code and was very professional throughout the project.",
        "censor_first_name": False,
        "censor_last_name": False,
        "consent_given": True
    }
    
    try:
        print("Testing testimonial API...")
        print(f"Sending POST request to: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ API test successful!")
            return True
        else:
            print("❌ API test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_invalid_data():
    """Test API with invalid data (missing required fields)"""
    url = "http://localhost:5000/api/testimonial"
    
    # Test data missing required consent
    invalid_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "testimonial": "Great work!",
        "consent_given": False  # This should fail validation
    }
    
    try:
        print("\n\nTesting API with invalid data (consent not given)...")
        response = requests.post(url, json=invalid_data)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 400:
            print("✅ Validation working correctly!")
            return True
        else:
            print("❌ Validation not working as expected!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid data: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Testimonial API\n")
    
    # Test valid data
    success1 = test_testimonial_api()
    
    # Test invalid data
    success2 = test_invalid_data()
    
    if success1 and success2:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed!")

import os
import sys
import requests
import json

def validate_xai_api_key(api_key):
    """
    Validates an xAI (Grok) API key by testing text and potential image/multimodal capabilities.
    Returns a tuple (is_valid_text, text_response, is_valid_image, image_response)
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_response = None
    test_prompt = "Say 'xAI API key is working correctly!' in one short sentence."
    multimodal_test_prompt = "This is a test for multimodal capability. Please respond with 'xAI multimodal test'."
    
    # API endpoint for xAI/Grok
    api_url = "https://api.xai.com/v1/chat/completions"
    
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test text generation with xAI/Grok
    try:
        payload = {
            "model": "grok-latest",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": test_prompt}
            ],
            "max_tokens": 20
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        text_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        text_valid = True
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        text_response = f"Text generation failed: {str(e)}{error_detail}"
    
    # Test image-related capabilities (if available)
    try:
        # Using potential multimodal capabilities
        payload = {
            "model": "grok-vision-latest",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": multimodal_test_prompt}
            ],
            "max_tokens": 20
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Check if the model exists and the request was successful
        if response.status_code == 200:
            response_data = response.json()
            multimodal_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            image_response = f"Response: {multimodal_response}"
            image_valid = True
        else:
            image_response = f"xAI doesn't currently offer multimodal capabilities on this endpoint. Status: {response.status_code}"
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
                
        if "model not found" in str(e).lower() or "not available" in str(e).lower():
            image_response = f"The multimodal model is not available with this API key - {error_detail}"
        else:
            image_response = f"Multimodal capability check failed: {str(e)}{error_detail}"
    
    return (text_valid, text_response, image_valid, image_response, test_prompt, multimodal_test_prompt)


if __name__ == "__main__":
    print("xAI (Grok) API Key Validator")
    print("-------------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your xAI/Grok API key: ").strip()
    
    print("\nValidating xAI API key...")
    text_valid, text_response, image_valid, image_response, test_prompt, multimodal_test_prompt = validate_xai_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {test_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nMultimodal Capability: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {multimodal_test_prompt}")
    if image_valid:
        print(f"Status: {image_response}")
    else:
        print(f"Error: {image_response}")
    
    if text_valid or image_valid:
        print("\nAPI key is valid for at least one capability.")
    else:
        print("\nAPI key is invalid for all tested capabilities.")
    
    print("\nNote: xAI is primarily focused on conversational AI with their Grok models.")
    print("The multimodal test above checks if the API key has access to potential multimodal features.")
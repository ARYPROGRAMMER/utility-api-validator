import os
import sys
import requests
import json

def validate_mistral_api_key(api_key):
    """
    Validates a Mistral AI API key by testing text generation capabilities.
    Returns a tuple with validation results and test prompts.
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_response = None
    test_prompt = "Say 'Mistral AI API key is working correctly!' in one short sentence."
    advanced_test_prompt = "This is a multimodal capability test. Please respond with 'Mistral AI multimodal test'."
    
    # API endpoint for Mistral AI
    api_url = "https://api.mistral.ai/v1/chat/completions"
    
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test text generation with one of Mistral's models
    try:
        payload = {
            "model": "mistral-small-latest",  # Using one of Mistral's standard models
            "messages": [
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
    
    # Test multimodal capabilities (if available)
    # As of April 2025, Mistral has some experimental multimodal capabilities
    try:
        # Using Mistral's multimodal capability if available
        payload = {
            "model": "mistral-large-latest",  # Using Mistral's most capable model for multimodal
            "messages": [
                {"role": "user", "content": advanced_test_prompt}
            ],
            "max_tokens": 20
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        advanced_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        image_response = f"Response: {advanced_response}\nMistral AI doesn't currently offer native image generation, but the API key is valid for their most advanced models."
        image_valid = True
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        image_response = f"Multimodal capability check failed: {str(e)}{error_detail}"
    
    return (text_valid, text_response, image_valid, image_response, test_prompt, advanced_test_prompt)


if __name__ == "__main__":
    print("Mistral AI API Key Validator")
    print("-------------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your Mistral AI API key: ").strip()
    
    print("\nValidating Mistral AI API key...")
    text_valid, text_response, image_valid, image_response, test_prompt, advanced_test_prompt = validate_mistral_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {test_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nAdvanced Model Access: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {advanced_test_prompt}")
    if image_valid:
        print(f"Status: {image_response}")
    else:
        print(f"Error: {image_response}")
    
    if text_valid:
        print("\nAPI key is valid for text generation.")
    else:
        print("\nAPI key is invalid for all tested capabilities.")
    
    print("\nNote: Mistral AI primarily focuses on text generation models.")
    print("Image generation is not currently a core feature of Mistral AI's offerings.")
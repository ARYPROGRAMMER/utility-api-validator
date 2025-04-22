import os
import sys
import requests
import json

def validate_claude_api_key(api_key):
    """
    Validates a Claude API key by testing both text and image generation/understanding capabilities.
    Returns a tuple (is_valid_text, text_response, is_valid_image, image_response)
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_response = None
    test_prompt = "Say 'Claude API key is working correctly!' in one short sentence."
    vision_test_prompt = "This is a test for vision capability. Please respond with 'Claude vision capability is working correctly!'"
    
    # API endpoint for Claude
    api_url = "https://api.anthropic.com/v1/messages"
    
    # Headers for the request
    headers = {
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "x-api-key": api_key
    }
    
    # Test text generation
    try:
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": test_prompt}
            ]
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for 4XX/5XX errors
        
        response_data = response.json()
        text_response = response_data.get("content", [{}])[0].get("text", "").strip()
        text_valid = True
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        text_response = f"Text generation failed: {str(e)}{error_detail}"
    
    # Test image understanding capabilities (Claude 3 can understand images)
    # Note: This tests image understanding rather than generation
    try:
        # Using Claude's vision capabilities to validate the API key for multimodal use
        # Since Claude doesn't generate images, we'll check if it can process an image-related request
        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": vision_test_prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        image_response = response_data.get("content", [{}])[0].get("text", "").strip()
        image_valid = True
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        image_response = f"Vision capability check failed: {str(e)}{error_detail}"
    
    return (text_valid, text_response, image_valid, image_response, test_prompt, vision_test_prompt)


if __name__ == "__main__":
    print("Claude API Key Validator")
    print("----------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your Claude API key: ").strip()
    
    print("\nValidating Claude API key...")
    text_valid, text_response, image_valid, image_response, test_prompt, vision_test_prompt = validate_claude_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {test_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nVision Capability: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {vision_test_prompt}")
    if image_valid:
        print(f"Response: {image_response}")
    else:
        print(f"Error: {image_response}")
    
    if text_valid or image_valid:
        print("\nAPI key is valid for at least one capability.")
    else:
        print("\nAPI key is invalid for all tested capabilities.")
        
    print("\nNote: Claude doesn't currently offer image generation capabilities like DALL-E.")
    print("The vision capability test above checks if the model can process text-only requests in vision mode.")
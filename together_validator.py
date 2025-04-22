import os
import sys
import requests
import json

def validate_together_api_key(api_key):
    """
    Validates a Together AI API key by testing text generation capabilities.
    Returns a tuple with validation results and test prompts.
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_response = None
    test_prompt = "Respond with 'Together AI API key is working correctly!' in one short sentence."
    multimodal_test_prompt = "This is a test for multimodal capability. Please respond with 'Together AI multimodal capability test'."
    
    # API endpoint for Together AI
    api_url = "https://api.together.xyz/v1/completions"
    
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test text generation with a simple model
    try:
        # Try modern model first
        try:
            payload = {
                "model": "meta-llama/Llama-3-8b-chat",
                "prompt": test_prompt,
                "max_tokens": 20,
                "temperature": 0.7
            }
            
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            text_response = response_data.get("choices", [{}])[0].get("text", "").strip()
            text_valid = True
        except Exception as e1:
            # Fallback to another model if the first one fails
            try:
                payload = {
                    "model": "togethercomputer/llama-2-7b-chat",
                    "prompt": test_prompt,
                    "max_tokens": 20,
                    "temperature": 0.7
                }
                
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()
                
                response_data = response.json()
                text_response = response_data.get("choices", [{}])[0].get("text", "").strip()
                text_valid = True
            except Exception as e2:
                raise Exception(f"Failed with both models: {str(e2)}")
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        text_response = f"Text generation failed: {str(e)}{error_detail}"
    
    # Test image generation capabilities (if available) via their newer chat API
    try:
        chat_api_url = "https://api.together.xyz/v1/chat/completions"
        
        payload = {
            "model": "mistralai/mixtral-8x7b-instruct-v0.1",  # A model that might have multimodal capabilities
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": multimodal_test_prompt}
            ],
            "max_tokens": 20
        }
        
        response = requests.post(chat_api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            multimodal_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            image_response = f"Response: {multimodal_response}\nNote: Together AI doesn't offer direct image generation yet, but API authorization successful for potential multimodal models."
            image_valid = True
        else:
            raise Exception(f"Status code: {response.status_code}, response: {response.text}")
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
                
        if "not found" in str(e).lower() or "not available" in str(e).lower():
            image_response = f"Together AI doesn't currently offer image generation capabilities.{error_detail}"
        else:
            image_response = f"Multimodal capability check failed: {str(e)}{error_detail}"
    
    return (text_valid, text_response, image_valid, image_response, test_prompt, multimodal_test_prompt)


if __name__ == "__main__":
    print("Together AI API Key Validator")
    print("---------------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your Together AI API key: ").strip()
    
    print("\nValidating Together AI API key...")
    text_valid, text_response, image_valid, image_response, test_prompt, multimodal_test_prompt = validate_together_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {test_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nImage/Multimodal Capability: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {multimodal_test_prompt}")
    if image_valid:
        print(f"Status: {image_response}")
    else:
        print(f"Error: {image_response}")
    
    if text_valid or image_valid:
        print("\nAPI key is valid for at least one capability.")
    else:
        print("\nAPI key is invalid for all tested capabilities.")
    
    print("\nNote: Together AI primarily focuses on text generation with various open source models.")
    print("The platform may add more multimodal or image capabilities in the future.")
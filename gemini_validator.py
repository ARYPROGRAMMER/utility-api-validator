import os
import sys
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument

def validate_gemini_api_key(api_key):
    """
    Validates a Gemini API key by testing both text and image processing capabilities.
    Returns a tuple with validation results and test prompts.
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_response = None
    test_prompt = "Say 'Gemini API key is working correctly!' in one short sentence."
    image_test_prompt = "Describe this test prompt without any image. Reply only with: 'Gemini image processing is working correctly!'"
    
    # Configure the API key
    genai.configure(api_key=api_key)
    
    # Test text generation with Gemini - use latest model
    try:
        # Updated to use gemini-1.5-flash (most recent model as of 2025)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(test_prompt)
        text_response = response.text.strip()
        text_valid = True
    except Exception as e:
        # If the flash model fails, try with the Pro model
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(test_prompt)
            text_response = response.text.strip()
            text_valid = True
        except Exception as e2:
            # If both fail, try the legacy model
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(test_prompt)
                text_response = response.text.strip()
                text_valid = True
            except Exception as e3:
                text_response = f"Text generation failed: {str(e3)}"
    
    # Test image processing capabilities 
    try:
        # Using Gemini's multimodal capabilities - updated model name
        model = genai.GenerativeModel('gemini-1.5-pro-vision')
        response = model.generate_content([image_test_prompt])
        image_response = response.text.strip()
        image_valid = True
    except Exception as e:
        # Try with legacy model if the new one fails
        try:
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([image_test_prompt])
            image_response = response.text.strip()
            image_valid = True
        except Exception as e2:
            if "deprecated" in str(e2).lower():
                image_response = f"Image capability testing failed: The model is deprecated. Consider using 'gemini-1.5-pro-vision' instead."
            else:
                image_response = f"Image capability testing failed: {str(e2)}"
    
    return (text_valid, text_response, image_valid, image_response, test_prompt, image_test_prompt)


if __name__ == "__main__":
    print("Gemini API Key Validator")
    print("-----------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your Gemini API key: ").strip()
    
    print("\nValidating Gemini API key...")
    text_valid, text_response, image_valid, image_response, test_prompt, image_test_prompt = validate_gemini_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {test_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nImage Processing: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {image_test_prompt}")
    if image_valid:
        print(f"Response: {image_response}")
    else:
        print(f"Error: {image_response}")
    
    if text_valid or image_valid:
        print("\nAPI key is valid for at least one capability.")
    else:
        print("\nAPI key is invalid for all tested capabilities.")
        
    print("\nNote: Gemini doesn't have direct image generation capabilities like DALL-E.")
    print("The image test above checks if the model can process image-related requests.")
import os
import sys
import requests
from openai import OpenAI

def validate_openai_api_key(api_key):
    """
    Validates an OpenAI API key by testing both text and image generation capabilities.
    Returns a tuple containing validation results and test prompts.
    """
    text_valid = False
    image_valid = False
    text_response = None
    image_url = None
    text_prompt = "Say 'OpenAI API key is working correctly!' in one short sentence."
    image_prompt = "A simple blue circle on a white background"
    
    # Create client with the provided API key
    client = OpenAI(api_key=api_key)
    
    # Test text generation
    try:
        # Try to handle project API keys (sk-proj-...) by using different models
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text_prompt}
                ],
                max_tokens=20
            )
            text_response = completion.choices[0].message.content.strip()
            text_valid = True
        except Exception as e1:
            # If standard model fails, try with GPT-4 which might be accessible
            if "invalid_api_key" in str(e1) and api_key.startswith("sk-proj-"):
                # Try alternative models for project-based keys
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": text_prompt}
                        ],
                        max_tokens=20
                    )
                    text_response = completion.choices[0].message.content.strip()
                    text_valid = True
                except Exception as e2:
                    raise Exception(f"Project API key not working with standard models: {str(e2)}")
            else:
                raise e1
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        text_response = f"Text generation failed: Error code: {e.__class__.__name__} - {str(e)}{error_detail}"
    
    # Test image generation
    try:
        # Try with DALL-E 2 first
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                n=1,
                size="256x256"
            )
            image_url = response.data[0].url
            image_valid = True
        except Exception as e1:
            # If DALL-E 2 fails, try with DALL-E 3
            if "insufficient_quota" in str(e1).lower() or "not_available" in str(e1).lower():
                try:
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=image_prompt,
                        n=1,
                        size="256x256"
                    )
                    image_url = response.data[0].url
                    image_valid = True
                except Exception as e2:
                    raise Exception(f"Image generation failed with both DALL-E 2 and 3: {str(e2)}")
            else:
                raise e1
    except Exception as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = f" - {e.response.json().get('error', {}).get('message', '')}"
            except:
                pass
        image_url = f"Image generation failed: Error code: {e.__class__.__name__} - {str(e)}{error_detail}"
    
    return (text_valid, text_response, image_valid, image_url, text_prompt, image_prompt)


if __name__ == "__main__":
    print("OpenAI API Key Validator")
    print("------------------------")
    
    # Get API key from command line argument or input
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Enter your OpenAI API key: ").strip()
    
    print("\nValidating OpenAI API key...")
    text_valid, text_response, image_valid, image_url, text_prompt, image_prompt = validate_openai_api_key(api_key)
    
    print("\nResults:")
    print(f"Text Generation: {'✓ Valid' if text_valid else '✗ Invalid'}")
    print(f"Test prompt: {text_prompt}")
    if text_valid:
        print(f"Response: {text_response}")
    else:
        print(f"Error: {text_response}")
    
    print(f"\nImage Generation: {'✓ Valid' if image_valid else '✗ Invalid'}")
    print(f"Test prompt: {image_prompt}")
    if image_valid:
        print(f"Image URL: {image_url}")
    else:
        print(f"Error: {image_url}")
    
    if text_valid or image_valid:
        print("\nAPI key is valid for at least one capability.")
    else:
        print("\nAPI key is invalid for both text and image generation.")
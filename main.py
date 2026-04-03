import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompt import system_prompt
from call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("NO API KEY FOUND")

def main():
    # print("Hello from jerrybean!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
    model="gemma-4-31b-it", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
    if response.usage_metadata is None:
        raise RuntimeError("THE API REQUEST FAILED")
    if args.verbose is True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is not None:
        function_call_results = []
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            if not function_call_result.parts or len(function_call_result.parts) == 0:
                raise Exception("Error: Function call parts is empty")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Error: Function call parts function response is empty")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: Function call parts function response response is empty")
            function_call_results.append(function_call_result.parts[0])
            if args.verbose is True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            
    else:
        print(response.text)


if __name__ == "__main__":
    main()

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


def promptFunction(input_prompt, verbose = False):

    loop_output = ''

    if verbose is True:
        loop_output += f"User prompt: {input_prompt}\n"

    messages = [types.Content(role="user", parts=[types.Part(text=input_prompt)])]

    function_responses = []

    for _ in range(20):

        messages.append(types.Content(role="user", parts=function_responses))

        response = client.models.generate_content(
        model="gemma-4-31b-it", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("THE API REQUEST FAILED")
        
        if verbose is True:
            loop_output += f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            loop_output += f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
    

        if response.function_calls is not None:
            
            for function_call in response.function_calls:
                loop_output += f"- Calling function: {function_call.name}({function_call.args})\n"
                function_call_result = call_function(function_call, verbose)
                if not function_call_result.parts or len(function_call_result.parts) == 0:
                    raise Exception("Error: Function call parts is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Error: Function call parts function response is empty")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Error: Function call parts function response response is empty")
                function_responses.append(function_call_result.parts[0])
                if verbose is True:
                    loop_output += f"-> {function_call_result.parts[0].function_response.response}\n"
        elif response.text:
            final_output = response.text
            return loop_output + final_output
        
    print("too many iterations")
    exit(code=1)




def main():
    # print("Hello from jerrybean!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    print(promptFunction(args.user_prompt, args.verbose))


if __name__ == "__main__":
    main()

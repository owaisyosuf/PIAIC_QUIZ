from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client, function_tool
from dotenv import load_dotenv 
import os
load_dotenv()
set_tracing_disabled(True)
set_default_openai_api("chat_completions")


api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
  raise ValueError("api key is not found")

external_client=AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(external_client)
global_model="gemini-2.0-flash"

@function_tool
def get_weather(city:str, unit:str ="c"):
  """this function get weather"""
  print("weather function ")
  return f"the weather in {city} is 12 {unit}"

@function_tool
def get_age(name:str):
  """this function get age"""
  print("age function ")
  return f"the age of {name} is 30"  

agent=Agent(
  name="Agent_level",
  instructions="you are a help full assistant",
  model=global_model,
  tools=[get_weather, get_age],
  tool_use_behavior=none
  )

result=Runner.run_sync(
  starting_agent=agent,
  input="what is the weather in karachi in celcius and what is the age of owais",
)

print(result.final_output)
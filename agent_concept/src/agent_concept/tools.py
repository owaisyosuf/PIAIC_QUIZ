from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client, function_tool
from dotenv import load_dotenv
import os
import asyncio
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

@function_tool()
def get_weather(city:str, unit: str = "C"):
   """
   this function get weather 
   """
   return f"the weather in {city} is 22 {unit}"



agent=Agent(
  name="Agent_level",
  instructions="you are a help full assistant",
   model=global_model,
   tools=[get_weather]
  )
async def main():
    result=await Runner.run(
    starting_agent=agent,
    input="what is the weather in karachi",
    )

    print(result.final_output)

asyncio.run(main())
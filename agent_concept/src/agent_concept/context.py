from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client,RunContextWrapper , function_tool
from dataclasses import dataclass
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

@dataclass
class userinfo:
     name:str
     age:int
     country:str="pakistan"
     

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[userinfo]) -> str:
    '''Returns the age of the user.'''
    return f"User {wrapper.context.name} is {wrapper.context.age} years old"

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[userinfo]) -> str:
    '''Returns the location of the user.'''
    return f"User {wrapper.context.name} is from {wrapper.context.location}"

async def main():
    user_info = userinfo(name="owais", age=34)

    agent = Agent[userinfo](
        name="Assistant",
        instructions="you are a helpfull assistant",
        tools=[fetch_user_age,fetch_user_location],
        model=global_model
    )

    result = await Runner.run(
        starting_agent=agent,
        input="tell me the user country name",
        context=user_info,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
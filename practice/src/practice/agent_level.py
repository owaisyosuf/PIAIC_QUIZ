from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled
from dotenv import load_dotenv
import os
load_dotenv()
set_tracing_disabled(True)


api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
  raise ValueError("api key is not found")

external_client=AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent=Agent(
  name="Agent_level",
  instructions="you are a help full assistant",
  model=OpenAIChatCompletionsModel(model="gemini-2.0-flash" , openai_client=external_client)  
  )

result=Runner.run_sync(
  starting_agent=agent,
  input="who is the founder of pakistan",
)
print(result.final_output)
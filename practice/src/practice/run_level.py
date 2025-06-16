from agents import Agent,Runner,RunConfig,OpenAIChatCompletionsModel,AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()


api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
  raise ValueError("api key is not found")

external_client=AsyncOpenAI(
  api_key=api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
  model="gemini-2.0-flash",
  openai_client=external_client
)

config=RunConfig(
  model=model,
  tracing_disabled=True,
  model_provider=external_client
)

agent=Agent(
  name="runlevel",
  instructions="you are a helfull assistant")

result=Runner.run_sync(
  starting_agent=agent,
  input="who is the founder of pakistan",
  run_config=config
)

print(result.final_output)
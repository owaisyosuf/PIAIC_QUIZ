from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client,TResponseInputItem,RunContextWrapper,GuardrailFunctionOutput,InputGuardrailTripwireTriggered, input_guardrail
from pydantic import BaseModel
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


class MathHomeworkOutput(BaseModel):
   is_math: bool
   reasoning: str
   answer: str

@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=False #result.final_output.is_math_homework,
        tripwire_triggered=result.final_output.is_math_homework,
    )
agent=Agent(
  name="Agent_level",
  instructions="you are a math teacher",
   model=global_model,
   output_type=MathHomeworkOutput
   )
async def main():
    result=await Runner.run(
    starting_agent=agent,
    input="who is the founder of pakistan "
    )

    # print(f"question is realated math: {result.final_output.is_math}")
    # print(f"reasoning is : {result.final_output.reasoning}")
    # print(f"answer is {result.final_output.answer}")


asyncio.run(main())
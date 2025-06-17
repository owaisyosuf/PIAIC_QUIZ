from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client,input_guardrail,RunContextWrapper,TResponseInputItem,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
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


guardrial_agent=Agent(
  name="Math_Teacher",
  instructions="you are a math teacher",
   model=global_model,
   output_type=MathHomeworkOutput
   )
@input_guardrail
async def math_guardrial(
   ctx:RunContextWrapper[None],agent:Agent,input: str | list[TResponseInputItem]
)-> GuardrailFunctionOutput:  
      result = await Runner.run(guardrial_agent, input, context=ctx.context)
     
      return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math,
    )

agent=Agent(
   name="customer_support_agent",
   instructions="You are a customer support agent. You help customers with their questions.",
   model=global_model,
   input_guardrails=[math_guardrial]
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "who is the founder of pakistan")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")


asyncio.run(main())
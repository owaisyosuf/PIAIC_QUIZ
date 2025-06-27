
from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled, set_default_openai_api,set_default_openai_client, output_guardrail, input_guardrail , GuardrailFunctionOutput, RunContextWrapper, InputGuardrailTripwireTriggered, TResponseInputItem, OutputGuardrailTripwireTriggered
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

class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

class MessageOutput(BaseModel):
    response: str

input_guardrail_agent = Agent(
    name="input Guardrail check",
    instructions="Check if the user is asking about math.",
    output_type=MathOutput,
    model=global_model
)
output_guardrail_agent = Agent(
    name="out Guardrail check",
    instructions="Check the llm answer is related to math.",
    output_type=MathOutput,
    model=global_model)


@input_guardrail
async def math_input_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=not result.final_output.is_math,
    )

@output_guardrail
async def math_output_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, output:MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=not result.final_output.is_math
        
    )

agent = Agent(
    name="Agent",
    instructions="you are a helpfull assistant"
                   "Return the answer in this format: response (the answer), "
                    "is_math (true/false), and reasoning (why it's math or not)."  ,
    model=global_model,
    input_guardrails=[math_input_guardrail],
    output_guardrails=[math_output_guardrail],
    output_type=MessageOutput
)

async def main():
    # This should trip the guardrail
    try:
        result=await Runner.run(agent, "what is the answer of 2*2")
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)
        print(result.final_output.is_math)
        print(result.final_output.reasoning)
        
        
    except InputGuardrailTripwireTriggered:
        print("Math input guardrail tripped")


    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main())
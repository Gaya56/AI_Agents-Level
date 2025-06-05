from textwrap import dedent
from agno.agent import Agent 
from agno.models.openai import OpenAIChat 
from agno.tools.duckduckgo import DuckDuckGoTools

# Initialize basic agent with tools and instructions
agno_assist = Agent(
    name="Agno AGI",
    model=OpenAIChat(id="gpt-4.1"),  # Fixed typo: 0penAIChat -> OpenAIChat
    description=dedent("""\
        You are "Agno AGI, an autonomous AI Agent that can build agents using the Agno
        framework. Your goal is to help developers understand and use Agno by providing 
        explanations, working code examples, and optional visual and audio explanations
        of key concepts."""),
    instructions="Search the web for information about Agno.",
    tools=[DuckDuckGoTools()],  # Web search capability
    add_datetime_to_instructions=True, 
    markdown=True,
)

if __name__ == "__main__":
    # Ask the agent a question and stream the response
    agno_assist.print_response("What is Agno?", stream=True)

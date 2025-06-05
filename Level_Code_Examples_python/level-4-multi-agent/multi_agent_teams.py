
from textwrap import dedent
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.claude import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

# Specialized web search agent
web_agent = Agent(
    name="Web Search Agent",
    role="Handle web search requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources in your responses.",
)

# Specialized financial data agent
finance_agent = Agent(
    name="Finance Agent",
    role="Handle financial data requests",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools()],
    instructions=[
        "You are a financial data specialist. Provide concise and accurate data.",
        "Use tables to display stock prices, fundamentals (P/E, Market Cap)",
    ],
)

# Team leader with reasoning capabilities
team_leader = Team(
    name="Reasoning Finance Team Leader",
    mode="coordinate",  # Coordinate between specialized agents
    model=Claude(id="claude-3-7-sonnet-latest"),
    members=[web_agent, finance_agent],  # Team members
    tools=[ReasoningTools(add_instructions=True)],  # Enhanced reasoning
    instructions=[
        "Use tables to display data",
        "Only output the final answer, no other text.",
    ],
    show_members_responses=True,  # Show individual agent responses
    enable_agentic_context=True,  # Context management across agents
    add_datetime_to_instructions=True,
    success_criteria="The team has successfully completed the task.",
)

if __name__ == "__main__":
    # Complex multi-step analysis task
    analysis_query = dedent("""\
        Analyze the impact of recent US tariffs on market performance across
        these key sectors:
        - Steel & Aluminum: (X, NUE, AA)
        - Technology Hardware: (AAPL, DELL, HPQ)

        For each sector:
        1. Compare stock performance before and after tariff implementation
        2. Identify supply chain disruptions and cost impact percentages
        3. Analyze companies' strategic responses (reshoring, price adjustments, supplier
        diversification)""")
    
    team_leader.print_response(
        analysis_query,
        stream=True,
        stream_intermediate_steps=True,  # Show progress from each agent
        show_full_reasoning=True,  # Display reasoning process
    )

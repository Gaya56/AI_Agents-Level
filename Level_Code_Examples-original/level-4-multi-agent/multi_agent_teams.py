... imports

web agent = Agent(
  name="Web Search Agent",  
  role="Handle web search requests", 
  model= OpenAIChat(id="gpt-4o-mini"),
  tools=[DuckDuckGoTools()],
  instructions="Always include sources",
)

finance_agent= Agent(
  name="Finance Agent",
  role="Handle financial data requests",
  model=OpenAIChat(id="gpt-4o-mini"),
  tools=[YFinanceTools()],
  instructions=[
    "You are a financial data specialist. Provide concise and accurate data.",
    "Use tables to display stock prices, fundamentals (P/E, Market Cap)",
  ],
)


team_leader = Team (
  name="Reasoning Finance Team Leader", 
  mode="coordinate",
  model=Claude(id="claude-3-7-sonnet-latest"),
  members=[web_agent, finance_agent],
  tools=[ReasoningTools(add_instructions=True)],
  instructions=[
    "Use tables to display data",
    "Only output the final answer, no other text.",
  ],
  show_members_responses=True, 
  enable_agentic_context=True, 
  add_datetime_to_instructions=True,
  success_criteria="The team has successfully completed the task.",
)


if __name__ == "__main__":
  team_leader.print_response(
    """\
    Analyze the impact of recent US tariffs on market performance across
these key sectors:
- Steel & Aluminum: (X, NUE, AA)
- Technology Hardware: (AAPL, DELL, HPQ)

For each sector:
1. Compare stock performance before and after tariff implementation
2. Identify supply chain disruptions and cost impact percentages
3. Analyze companies' strategic responses (reshoring, price adjustments, supplier
diversification)""",
  stream=True, 
  stream_intermediate_steps=True, 
  show_full_reasoning=True,
)

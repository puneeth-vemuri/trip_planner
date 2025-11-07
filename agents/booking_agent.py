from crewai import Agent

def create_booking_agent():
    """Creates a flight booking research agent"""
    return Agent(
        role='Flight Booking Specialist',
        goal='Find the best flight options between origin and destination cities',
        backstory="""You are an expert flight booking agent with extensive knowledge of 
        flight routes, airlines, and booking strategies. You provide recommendations on 
        flight options, timing, and booking advice for the best travel experience.""",
        verbose=True,
        allow_delegation=False,
        llm='openrouter/mistralai/mistral-7b-instruct'
    )

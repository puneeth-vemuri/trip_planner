from crewai import Crew, Task
from agents.booking_agent import create_booking_agent
from agents.destination_researcher import create_destination_researcher
from agents.itinerary_planner import create_itinerary_planner
from agents.budget_estimator import create_budget_estimator
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def plan_trip_with_crew_stream(origin: str, destination: str, days: int, budget: str, preferences: str, people: int = 1):
    """
    Generator that runs each agent task sequentially and yields progress events.
    Yields dicts of the form:
      { 'type': 'start'|'done'|'final'|'error', 'step': int, 'agent': str, 'result': str|None }
    The final event includes the full combined result in 'result'.
    """
    # Set up LLM for agents (using OpenRouter)
    # Try Streamlit secrets first, fallback to env variable
    try:
        import streamlit as st
        api_key = st.secrets.get("OPENROUTER_API_KEY")
    except:
        api_key = os.getenv("OPENROUTER_API_KEY")
    
    # Create LLM instance
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7
    )

    # Create agents with the LLM
    researcher = create_destination_researcher(llm)
    flight_agent = create_booking_agent(llm)
    itinerary_agent = create_itinerary_planner(llm)
    budget_agent = create_budget_estimator(llm)

    combined_sections = []

    # Step 1: Destination research
    try:
        yield {"type": "start", "step": 1, "agent": "Destination Research Specialist", "result": None}

        research_task = Task(
            description=(
                f"Research the destination '{destination}' and provide:\n"
                f"1. Overview of the city/region\n"
                f"2. Top tourist attractions and points of interest\n"
                f"3. Local culture and customs\n"
                f"4. Best activities matching these preferences: {preferences}\n\n"
                f"If you are unsure about real-time data, provide timeless highlights and typical attractions."
            ),
            agent=researcher,
            expected_output="A comprehensive destination overview with attractions and activities"
        )
        crew1 = Crew(agents=[researcher], tasks=[research_task], verbose=False)
        research_result = str(crew1.kickoff())
        combined_sections.append(("Destination Research", research_result))
        yield {"type": "done", "step": 1, "agent": "Destination Research Specialist", "result": research_result}
    except Exception as e:
        yield {"type": "error", "step": 1, "agent": "Destination Research Specialist", "result": str(e)}
        return

    # Step 2: Flight booking
    try:
        yield {"type": "start", "step": 2, "agent": "Flight Booking Specialist", "result": None}

        flight_task = Task(
            description=(
                f"Consider the trip from {origin} to {destination} for {people} traveler(s). Provide flight availability guidance,"
                f" typical routes, nearby airports, and booking tips. If exact live data is not available,"
                f" suggest general options and how to search effectively."
            ),
            agent=flight_agent,
            expected_output="Flight options and recommendations"
        )
        crew2 = Crew(agents=[flight_agent], tasks=[flight_task], verbose=False)
        flight_result = str(crew2.kickoff())
        combined_sections.append(("Flight Options", flight_result))
        yield {"type": "done", "step": 2, "agent": "Flight Booking Specialist", "result": flight_result}
    except Exception as e:
        yield {"type": "error", "step": 2, "agent": "Flight Booking Specialist", "result": str(e)}
        return

    # Step 3: Itinerary planning
    try:
        yield {"type": "start", "step": 3, "agent": "Travel Itinerary Planner", "result": None}

        itinerary_task = Task(
            description=(
                f"Create a detailed {days}-day itinerary for {destination}. Use these findings for context:\n\n"
                f"Destination research summary:\n{research_result}\n\n"
                f"Preferences: {preferences}\n\n"
                f"This trip is for {people} traveler(s).\n"
                f"Requirements:\n- Balance sightseeing with rest\n- Consider travel time between locations\n- Include meal suggestions\n- Format as Day 1, Day 2, etc., with morning/afternoon/evening"
            ),
            agent=itinerary_agent,
            expected_output=f"A detailed {days}-day itinerary with daily activities"
        )
        crew3 = Crew(agents=[itinerary_agent], tasks=[itinerary_task], verbose=False)
        itinerary_result = str(crew3.kickoff())
        combined_sections.append(("Itinerary", itinerary_result))
        yield {"type": "done", "step": 3, "agent": "Travel Itinerary Planner", "result": itinerary_result}
    except Exception as e:
        yield {"type": "error", "step": 3, "agent": "Travel Itinerary Planner", "result": str(e)}
        return

    # Step 4: Budget analysis
    try:
        yield {"type": "start", "step": 4, "agent": "Travel Budget Analyst", "result": None}

        budget_task = Task(
            description=(
                f"Create a detailed budget breakdown for a {days}-day trip to {destination}.\n"
                f"Travelers: {people} people.\n"
                f"Total budget (entered): {budget}\n\n"
                f"Consider these references (summarize where needed):\n"
                f"- Flight options summary:\n{flight_result}\n\n"
                f"- Itinerary summary:\n{itinerary_result}\n\n"
                f"Include estimates for flights, accommodation (per night), daily food, activities, local transport, and misc.\n"
                f"Provide per-person and total costs, a daily breakdown and grand total, and compare with the stated budget."
            ),
            agent=budget_agent,
            expected_output="Detailed budget breakdown with cost estimates"
        )
        crew4 = Crew(agents=[budget_agent], tasks=[budget_task], verbose=False)
        budget_result = str(crew4.kickoff())
        combined_sections.append(("Budget", budget_result))
        yield {"type": "done", "step": 4, "agent": "Travel Budget Analyst", "result": budget_result}
    except Exception as e:
        yield {"type": "error", "step": 4, "agent": "Travel Budget Analyst", "result": str(e)}
        return

    # Build final combined result
    final_text_parts = []
    for title, content in combined_sections:
        final_text_parts.append(f"## {title}\n\n{content}\n")
    final_text = "\n".join(final_text_parts)

    yield {"type": "final", "step": 5, "agent": "Crew", "result": final_text}

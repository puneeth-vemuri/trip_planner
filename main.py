"""
Trip Planner Web App Launcher
Run this file to start the Streamlit web application.

Usage:
    python main.py              # Start web app
    python main.py --cli        # Run in terminal (old CLI mode)
"""
import subprocess
import sys
import os

def run_web_app():
    """Launch the Streamlit web application"""
    # Get the path to the webapp
    webapp_path = os.path.join(os.path.dirname(__file__), "webapp.py")
    
    # Get the Python executable from the virtual environment
    venv_python = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
    
    # Check if venv exists, otherwise use system python
    if os.path.exists(venv_python):
        python_cmd = venv_python
    else:
        python_cmd = sys.executable
    
    print("🌍 Starting Trip Planner Web App...")
    print(f"📍 Using Python: {python_cmd}")
    print(f"📂 Web app: {webapp_path}")
    print("\n🚀 Launching Streamlit on http://localhost:8501")
    print("   (If port 8501 is busy, it will use the next available port)\n")
    
    # Run streamlit
    try:
        subprocess.run([
            python_cmd, 
            "-m", 
            "streamlit", 
            "run", 
            webapp_path,
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Trip Planner stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        print("\nTry running manually:")
        print(f'   {python_cmd} -m streamlit run "{webapp_path}"')

def run_cli():
    """Run the old CLI version"""
    from dotenv import load_dotenv
    from utils.api_utils import openrouter_chat

    load_dotenv()
    # Interactive user input
    print("Welcome to the Trip Planner! Please answer a few questions to get a personalized trip plan.\n")
    origin = input("Where are you starting your trip from? (City/Country): ").strip()
    destination = input("Where do you want to go? (City/Country or type, e.g. 'beach in Europe'): ").strip()
    days = input("How many days do you want your trip to be?: ").strip()
    budget = input("What is your total budget for the trip (in your currency)?: ").strip()
    preferences = input("Any special preferences? (e.g. family-friendly, adventure, sightseeing, food, etc.): ").strip()

    # Compose a prompt for the chat model
    system_prompt = "You are a travel assistant. Please help with the following:"
    user_prompt = (
        f"I am planning a trip. Here are my details:\n"
        f"- Starting from: {origin}\n"
        f"- Destination/Type: {destination}\n"
        f"- Number of days: {days}\n"
        f"- Budget: {budget}\n"
        f"- Preferences: {preferences}\n"
        "Please suggest the best destinations (if not specific), create a detailed itinerary, and estimate a reasonable budget. Return the answer in a clear, organized format."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    result = openrouter_chat(messages)

    print("\n\n########################")
    print("## Here is your trip plan:")
    print("########################\n")
    print(result)

def main():
    # Check if user wants CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        run_web_app()

if __name__ == "__main__":
    main()

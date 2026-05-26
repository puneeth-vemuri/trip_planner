# Try to use pysqlite3-binary to bypass outdated SQLite versions on Linux (e.g. Hugging Face Spaces)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
from crew_orchestrator import plan_trip_with_crew_stream
from utils.export_utils import generate_pdf_from_text


st.set_page_config(page_title="Trip Planner AI", page_icon="🌍")
st.title("🌍 Trip Planner AI")
st.write("Fill in your trip details to get a personalized plan powered by AI agents!")

with st.form("trip_form"):
    origin = st.text_input("Where are you starting your trip from? (City/Country)")
    destination = st.text_input("Where do you want to go? (City/Country or type, e.g. 'beach in Europe')")
    days = st.number_input("How many days do you want your trip to be?", min_value=1, max_value=60, value=5)
    budget = st.text_input("What is your total budget for the trip (in your currency)?")
    preferences = st.text_input("Any special preferences? (e.g. family-friendly, adventure, sightseeing, food, etc.)")
    people = st.number_input("How many people are traveling?", min_value=1, max_value=20, value=2, step=1)
    submitted = st.form_submit_button("Get My Trip Plan!")

if submitted:
    if not origin or not destination:
        st.error("⚠️ Please fill in at least the departure and destination fields!")
    else:
        # Create progress placeholders
        st.markdown("## 🤖 AI Agents Working on Your Trip Plan")
        
        progress_container = st.container()
        
        with progress_container:
            step1 = st.empty()
            step2 = st.empty()
            step3 = st.empty()
            step4 = st.empty()
            final_status = st.empty()
        
        # Display initial waiting states
        step1.markdown("**📍 Destination Research Specialist**\n\nStatus: ⏳ Waiting")
        step2.markdown("**✈️ Flight Booking Specialist**\n\nStatus: ⏳ Waiting")
        step3.markdown("**📋 Travel Itinerary Planner**\n\nStatus: ⏳ Waiting")
        step4.markdown("**💰 Travel Budget Analyst**\n\nStatus: ⏳ Waiting")

        result = None
        try:
            # Stream real-time progress from the crew
            for event in plan_trip_with_crew_stream(
                origin=origin,
                destination=destination,
                days=days,
                budget=budget,
                preferences=preferences,
                people=people
            ):
                etype = event.get("type")
                estep = event.get("step")
                if etype == "start":
                    if estep == 1:
                        step1.markdown("**📍 Destination Research Specialist**\n\nStatus: 🔄 Working...")
                    elif estep == 2:
                        step2.markdown("**✈️ Flight Booking Specialist**\n\nStatus: 🔄 Working...")
                    elif estep == 3:
                        step3.markdown("**📋 Travel Itinerary Planner**\n\nStatus: 🔄 Working...")
                    elif estep == 4:
                        step4.markdown("**💰 Travel Budget Analyst**\n\nStatus: 🔄 Working...")
                elif etype == "done":
                    if estep == 1:
                        step1.markdown("**📍 Destination Research Specialist**\n\nStatus: ✅ Completed")
                    elif estep == 2:
                        step2.markdown("**✈️ Flight Booking Specialist**\n\nStatus: ✅ Completed")
                    elif estep == 3:
                        step3.markdown("**📋 Travel Itinerary Planner**\n\nStatus: ✅ Completed")
                    elif estep == 4:
                        step4.markdown("**💰 Travel Budget Analyst**\n\nStatus: ✅ Completed")
                elif etype == "error":
                    agent = event.get("agent", "Agent")
                    msg = event.get("result", "Unknown error")
                    st.error(f"❌ {agent} failed: {msg}")
                    break
                elif etype == "final":
                    result = event.get("result")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            result = None

        if result is not None:
            # Final status
            final_status.success("🎉 **Crew Execution Completed!** Your trip plan is ready.")
            
            # Display result
            st.markdown("---")
            st.markdown("## 📝 Your Trip Plan:")
            st.markdown(
                f"**Trip Summary**  "+
                f"From: {origin} → To: {destination}  |  Days: {days}  |  People: {people}  |  Budget: {budget}")
            
            # Clean the result text to remove strikethrough formatting
            cleaned_result = result.replace("~~", "").replace("<del>", "").replace("</del>", "").replace("<s>", "").replace("</s>", "")
            
            try:
                st.markdown(cleaned_result, unsafe_allow_html=True)
            except Exception:
                st.write(cleaned_result)

            # PDF Export
            st.divider()
            st.subheader("Export Your Plan")
            
            with st.spinner("Rendering PDF..."):
                pdf_bytes = generate_pdf_from_text(result, title="Trip Plan")
            
            # Generate dynamic filename: origin_to_destination_DDMMYYYY.pdf
            from datetime import datetime
            today = datetime.now().strftime("%d%m%Y")
            # Clean origin and destination for filename (remove spaces and special chars)
            clean_origin = "".join(c for c in origin if c.isalnum() or c in (' ', '-')).strip().replace(' ', '_')
            clean_dest = "".join(c for c in destination if c.isalnum() or c in (' ', '-')).strip().replace(' ', '_')
            filename = f"{clean_origin}_to_{clean_dest}_{today}.pdf"
            
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                key="pdf_download"
            )

# Footer
from datetime import datetime
st.markdown(
    f'<div style="text-align: center; padding: 2rem 0 1rem 0; color: #6c757d; font-size: 0.9rem; border-top: 1px solid #e9ecef; margin-top: 3rem;">© {datetime.now().year} PUNEETH VEMURI - ALL RIGHTS RESERVED</div>',
    unsafe_allow_html=True
)

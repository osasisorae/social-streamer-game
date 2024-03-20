import streamlit as st
from game_narrative import NarrativeEngine
from content_library import start_scenarios

st.title('Social Media Aggregator Game')

game = NarrativeEngine()
scenarios = [ key for key, _ in start_scenarios.items()]

option = st.selectbox(
    'Choose start scenario',
     scenarios)

if option:
    context = start_scenarios[option]
    st.write(context)

action = st.chat_input("what action would you like to take?")
if action:
    response = game.generate_creative_response(
        action=action,
        context=context)
    
    st.write_stream(game.stream_text_generator(response['narrative']))
    context = response['action_effect']
    # st.write_stream(game.stream_text_generator(response['action_effect']))
    # st.write({"action": action, "context": context})
    # st.write(response)
# Sidebar for game stats (this could dynamically update based on game progress)
st.sidebar.markdown("### Game Stats")
st.sidebar.markdown("**Followers:** 100")  # Placeholder for follower count

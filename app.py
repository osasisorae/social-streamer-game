import streamlit as st
from game_narrative import NarrativeEngine
from content_library import start_scenarios

st.title('Social Media Aggregator Game')

game = NarrativeEngine()
scenarios = [ key for key, _ in start_scenarios.items()]

option = st.selectbox(
    'Choose start scenario',
     scenarios)

if 'context' not in st.session_state:
    st.session_state.context = None
    
if option and st.session_state.context is None:
    st.session_state.context = start_scenarios[option]
    st.write(st.session_state.context)

action = st.chat_input("what action would you like to take?")

if action and st.session_state.context:
    response = game.generate_creative_response(
        action=action,
        context=st.session_state.context)
    
    print(f"Context: {st.session_state.context}\nAction: {action}")
    

    st.write_stream(game.stream_text_generator(response['narrative']))
    st.session_state.context = response['action_effect']


st.sidebar.markdown("### Game Stats")
st.sidebar.markdown("**Followers:** 100")  # Placeholder for follower count

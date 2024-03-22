import streamlit as st
from game_narrative import NarrativeEngine
from content_library import start_scenarios, intro
import time

st.title("TextTrek: The Wanderer's Chronicles")

def response_generator(response: str):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

game = NarrativeEngine()
scenarios = [ key for key, _ in start_scenarios.items()]

expand = st.expander("Choose gameplay scenario")
with expand:
    scenario = st.radio("Select one:", scenarios)
expand.write(intro)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if 'context' not in st.session_state:
    st.session_state.context = None
        
print(scenario)
start_context = start_scenarios[scenario]
st.session_state.context = start_context

if scenario and start_context:
    # Display assistant response in chat message container
    if st.session_state.context:
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(st.session_state.context))
    else:
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(start_context))
        
# Accept user input
if prompt := st.chat_input("What action would you like to take?"):
    
    response = game.generate_creative_response(
        action=prompt,
        context=st.session_state.context)
    st.session_state.messages.append({"role": "assistant", "content": response['narrative'], "name": scenario})
    st.session_state.messages.append({"role": "user", "content": response['action_effect'], "name": scenario, "action": prompt})
    st.session_state.context = response['action_effect']
    

for message in st.session_state.messages:
    if message['name'] == scenario:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

print(st.session_state.messages)


# st.sidebar.markdown("### Game Stats")
# st.sidebar.markdown("**Followers:** 100")  # Placeholder for follower count

import streamlit as st
from game_narrative import NarrativeEngine
from content_library import start_scenarios, intro
import time

st.title("TextTrek: The Wanderer's Chronicles")

user_email = "osasisorae@gmail.com"
user_id = "54qtrfs8dguh23489"

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
messages = game.load_messages_from_file(f"{user_id}_{user_email}.json", scenario)
print(type(messages))
print(messages)
if len(messages) > 0:
    st.session_state.messages = messages
    # initialize context
    st.session_state.context = messages[-1]['content']
else:
    st.session_state.messages = []
    start_context = start_scenarios[scenario]
    st.session_state.context = start_context

if scenario and st.session_state.context:
    # Display assistant response in chat message container
    if start_scenarios[scenario] == st.session_state.context:
        st.write_stream(response_generator(st.session_state.context))
    else:
        # print(st.session_state.context)
        st.write_stream(response_generator(scenario))

# Accept user input
if prompt := st.chat_input("What action would you like to take?"):
    
    response = game.generate_creative_response(
        file_path=f"{user_id}_{user_email}.json",
        action=prompt,
        context=st.session_state.context)
    
    # Update chat history
    assistant_msg = {"role": "assistant", "content": response['narrative'], "name": scenario}
    user_msg = {"role": "user", "content": response['action_effect'], "name": scenario, "action": prompt}
    
    game.store_messages_to_file(f"{user_id}_{user_email}.json", assistant_msg)
    game.store_messages_to_file(f"{user_id}_{user_email}.json", user_msg)
    
    
    st.session_state.messages.append(assistant_msg)
    st.session_state.messages.append(user_msg)
    st.session_state.context = response['action_effect']
    

for message in st.session_state.messages:
    if message['name'] == scenario:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    st.divider()

print(st.session_state.messages)


# st.sidebar.markdown("### Game Stats")
# st.sidebar.markdown("**Followers:** 100")  # Placeholder for follower count

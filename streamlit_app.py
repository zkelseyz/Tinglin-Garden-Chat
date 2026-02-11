import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🌳 亭林园游览推荐")
st.write(
    "欢迎使用亭林园游览推荐系统！这个聊天助手会根据您的需求提供亭林园的游览建议。"
    "您可以询问关于亭林园的历史、景点信息或推荐的游览路线等。"
    "要使用此应用，您需要提供 OpenAI API 密钥，您可以在 [这里](https://platform.openai.com/account/api-keys) 获取。"
    "您还可以通过 [这个教程](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) 学习如何构建此应用。"
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("请输入您的 OpenAI API 密钥以继续使用。", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("您想了解亭林园的哪些信息？"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

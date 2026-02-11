import streamlit as st
from openai import OpenAI

# Show title and description based on the selected language
lang = st.selectbox("Select Language / 选择语言", ["English", "中文"])

if lang == "English":
    # English Version
    st.title("🌳 Tinglin Garden Tour Recommendations")
    st.write(
        "Welcome to the Tinglin Garden Tour Recommendation system! This chatbot will provide you with tour suggestions based on your needs. "
        "You can ask about the history, attractions, or recommended routes in Tinglin Garden."
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
        "You can also learn how to build this app step by step by [following this tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
    )
    chat_input_placeholder = "What information would you like to know about Tinglin Garden?"
    info_message = "Please enter your OpenAI API key to continue using the app."
else:
    # Chinese Version
    st.title("🌳 亭林园游览推荐")
    st.write(
        "欢迎使用亭林园游览推荐系统！这个聊天助手会根据您的需求提供亭林园的游览建议。"
        "您可以询问关于亭林园的历史、景点信息或推荐的游览路线等。"
        "要使用此应用，您需要提供 OpenAI API 密钥，您可以在 [这里](https://platform.openai.com/account/api-keys) 获取。"
        "您还可以通过 [这个教程](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) 学习如何构建此应用。"
    )
    chat_input_placeholder = "您想了解亭林园的哪些信息？"
    info_message = "请输入您的 OpenAI API 密钥以继续使用。"

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info(info_message, icon="🗝️")
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

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input(chat_input_placeholder):

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


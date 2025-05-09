import streamlit as st
import recorder as rc
import base64
import llm 

st.set_page_config(layout="wide")

st.title("ReportGPT")
st.divider()

left_col, right_col = st.columns([0.65,0.35],border=True,)

with left_col:
    st.subheader("Analysis:", divider="gray")
    analysis_con = st.container(height=500)
    upload_button, analysis_button = st.columns([0.7,0.3])

    if "language" not in st.session_state:
        st.session_state.language = "English"

    image_file = upload_button.file_uploader("Upload file",label_visibility="collapsed",type=["jpeg","jpg","png"])
    
    if image_file is not None:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    if "img_response" not in st.session_state:
        st.session_state["img_response"] = ""

    if analysis_button.button("Show Analysis",use_container_width=True):
        response = llm.report_chain.invoke(
            {"image_data": image_data,
             "language": st.session_state.language}
        )
        st.session_state.img_response = response.content
    
    with analysis_button:
        on = st.toggle("Hindi/English")

        if on:
            st.session_state.language = "Hindi"
        else:
            st.session_state.language = "English"

    with analysis_con:
        st.markdown(st.session_state.img_response, unsafe_allow_html=True)





with right_col:
    st.subheader("Chat:", divider="gray")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    
    chat_con = st.container(height=500)
    with chat_con:
        for message in st.session_state.messages:
            with st.chat_message(message["role"],):
                st.markdown(message["content"])
    
    query = None
    
    if st.button(label="Speak", icon=":material/mic:", use_container_width=True):
        audio_data = rc.record_audio()
        query = "voice: " + llm.audio_to_text(audio_data)
    
    text_query = st.chat_input()
    if text_query:
        query = text_query
    
    if query:
        
        retrieved_docs = llm.vector_store.similarity_search(query)
        information = "\n\n".join(doc.page_content for doc in retrieved_docs)

        with chat_con.chat_message("user"):
            if "voice: " in query:
                st.markdown(f"*{query}*")
            else:
                st.markdown(query)


        response = llm.chat_chain.invoke(
            {
                "messages": st.session_state.messages,
                "input": query,
                "context": st.session_state.img_response,
                "information": information,
                "language": st.session_state.language
            }
        )

        with chat_con.chat_message("assistant"):
            st.markdown(response.content)
        
        st.session_state.messages.append({"role":"user", "content":query})
        st.session_state.messages.append({"role":"assistant","content":response.content})





import streamlit as st


from PromptMessage import *
from VideoTextClass import *
from GptSummary import *
# from ClassLab45API import *
from GptSummary import *
import pytube
from extract_information import *
from DocumentReaderLangchain import *
import os

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

openai_api_key = key

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Save uploaded file locally.
def save_uploaded_file(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return

# Process Uploaded video
def process_uploaded_video(video_path):
    vidText = LinkVideoTimelyText(video_path)
    transcript = vidText.getText()
    return transcript
    

# Process Youtube link
def process_youtube_link(url):
    youtube=pytube.YouTube(url)
    stream=youtube.streams.get_audio_only()
    stream.download(output_path=r'youtube_path', filename='youtube_video.mp4') # store in the localhost
    path = r'youtube_path\youtube_video.mp4'
    vidText = LinkVideoTimelyText(path)
    transcript = vidText.getText()
    return transcript

def get_final_summary(system_msg, transcript):
    # Creating object of class for generating summary using gpt.
    gptSumm = Gptresponse(system_msg, transcript)
    final_summary = gptSumm.getSummary()
    return final_summary

# create function to download the transcript
def download_transcript(trascript):
    text_file = open(r'transcript_path\transcript.doc', 'w')
    trascript = trascript
    text_file.write(trascript)
    text_file.close()
    return

def main():
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    [role=radiogroup]{
        gap: 0.5rem;
    }
    
    [data-testid=stSidebar] {
            background-color: #EBE8E8;
        }
    </style>
    """,unsafe_allow_html=True)
    
    st.sidebar.image('img\logo_png.png')
 
    # Add space below radio button options
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    st.sidebar.title("Please select below application to use")
    selected_option = st.sidebar.radio("Choose an app", ("Upload Your video", "Paste your YouTube link", "Upload your document", "Chat with your Document"))
    
    # Add space below radio button options
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
     # Description for each radio button
    if selected_option == "Upload Your video":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. Upload a MP4, MOV or MPEG4 file.")
        st.sidebar.write("2. Click on the 'Upload video' button.")
        st.sidebar.write("3. You will get the Topic, Sentiment and Conclusion for uploaded video.")
       
        
        
    elif selected_option == "Paste your YouTube link":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. 'Paste your YouTube link' in the provided text input.")
        st.sidebar.write("2. Click 'Submit' to process the YouTube link.")
        st.sidebar.write("3. You will get the Topic, Sentiment, Conclusion for and summary with time frame for given YT video link.")

    elif selected_option == "Upload your document":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. 'Upload your document'.")
        st.sidebar.write("2. Click on the 'Submit' button.")
        st.sidebar.write("3. You will get the Topic and summary for that document")
        
        
    elif selected_option == "Chat with your Document":
        st.sidebar.markdown("## How to Use?")
        st.sidebar.write("1. 'Upload your document'.")
        st.sidebar.write("2. Ask any questions related to your document")
        st.sidebar.write("3. Please ask your question in send section")
        
        
    
    # Add space below radio button options
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("## About!")
    st.sidebar.write("The features will be answered by OpenAI LLM GPT-3.5 Model")
    st.sidebar.write("")
    st.sidebar.write("This work in progress Please connect with:")
    st.sidebar.write("atul.bhardwaj@gamil.com")
    st.sidebar.write("subodh.thore@gmail.com")
    st.sidebar.write("govind.biradar@gmail.com")
    

    
    # Video Upload
    if selected_option == "Upload Your video":
        st.title("Upload Your Video")
        uploaded_video = st.file_uploader("Upload video", type=["mp4", "mov"])
        
        col_upvd_1, col_upvd_2 = st.columns([2, 1])
        upd_vid_final_summary = None
        
        with col_upvd_1:
            if uploaded_video is not None:
                if st.button("Upload video"):
                    st.success('Your file successfully Submitted.', icon="✅")
                    with st.spinner('Please wait.. Your Video is processing!'):
                        save_uploaded_file(uploaded_video)
                        uploaded_video_path = r"uploads\{}".format(uploaded_video.name)
                        upd_vid_transcript = process_uploaded_video(uploaded_video_path)
                        upd_vid_final_summary = get_final_summary(system_msg, upd_vid_transcript)
                        topic, sentiment, conclusion, summary = extract_information(upd_vid_final_summary)
                            
                        st.write('Topic :',topic)
                        st.write('Sentiment :',sentiment)
                        st.write('Conclusion :',conclusion)
                        st.write('Summary :',summary)
                        # Here you can implement the functionality for processing the uploaded video
                    st.success('Thanks for using  our service!')
                    
        with col_upvd_2:
            if upd_vid_final_summary is not None:
                doc_path = r"transcript_path\transcript.doc"
                with open(doc_path, "rb") as file:
                    doc = file.read()
                    st.download_button(label="Download Video Transcript", data=doc, file_name="transcript.doc")

    #youtube
    elif selected_option == "Paste your YouTube link":
        st.title("Paste Your YouTube Link")
        youtube_link = st.text_input("Paste your YouTube link here:")
        
        # Create two columns
        col_yt_1, col_yt_2 = st.columns([2, 1])
        yt_final_summary = None
        with col_yt_1:
            if st.button("Submit"):
                with st.spinner('Please wait.. Your link is processing!'):
                    yt_transcript = process_youtube_link(youtube_link)
                    download_transcript(yt_transcript)
                    yt_final_summary = get_final_summary(system_msg, yt_transcript)
                    topic, sentiment, conclusion, summary = extract_information(yt_final_summary)
                    
                    st.write('Topic :',topic)
                    st.write('Sentiment :',sentiment)
                    st.write('Conclusion :',conclusion)
                    st.write('Summary :',summary)
                    st.write('')
                st.success('Thanks for using our service!')
                
        # Download button
        with col_yt_2:
            if yt_final_summary is not None:
                doc_path = r"transcript_path\transcript.doc"
                with open(doc_path, "rb") as file:
                    doc = file.read()
                    st.download_button(label="Download Video Transcript", data=doc, file_name="transcript.doc")
            
            # Here you can implement the functionality for processing the YouTube link
            
    # Document Upload
    elif selected_option == "Upload your document":
        st.title("Upload Your Document")
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Submit"):
                st.success('Your file successfully Submitted.', icon="✅")
                with st.spinner('Please wait.. Your document is processing!'):
                    save_uploaded_file(uploaded_file)
                    docgptlangresponse = DocGptLangResponse("uploads\{}".format(uploaded_file.name))
                    doc_summary = docgptlangresponse.getDocSummary()
                    st.write(doc_summary)
                st.success('Thanks for using our service!')
                # Here you can implement the functionality for processing the uploaded PDF file
                
    # Document Chat
    elif selected_option == "Chat with your Document":
        st.title("Welcome to Custom Document chat")
        st.write("This feature unables you chat with your custom uploaded documents. For example: Provide a document of any any syllabus and ask to 'prepare set of questions to take exam'.")
        
        # Set up memory
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        if len(msgs.messages) == 0:
            msgs.add_ai_message("How can I help you! With this document?")
        
        uploaded_file_doc_chat = st.file_uploader("Upload PDF file", type=["pdf"])
        
        if uploaded_file_doc_chat:
            # st.success('Your file successfully Submitted. S', icon="✅")
            st.markdown("<hr>", unsafe_allow_html=True)
            save_uploaded_file(uploaded_file_doc_chat)
            docgptlangresponse = DocGptLangResponse("uploads\{}".format(uploaded_file_doc_chat.name))
            doc_context = docgptlangresponse.doc_context()
            
            prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an AI chatbot having a conversation with a human regarding document context, Human can ask you question based on document context. following is the document context:"+doc_context),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
            )
            
            chain = prompt | ChatOpenAI(api_key=openai_api_key)
            chain_with_history = RunnableWithMessageHistory(
                chain,
                lambda session_id: msgs,
                input_messages_key="question",
                history_messages_key="history",
            )
            # Render current messages from StreamlitChatMessageHistory
            for msg in msgs.messages:
                st.chat_message(msg.type).write(msg.content)
                
            # If user inputs a new prompt, generate and draw a new response
            if prompt := st.chat_input():
                st.chat_message("human").write(prompt)
                # Note: new messages are saved to history automatically by Langchain during run
                config = {"configurable": {"session_id": "any"}}
                response = chain_with_history.invoke({"question": prompt}, config)
                st.chat_message("ai").write(response.content)

                        
            
        
    

    else:
        st.title("Welcome to the App")
        st.write("Please select an option from the sidebar to proceed.")

if __name__ == "__main__":
    main()










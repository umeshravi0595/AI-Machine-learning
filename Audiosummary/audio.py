from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
import streamlit as st
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import assemblyai as aai
import os
from dotenv import load_dotenv
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
aai.settings.api_key = "dadbbd65a132428bb4cbde4a36663f9f" 

model=ChatGroq(model="gemma2-9b-it")
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
from langchain_huggingface import HuggingFaceEmbeddings
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

st.set_page_config(page_title="Sharon Model: Summarize content from audio file",page_icon='▶️')
st.title("Sharon to Summarize content for your Audio")
# File uploader for audio files
uploaded_files = st.file_uploader(
    "Please upload the audio files",
    type=["mp3", "wav", "ogg"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        st.write(f"Processing uploaded file: {file.name}")
        
        # Save the uploaded file content temporarily
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        
        # Initialize the transcriber
        transcriber = aai.Transcriber()

        # Configure transcription settings
        config = aai.TranscriptionConfig(speaker_labels=True)

        # Transcribe the uploaded audio file
        try:
            transcript = transcriber.transcribe(file.name, config)

            # Check transcription status
            if transcript.status == aai.TranscriptStatus.error:
                st.error(f"Transcription failed for {file.name}: {transcript.error}")
                continue

            # Display the transcription text
            st.subheader(f"Transcription for {file.name}:")
            transcript_text=transcript.text
            docs = [Document(page_content=transcript_text)]
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
            splits=text_splitter.split_documents(docs)
            vectorstore=Chroma.from_documents(documents=splits,embedding=embeddings)
            retriever=vectorstore.as_retriever()
            # st.write(transcript.text)
            system_prompt=(
            "You are an AI trained assistant to analyze conversations between a salesperson and a customer."
            "Your task is to focus specifically on the points made by the salesperson to persuade the customer."
            "After reading the conversation, summarize the persuasive points from the salesperson in bullet points," 
            "highlighting the arguments, benefits, or strategies used by the salesperson to convince the customer"
            "\n\n"
            "{context}"
            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("human", "{input}"),
                ]
            )

            question_answer_chain=create_stuff_documents_chain(model,prompt)
            rag_chain=create_retrieval_chain(retriever,question_answer_chain)
            response=rag_chain.invoke({"input":"can u give me the conversations where sales person try to convince with customer"})
            st.write(response['answer'])

            # Display speaker utterances if available
        #     if transcript.utterances:
        #         for utterance in transcript.utterances:
        #             st.write(f"Speaker {utterance.speaker}: {utterance.text}")
        #     else:
        #         st.write("No distinct utterances found.")
        except Exception as e:
            st.error(f"An error occurred while processing {file.name}: {e}")

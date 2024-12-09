import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from youtube_transcript_api.formatters import TextFormatter
from langchain.chains import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.docstore.document import Document  # Import Document
import validators

import textwrap
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
# Streamlit UI
st.set_page_config(page_title="Sharon Model: Summarize content from YT or Website", page_icon="▶️")
st.title("Sharon Model Summarize content from YT or Website")
st.sidebar.text_input("Enter your Email Address")

url = st.text_input("Paste your URL link below:")
summarize_english = st.button("Summarize")

# Define LLM and Prompt
llm = ChatGroq(model="gemma2-9b-it")
prompt_template = """
Provide a summary for content in 300 words:
content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

def extract_video_id(youtube_url):
    """Extract video ID from the YouTube URL."""
    import re
    match = re.search(r"v=([a-zA-Z0-9_-]+)", youtube_url)
    if match:
        return match.group(1)
    else:
        return None
# Helper function to split text into smaller chunks
def split_text(text, max_length=2000):
    """Split the text into chunks that fit within the OpenAI token limit."""
    return textwrap.wrap(text, max_length)

# Truncate text if it exceeds the length limit
def truncate_text(text, max_tokens=2000):
    tokens_per_word = 0.75  # Approximation
    max_words = int(max_tokens / tokens_per_word)
    words = text.split()
    
    if len(words) > max_words:
        text = " ".join(words[:max_words]) + "..."
    
    return text

if summarize_english:
    if not url.strip() and not validators.url(url):
        st.error("Please provide a valid  URL.")
    elif "youtube.com" not in url and "youtu.be" not in url and not validators.url(url):
        st.error("Please provide a valid YouTube URL.")
    else:
        try:
            with st.spinner("Waiting..."):
                # Extract video ID
                video_id = extract_video_id(url)
                
                if video_id:
                    # Fetch transcript for the video
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    transcript = transcript_list.find_generated_transcript(['en','ta','hi'])
                    transcript_data = transcript.fetch()

                    # Format the transcript
                    formatter = TextFormatter()
                    transcript_text = formatter.format_transcript(transcript_data)
                    transcript_split=truncate_text(transcript_text)
                    # Create content for summarization
                    video_title = YouTube(url).title
                    content = f"Title: {video_title}\n\nTranscript: {transcript_split}"

                    # Wrap content in a Document object
                    docs = [Document(page_content=content)]  # Correct structure with `page_content`

                    # Summarize the content
                    # chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    # response = chain.run(docs)
                else:
                    
                  loader=UnstructuredURLLoader(urls=[url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                  docs=loader.load()
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                response=chain.run(docs)
                st.success("Summary:")
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import streamlit as st
import validators
from pytube import YouTube
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')



# Custom PatchedYoutubeLoader
# class PatchedYoutubeLoader:
#     def __init__(self, video_url: str, add_video_info: bool = False):
#         self.video_url = video_url
#         self.add_video_info = add_video_info
#         self.video_id = video_url.split("v=")[-1]

#     def _get_video_metadata(self) -> dict:
#         yt = YouTube(
#             f"https://www.youtube.com/watch?v={self.video_id}",
#             use_oauth=True,
#             allow_oauth_cache=True,
#         )
#         return {
#             "title": yt.title,
#             "description": yt.description,
#             "author": yt.author,
#             "length": yt.length,
#             "keywords": yt.keywords,
#         }

#     def load(self) -> list:
#         metadata = self._get_video_metadata()
#         content = metadata.get("description", "")
#         return [Document(page_content=content, metadata=metadata)]
    
#streamlit app title

st.set_page_config(page_title="Sharon Model: Summarize content from YT or Website",page_icon='▶️')
st.title("Summarize content from YT or Website")
st.sidebar.text_input("Enter your Email Address")

url=st.text_input('Paste your Url link below:')
summarize_english=st.button("Summarize")
llm=ChatGroq(model="gemma2-9b-it")

prompt_template="""
provide a summary for content in 300 words:
content:{text}
"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if summarize_english:
   if  not validators.url(url):
      st.error("Please enter a valid Url")

   else:
       
         with st.spinner("waiting..."):
            if "youtube.com" in url:
               loader=YoutubeLoader(url,add_video_info=True)
               # Extract video title and description
            #    video_title = yt.title
            #    video_description = yt.description
                   
                # Combine title and description for summarization
            #    content = f"Title: {video_title}\n\nDescription: {video_description}"
            #    docs = [{"page_content": content}]  # Format compatible with LangChain
            else:
               loader=UnstructuredURLLoader(urls=[url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
            docs=loader.load()
            chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
            response=chain.run(docs)
            st.success(response)

       
          




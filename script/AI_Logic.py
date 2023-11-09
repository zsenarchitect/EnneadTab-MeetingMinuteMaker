

from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import pickle


import os
import json

import time

import shutil




class Logic_Solution:

    def process_pdf(self, file):
        pdf_reader = PdfReader(file)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        
        self.process_text(text)

    def process_text(self, text):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        embeddings = OpenAIEmbeddings(openai_api_key=self.KEY)

        # FAISS is a vectorstore obj
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open(self.local_embeding, "wb") as f:
            pickle.dump(VectorStore, f)

        self.vectors = VectorStore

    @property
    def local_embeding(self):
        return self.get_file_in_dump_folder(f"{self.store_name}.pkl")

    def is_vector_store_exists(self):

        if os.path.exists(self.local_embeding):
            with open(self.local_embeding, "rb") as f:
                self.vectors = pickle.load(f)
            return True
        return False

    def get_response(self, query):

        docs = self.vectors.similarity_search(query=query, k=5)

        llm = OpenAI(openai_api_key=self.KEY)
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=query)
            print(cb)

        return response

    def get_data_file(self):
        return self.get_file_in_dump_folder("MeetingMinuteMaker_Data.json")

    def get_file_in_dump_folder(self, file):

        return "{}\Documents\EnneadTab Settings\Local Copy Dump\{}".format(os.environ["USERPROFILE"], file)

    def has_new_job(self):
        file = self.get_data_file()

        file = shutil.copyfile(
            file, self.get_file_in_dump_folder("MeetingMinuteMaker.json"))
        with open(file, 'r') as f:
            # get dictionary from json file
            data = json.load(f)

        return data["direction"] == "IN"

  
    def main(self):
        
        begin_time = time.time()
        file = self.get_data_file()
        with open(file, 'r') as f:
            # get dictionary from json file
            data = json.load(f)

        self.KEY = data.get('api_key')
        # this should be controled from Revit side to maintain consiststn over multiple query
        self.store_name = data.get('store_name')
        print(self.store_name)
        if not self.is_vector_store_exists():
            print("vect stroe no existent")
            
            method = data.get('method')
            if method == 'pdf':
                report_address = data["qaqc_file"]
                self.process_pdf(report_address)
            elif method == 'text':
                self.process_text(data.get("qaqc_text"))

        response = self.get_response(data.get("query"))
        print("Response = " + response)
        data["response"] = response
        data["direction"] = "OUT"
        data["compute_time"] = time.time() - begin_time
      
        with open(file, 'w') as f:
            # get dictionary from json file
            json.dump(data, f)


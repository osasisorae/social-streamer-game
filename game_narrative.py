from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from decouple import config
from langchain_community.document_loaders import JSONLoader
import json
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

class GameNarrative(BaseModel):
    narrative: str = Field(description="Narrative continuation based on player's action.")
    action_effect: str = Field(description="Effect of the player's action on the game world.")


class NarrativeEngine:
    def __init__(self):
        # Setup JSON output parser with the GameNarrative data model
        self.parser = JsonOutputParser(pydantic_object=GameNarrative)
        self.model = ChatOpenAI(api_key=config('OPENAI_API_KEY'), model="gpt-4-1106-preview", temperature=0)
        self.prompt = PromptTemplate(
            # template="""
            #     When provided a context and a players action, generate a narrative
            #     continuation that directly follows from the action within the same 
            #     scenario. Ensure the narrative and action effect are closely related 
            #     to the action described.\n{format_instructions}\n{context}\n{action}
            #     """,
            template="""
                Previous Conversation:\n{previous_conversation}\n
                Given the latest context and the player's action below, generate a narrative
                continuation that directly follows from the action within the same scenario. 
                Ensure the narrative and action effect are closely related to the action described.\n
                Latest Context: {context}\n
                Latest Action: {action}\n
                Please provide the response in the following format:\n{format_instructions}
                """,
            input_variables=["context", "action", "previous_conversation"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.model | self.parser

    
    def generate_creative_response(self, action, context):
        file_path = 'context_action_log.json'
        # Load the previous conversation context as a narrative string
        previous_conversation = self.load_context_action_from_file(file_path)
        
        # Pass the previous conversation directly into the prompt
        response = self.chain.invoke({
            "context": context,
            "action": action,
            "previous_conversation": previous_conversation
        })
        
        # response = self.chain.invoke({"context": context, "action": action})
        
        self.store_context_action_to_file(file_path, context, action)
        
        return response
    
    def stream_text_generator(self, input_text, chunk_size=1):
        """
        A generator function that streams a string in chunks.

        :param input_text: The text to be streamed.
        :param chunk_size: The number of characters to yield in each chunk.
        """
        for i in range(0, len(input_text), chunk_size):
            yield input_text[i:i + chunk_size]
            
    def store_context_action_to_file(self, file_path, context, action):
        """
        Store and append context and action pairs in a JSON file.

        :param file_path: Path to the JSON file where data will be stored.
        :param context: The context string to store.
        :param action: The action string to store.
        """
        data = {"context": context, "action": action}

        # Check if the file exists and has content; if so, load existing data
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Append the new data
        existing_data.append(data)

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
            
    def load_context_action_from_file(self, file_path):
        jq_schema = '.'
        loader = JSONLoader(file_path=file_path, jq_schema=jq_schema, text_content=False)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        retriever = db.as_retriever()
        docs = retriever.get_relevant_documents("What is the summary of the story")
        page_content = docs[0].page_content
        return page_content

    
# action = "climb up a tree"
# context = "You wake up in a forest, surrounded by towering trees and the sound of distant wildlife."

# response = chain.invoke({"context": context, "action": action})
# print(type(response))
# print(response)

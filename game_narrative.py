from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from decouple import config



class GameNarrative(BaseModel):
    narrative: str = Field(description="Narrative continuation based on player's action.")
    action_effect: str = Field(description="Effect of the player's action on the game world.")


class NarrativeEngine:
    def __init__(self):
        # Setup JSON output parser with the GameNarrative data model
        self.parser = JsonOutputParser(pydantic_object=GameNarrative)
        self.model = ChatOpenAI(api_key=config('OPENAI_API_KEY'), model="gpt-4-1106-preview", temperature=0)
        self.prompt = PromptTemplate(
            template="""
                When provided a context and a players action, generate a narrative
                continuation that directly follows from the action within the same 
                scenario. Ensure the narrative and action effect are closely related 
                to the action described.\n{format_instructions}\n{context}\n{action}
                """,
            input_variables=["context", "action"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = self.prompt | self.model | self.parser

    
    def generate_creative_response(self, action, context):

        response = self.chain.invoke({"context": context, "action": action})
        
        return response
    
    def stream_text_generator(self, input_text, chunk_size=1):
        """
        A generator function that streams a string in chunks.

        :param input_text: The text to be streamed.
        :param chunk_size: The number of characters to yield in each chunk.
        """
        for i in range(0, len(input_text), chunk_size):
            yield input_text[i:i + chunk_size]
    
# action = "climb up a tree"
# context = "You wake up in a forest, surrounded by towering trees and the sound of distant wildlife."

# response = chain.invoke({"context": context, "action": action})
# print(type(response))
# print(response)

from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Define the JSON Schema for the structured output
json_schema = {
    "title": "Headlines",
    "description": "Object containing a list of headlines ranked by importance.",
    "type": "object",
    "properties": {
        "headlines": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "headline": {"type": "string", "description": "The news headline"},
                    "url": {"type": "string", "description": "The URL of the news article"},
                    "importance": {"type": "integer", "description": "The importance rank of the headline"}
                },
                "required": ["headline", "url", "importance"]
            }
        }
    },
    "required": ["headlines"]
}

class NewsRanker:
    def __init__(self, openai_api_key):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a world-class algorithm for ranking news headlines based on their importance."),
                ("human", "Rank the following headlines based on their importance: {input}"),
                ("human", "Tip: Make sure to answer in the correct format"),
            ]
        )

    def rank_headlines(self, headlines_dict):
        # Convert the dictionary to a string format for input
        headlines_str = ', '.join(headlines_dict.keys())

        # Create the chain for structured output
        chain = create_structured_output_chain(json_schema, self.llm, self.prompt, verbose=True)
        result = chain.run(headlines_str)

        # Sort the headlines based on their importance (from most to least important)
        sorted_headlines = sorted(result["headlines"], key=lambda x: x['importance'], reverse=True)

        # Extract the headlines and URLs and return them as a list of dictionaries
        ranked_list = [{"headline": item["headline"], "url": headlines_dict[item["headline"]]} for item in sorted_headlines]

        return ranked_list

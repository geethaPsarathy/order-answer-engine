import openai
import os
from dotenv import load_dotenv
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import json


# Load .env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the OpenAI model to use
openai_model = "gpt-3.5-turbo"


async def generate_dish_insight(dish_name, summarized_reviews, user_query , tone="positive"):
    """
    Generate the final dish insight using LLM based on summarized customer reviews.
    Adjusts tone based on user input (positive, neutral, constructive).
    """
    tone_instruction = {
        "positive": "Generate a concise, friendly, and positive insight highlighting the strengths of the dish.",
        "neutral": "Generate a concise and objective insight presenting both strengths and weaknesses.",
        "constructive": "Provide constructive feedback on the dish, focusing on areas for improvement while maintaining a respectful tone."
    }
    
    prompt = f"""
    Summarize the customer feedback on the dish '{dish_name}' using the following reviews:
    {summarized_reviews} 
    and answer the {user_query} coombining the information from the reviews.
    {tone_instruction.get(tone, tone_instruction['neutral'])}
    Focus on taste, uniqueness, and commonly mentioned highlights.
    
    Generate an solid information based on the reviews and user query. Basically address all the aspects of user query with summarized reviews,user query and also provide a new information.
    
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful food critic assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        insight = response.choices[0].message.content.strip()
        print(f"[INFO] Insight generated with {tone} tone.")
        return insight

    except Exception as e:
        print(f"[ERROR] Insight generation failed: {str(e)}")
        return "Could not generate insights at this time."


async def generate_customizations(dish_name: str, insights: list, user_query: str = None):
    """
    Generate customizations for the dish.
    
    Args:
        dish_name (str): Name of the dish.
        insights (list): List of insights about the dish.
        user_query (str): User-specific query to tailor the customizations.

    Returns:
        dict: Customization suggestions.
    """
    try:
        # Construct the prompt
        prompt = f"""
        The following are insights about the dish "{dish_name}":
        {insights}
        
        User query (if provided): "{user_query or 'No specific query'}"
        
        Based on the insights and user query, generate three customization suggestions
        that could enhance the user's experience with this dish.
        
        Focus on:
        - Additions (e.g., toppings, condiments)
        - Substitutions (e.g., bun, patty)
        - Dietary adjustments (e.g., vegan, gluten-free options)
        
        Return the response in JSON format:
        {{
            "customizations": [
                "Suggestion 1",
                "Suggestion 2",
                "Suggestion 3"
            ]
        }}
        """

        # Call OpenAI API
        response = openai.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": "You are a creative culinary assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        # Parse and extract the list of customizations
        response_text = response.choices[0].message.content.strip()
        print("[INFO] Customizations Generated:\n", response_text)

        # Convert to Python dictionary
        customizations_dict = eval(response_text)
        customizations_list = customizations_dict.get("customizations", [])

        # Ensure the response is a list for FastAPI
        return customizations_list

    except Exception as e:
        print(f"[ERROR] Failed to generate customizations: {str(e)}")
        return {"error": f"Failed to generate customizations: {str(e)}"}


async def generate_suggestions(dish_name: str, insights: list):
    """
    Generate ingredient substitutions, beverage pairings, flavors, and desserts.
    
    Args:
        dish_name (str): Name of the dish.
        insights (list): List of insights about the dish.

    Returns:
        dict: Suggestions categorized into ingredients, beverages, flavors, and desserts.
    """
    try:
        # Construct the prompt
        prompt = f"""
        The following are insights about the dish "{dish_name}":
        {insights}
        
        Based on this, provide creative suggestions in the following categories:
        - 3 Ingredient Substitutions
        - 3 Beverage Pairings
        - 3 Flavor Enhancements
        - 3 Dessert Pairings
        
        Return the response in valid JSON format:
        {{
            "ingredients": ["Substitution 1", "Substitution 2", "Substitution 3"],
            "beverages": ["Beverage 1", "Beverage 2", "Beverage 3"],
            "flavors": ["Flavor Enhancement 1", "Flavor Enhancement 2", "Flavor Enhancement 3"],
            "desserts": ["Dessert 1", "Dessert 2", "Dessert 3"]
        }}
        """

        # Call OpenAI API
        response = openai.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": "You are a culinary expert providing creative dish suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Extract response and parse as JSON safely
        response_text = response.choices[0].message.content.strip()
        print("[INFO] Suggestions Generated:\n", response_text)

        # Safe parsing using json.loads
        suggestions = json.loads(response_text)

        # Validate presence of all required fields
        required_fields = ["ingredients", "beverages", "flavors", "desserts"]
        for field in required_fields:
            if field not in suggestions:
                suggestions[field] = [f"No {field} suggestions available."]

        return suggestions

    except json.JSONDecodeError:
        print("[ERROR] Failed to parse JSON response.")
        return {
            "ingredients": ["Error parsing suggestions."],
            "beverages": ["Error parsing suggestions."],
            "flavors": ["Error parsing suggestions."],
            "desserts": ["Error parsing suggestions."]
        }

    except Exception as e:
        print(f"[ERROR] Failed to generate suggestions: {str(e)}")
        return {
            "ingredients": ["Error generating ingredients."],
            "beverages": ["Error generating beverages."],
            "flavors": ["Error generating flavors."],
            "desserts": ["Error generating desserts."]
        }
# async def generate_response_from_messages(messages, user_query):
#     # Extract context from all previous messages
#     context = "\n".join(
#         [
#             f"{message['role'].capitalize()}: {message['content']}"
#             for message in messages
#             if "content" in message
#         ]
#     )

#     # Prepare the prompt for ChatGPT
#     prompt = f"""
#             The following is a conversation history between a user and an assistant. Use this context to answer the user's follow-up query.

#             Conversation History:
#             {context}

#             User's Query: {user_query}

#             Generate a response to the user query based on the conversation context.
#             """

#     # Call OpenAI's GPT API
#     try:
#         response = openai.chat.completions.create(
#             model=openai_model,
#             messages=[
#                 {"role": "system", "content": "Act like You are a powerful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             temperature=0.7,
#         )

#         # Extract the assistant's reply from the API response
#         assistant_message = response.choices[0].message.content

#         return {
#             "message": assistant_message,
#         }

#     except Exception as e:
#         return {
#             "error": f"Failed to generate response: {str(e)}",
#             "context": context  # Include full conversation context for debugging purposes
#         }

async def generate_response_from_messages(messages, user_query):
    # Extract context from all previous messages
    context = "\n".join(
        [
            f"{message['role'].capitalize()}: {message['content']}"
            for message in messages
            if "content" in message
        ]
    )

    # Prepare a simplified prompt for ChatGPT
    prompt1 = f"""
            You are a helpful assistant. Use the following conversation history to answer the user's query concisely and intuitively.
            The following are insights about the our conversation:
            Conversation History:
            {context}

            User's Query: {user_query}

            Generate a response taking both conversation history and give me a new response. Don't repeat the same information. also 
            Don't provide any information that is not relevant to the user query.
            Don't say Based on the previous information, or anything similar.
            Response should be best ,intuitive , directly adress the user query and should be concise. 
            """
    prompt2 = f"""
    You are a helpful assistant. Use the following conversation history to answer the user's query thoughtfully and comprehensively.

    Conversation History:
    {context}

    User's Query: {user_query}

    Craft a direct, engaging response that intuitively answers the query without repeating prior responses. 
    Focus on providing fresh insights that address the user’s query fully. Where necessary, expand with relevant examples or explanations to offer additional value.  
    Ensure the response is insightful, well-structured, and easy to understand.
    """

    # Call OpenAI's GPT API
    try:
        response = openai.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt1+prompt2}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        # Extract and return only the assistant's reply
        assistant_message = response.choices[0].message.content

        return {
            "message": assistant_message,
        }

    except Exception as e:
        return {
            "error": f"Failed to generate response: {str(e)}",
        }

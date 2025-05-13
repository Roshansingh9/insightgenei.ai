import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import re


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="deepseek-r1-distill-llama-70b"
)


column_mapping = {
    "State": "state",
    "Avg Daily Distance (km)": "avg_daily_distance_km",
    "Brand": "brand",
    "Model": "model",
    "Price (INR)": "price_inr",
    "Year of Manufacture": "year_of_manufacture",
    "Engine Capacity (cc)": "engine_capacity_cc",
    "Fuel Type": "fuel_type",
    "Mileage (km/l)": "mileage_kmpl",
    "Owner Type": "owner_type",
    "Registration Year": "registration_year",
    "Insurance Status": "insurance_status",
    "Seller Type": "seller_type",
    "Resale Price (INR)": "resale_price_inr",
    "City Tier": "city_tier"
}


prompt = ChatPromptTemplate.from_template(
    """
    You are an expert SQL assistant.
    Using the table `car_sales` with the following columns:
    {columns}

    Convert the following natural language question into a valid SQLite SQL query.
    Only return the SQL query without explanation.

    Question: {input}
    """
)


def generate_sql(user_input):
    columns = ', '.join(column_mapping.values())
    formatted_prompt = prompt.format_messages(
        columns=columns,
        input=user_input
    )
    response = llm.invoke(formatted_prompt)
    return response.content.strip()


def generate_query(user_input):
    sql_query = generate_sql(user_input)
    
    
    match = re.search(r'</think>(.*?)<think>', sql_query, re.DOTALL)

    if match:
        content_after_think = match.group(1).strip()  # Extract content between </think> tags
    else:
        content_after_think = "No detailed explanation available."

    
    response_json = {
        "detail": content_after_think,
        "sql_query": sql_query.split("\n")[-1].strip()  # Get the actual SQL query from the last line
    }
    return json.dumps(response_json, indent=4)

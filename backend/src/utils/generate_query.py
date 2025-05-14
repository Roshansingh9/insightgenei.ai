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

    Convert the following natural language question into a valid PostgreSQL SQL query.
    Return ONLY the SQL query without ANY explanation or markdown formatting.
    Make sure the query syntax is 100% valid for PostgreSQL.
    DO NOT include <think> tags or any explanations of your thought process.
    ONLY return the SQL query text.

    Question: {input}
    """
)


def extract_sql_query(response_text):
    
    clean_text = re.sub(r'```sql|```', '', response_text, flags=re.IGNORECASE)
    
    # Remove any <think> blocks
    clean_text = re.sub(r'<think>.*?</think>', '', clean_text, flags=re.DOTALL)
    
    # Get the actual query - typically the last part after any explanations
    lines = [line for line in clean_text.strip().split('\n') if line.strip()]
    if lines:
        # Take the last non-empty line as the query if there are multiple lines
        sql_query = lines[-1].strip()
    else:
        sql_query = clean_text.strip()
        
    return sql_query


def generate_sql(user_input):
    columns = ', '.join(column_mapping.values())
    formatted_prompt = prompt.format_messages(
        columns=columns,
        input=user_input
    )
    response = llm.invoke(formatted_prompt)
    raw_response = response.content.strip()
    
    print("Raw LLM Response:", raw_response)
    
    # Extract the actual SQL query
    sql_query = extract_sql_query(raw_response)
    
    return sql_query


def generate_query(user_input):
    sql_query = generate_sql(user_input)
    
    
    response_json = {
        "detail": "Query generated successfully",
        "sql_query": sql_query
    }
    return json.dumps(response_json, indent=4)
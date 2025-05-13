import os
import json
import sys
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
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


data_summary_prompt = ChatPromptTemplate.from_template(
    """
You are an expert data analyst. Use the following column mapping to interpret results:
{column_map}

Given the result data from a SQL query and a brief explanation, produce a clean, plain-text summary that:
- Verbally interprets the query result .
- References the relevant column meanings


Result Data (JSON):
{data}

Brief Explanation:
{explanation}

Respond with only the summary text (no markdown fences).
    """
)


def explain_query_response(json_input: str) -> str:
    parsed = json.loads(json_input)
    data_obj = parsed.get("data", [])
    explanation = parsed.get("explanation", "")

   
    map_lines = [f"- {col} maps to '{key}'" for col, key in column_mapping.items()]
    column_map_str = "\n".join(map_lines)


    formatted = data_summary_prompt.format_messages(
        column_map=column_map_str,
        data=json.dumps(data_obj, indent=4),
        explanation=explanation
    )
    llm_response = llm.invoke(formatted).content.strip()

    
    llm_response = re.sub(r"^```[\s\S]*?\n", "", llm_response)
    llm_response = re.sub(r"\n```$", "", llm_response)

   
    output = {
        "data": data_obj,
        "summary": llm_response
    }
    return json.dumps(output, indent=4)


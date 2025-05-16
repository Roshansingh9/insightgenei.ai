import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    logger.error("GROQ_API_KEY environment variable is not set")
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize the LLM
try:
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"
    )
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {str(e)}")
    raise

# Column mapping for data interpretation
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

# Prompt template for data summarization
data_summary_prompt = ChatPromptTemplate.from_template(
    """
You are an expert data analyst for a motorcycle sales database in India. Use the following column mapping to interpret results:
{column_map}

Given the result data from a SQL query and a brief explanation, produce a clean, plain-text summary that:
- Verbally interprets the query result data
- References the relevant column meanings
- If there's an error message in the explanation, interpret what it means and provide troubleshooting advice
- If the query returned no results, explain what that likely means in business terms

Result Data (JSON):
{data}

Brief Explanation:
{explanation}

SQL Query:
{sql}

Respond with only the summary text (no markdown fences).
    """
)

def explain_query_response(json_input: str) -> str:
    try:
        logger.info("Starting query explanation process")
        parsed = json.loads(json_input)
        data_obj = parsed.get("data", [])
        explanation = parsed.get("explanation", "")
        sql = parsed.get("sql", "")
        
        logger.info(f"Input data for explanation has {len(data_obj)} rows")
        logger.info(f"Explanation: {explanation}")
        
        # Create a formatted column mapping string
        map_lines = [f"- {col} maps to '{key}'" for col, key in column_mapping.items()]
        column_map_str = "\n".join(map_lines)
        
        # Format the prompt with our data
        formatted = data_summary_prompt.format_messages(
            column_map=column_map_str,
            data=json.dumps(data_obj, indent=4),
            explanation=explanation,
            sql=sql
        )
        
        logger.info("Calling LLM for explanation generation")
        llm_response = llm.invoke(formatted).content.strip()
        logger.info(f"LLM response received: {llm_response[:100]}...")  # Log first 100 chars
        
        # Clean up markdown (just in case)
        llm_response = re.sub(r"^```[\s\S]*?\n", "", llm_response)
        llm_response = re.sub(r"\n```$", "", llm_response)
        
        output = {
            "data": data_obj,
            "summary": llm_response,
            "error": "error" in explanation.lower() or len(data_obj) == 0
        }
        logger.info("Query explanation completed successfully")
        return json.dumps(output, indent=4)
        
    except Exception as e:
        err_msg = str(e)
        logger.error(f"Error in explain_query_response: {err_msg}", exc_info=True)
        
        # Handle token size error (413) from Groq
        if "Request too large for model" in err_msg or "413" in err_msg:
            logger.warning("Token limit exceeded; returning fallback summary")
            return json.dumps({
                "data": parsed.get("data", []),
                "summary": None,
                "error": True
            }, indent=4)
        
        # General error fallback
        return json.dumps({
            "data": [],
            "summary": f"An error occurred while generating the explanation: {err_msg}",
            "error": True
        }, indent=4)

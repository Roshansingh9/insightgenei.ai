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
    Using the table `Motorcycle_sales` with the following columns:
    {columns}

    Convert the following natural language question into a valid PostgreSQL SQL query.
    Return ONLY the SQL query without ANY explanation or markdown formatting.
    Make sure the query syntax is 100% valid for PostgreSQL.
    DO NOT include <think> tags or any explanations of your thought process.
    ONLY return the SQL query text.

    Question: {input}
    """import os
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


# Sample data types and constraints for better schema understanding
column_details = {
    "state": "TEXT - Indian state names",
    "avg_daily_distance_km": "NUMERIC - Average daily distance traveled in kilometers",
    "brand": "TEXT - Motorcycle manufacturer (e.g., Honda, Bajaj, Hero)",
    "model": "TEXT - Specific motorcycle model name",
    "price_inr": "NUMERIC - Original purchase price in Indian Rupees",
    "year_of_manufacture": "INTEGER - Year when the motorcycle was manufactured (e.g., 2018, 2020)",
    "engine_capacity_cc": "INTEGER - Engine size in cubic centimeters (e.g., 100, 150, 350)",
    "fuel_type": "TEXT - Type of fuel (e.g., Petrol, Electric)",
    "mileage_kmpl": "NUMERIC - Fuel efficiency in kilometers per liter",
    "owner_type": "TEXT - Type of owner (e.g., First, Second, Third)",
    "registration_year": "INTEGER - Year when the motorcycle was registered",
    "insurance_status": "TEXT - Current insurance status (e.g., Active, Expired)",
    "seller_type": "TEXT - Type of seller (e.g., Individual, Dealer)",
    "resale_price_inr": "NUMERIC - Resale/second-hand value in Indian Rupees",
    "city_tier": "INTEGER - Classification of the city (1, 2, or 3, with 1 being metropolitan)"
}


# Create example data for the LLM to understand the data better
example_data = """
| state      | brand  | model      | price_inr | engine_capacity_cc | fuel_type | city_tier |
|------------|--------|------------|-----------|-------------------|-----------|-----------|
| Maharashtra| Honda  | Activa     | 75000     | 110               | Petrol    | 1         |
| Karnataka  | Bajaj  | Pulsar     | 120000    | 150               | Petrol    | 1         |
| Tamil Nadu | TVS    | Jupiter    | 70000     | 110               | Petrol    | 2         |
| Delhi      | Hero   | Splendor   | 65000     | 100               | Petrol    | 1         |
| Rajasthan  | Royal Enfield | Classic | 180000 | 350              | Petrol    | 2         |
"""


# Example queries and their corresponding SQL to guide the model
example_queries = """
Example 1:
Question: Find the average price of Honda motorcycles in Maharashtra
SQL: SELECT AVG(price_inr) FROM Motorcycle_sales WHERE brand = 'Honda' AND state = 'Maharashtra';

Example 2:
Question: List all motorcycles with engine capacity greater than 150cc ordered by price from highest to lowest
SQL: SELECT * FROM Motorcycle_sales WHERE engine_capacity_cc > 150 ORDER BY price_inr DESC;

Example 3:
Question: Calculate the average resale value as a percentage of original price grouped by brand
SQL: SELECT brand, AVG(resale_price_inr * 100.0 / price_inr) AS avg_resale_percentage FROM Motorcycle_sales GROUP BY brand ORDER BY avg_resale_percentage DESC;

Example 4:
Question: Find the most popular motorcycle model in each state based on count
SQL: SELECT state, model, COUNT(*) AS count FROM Motorcycle_sales GROUP BY state, model ORDER BY state, count DESC;

Example 5:
Question: Compare the average mileage between motorcycles manufactured before 2020 and those manufactured in or after 2020
SQL: 
SELECT 
    CASE WHEN year_of_manufacture < 2020 THEN 'Before 2020' ELSE '2020 and After' END AS manufacture_period,
    AVG(mileage_kmpl) AS avg_mileage
FROM Motorcycle_sales
GROUP BY manufacture_period
ORDER BY manufacture_period;
"""


# Improved prompt with clearer instructions and examples
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert PostgreSQL database administrator specializing in SQL query generation.
    
    # DATABASE SCHEMA
    Table name: Motorcycle_sales
    
    ## Columns with data types and descriptions:
    {column_details}
    
    ## Sample data to understand the content:
    {example_data}
    
    # TASK
    Convert the following natural language question into a precise, optimized PostgreSQL SQL query.
    
    # REQUIREMENTS
    - Your response must ONLY contain the SQL query without explanation, comments, or markdown formatting
    - Use proper PostgreSQL syntax, including correct functions and operators
    - Return comprehensive column selections when appropriate (avoid SELECT * except where truly needed)
    - Include appropriate aliasing for clarity in complex queries
    - Use appropriate JOIN operations where needed
    - Implement proper filtering with WHERE clauses
    - Use aggregate functions (AVG, COUNT, SUM, MIN, MAX) appropriately
    - Include GROUP BY, HAVING, ORDER BY clauses as needed
    - For complex queries, use CTEs (WITH clause) or subqueries for better readability
    - Handle potential NULL values properly
    - Implement window functions for advanced analytics when appropriate
    - Write queries that are performant and follow best practices

    # EXAMPLES OF QUESTIONS AND CORRESPONDING SQL QUERIES:
    {example_queries}
    
    # INSTRUCTIONS
    Answer with ONLY the SQL query. No explanations, no markdown, no code blocks, no preamble.
    
    # USER QUESTION
    {input}
    """
)


def extract_sql_query(response_text):
    # Remove SQL code blocks if present
    clean_text = re.sub(r'```sql|```', '', response_text, flags=re.IGNORECASE)
    
    # Remove any remaining explanations or thoughts
    clean_text = re.sub(r'<think>.*?</think>', '', clean_text, flags=re.DOTALL)
    
    # Remove any other markdown formatting that might be present
    clean_text = re.sub(r'^SELECT', 'SELECT', clean_text, flags=re.MULTILINE)
    
    # Remove any prefixes like "SQL:" or "Query:"
    clean_text = re.sub(r'^(SQL:|Query:)\s*', '', clean_text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    clean_text = clean_text.strip()
    
    return clean_text


def generate_sql(user_input):
    # Prepare column details string
    column_detail_str = "\n".join([f"- {col}: {desc}" for col, desc in column_details.items()])
    
    # Format the prompt with all the details
    formatted_prompt = prompt.format_messages(
        column_details=column_detail_str,
        example_data=example_data,
        example_queries=example_queries,
        input=user_input
    )
    
    # Call the LLM
    response = llm.invoke(formatted_prompt)
    raw_response = response.content.strip()
    
    # For debugging
    print("Raw LLM Response:", raw_response)
    
    # Extract the actual SQL query
    sql_query = extract_sql_query(raw_response)
    
    return sql_query


def generate_query(user_input):
    sql_query = generate_sql(user_input)
    
    # Return the result
    response_json = {
        "detail": "Query generated successfully",
        "sql_query": sql_query
    }
    return json.dumps(response_json, indent=4)


# Example usage
if __name__ == "__main__":
    # Test with a complex query
    user_query = "What's the average resale price difference between first and second owners for motorcycles with engine capacity over 150cc, grouped by brand, and only include brands with at least 5 motorcycles?"
    result = generate_query(user_query)
    print(result)
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
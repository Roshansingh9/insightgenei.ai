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
    model_name="deepseek-r1-distill-llama-70b",
    temperature=0.0  # Set temperature to 0 for more deterministic outputs
)


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
SQL: SELECT CASE WHEN year_of_manufacture < 2020 THEN 'Before 2020' ELSE '2020 and After' END AS manufacture_period, AVG(mileage_kmpl) AS avg_mileage FROM Motorcycle_sales GROUP BY manufacture_period ORDER BY manufacture_period;
"""


# Completely revamped prompt with extremely strict instructions
prompt = ChatPromptTemplate.from_template(
    """
    You will generate ONLY a PostgreSQL SQL query based on the natural language question below.
    
    Table name: Motorcycle_sales
    Columns: {column_details}
    
    EXTREMELY IMPORTANT INSTRUCTIONS:
    1. Your ENTIRE response must be ONLY the SQL query - nothing else
    2. Do NOT include any explanations before or after the query
    3. Do NOT use <think> tags, internal monologue, or explain your reasoning AT ALL
    4. Do NOT include markdown code blocks (```sql```)
    5. Start your response with SELECT, WITH, or other SQL keyword
    6. End your query with a semicolon
    7. Include necessary WHERE, GROUP BY, HAVING, ORDER BY clauses as needed
    8. Your response should be PURE SQL ONLY with no commentary
    
    Examples of correct responses:
    {example_queries}
    
    Converting this question to SQL ONLY:
    {input}
    """
)


def extract_sql_query(response_text):
    """
    Extract only the SQL query from the LLM response.
    This function is significantly improved to handle cases where the LLM provides
    thinking or explanations along with the SQL query.
    """
    # First, try to remove any think tags and their content
    clean_text = re.sub(r'<think>[\s\S]*?</think>', '', response_text, re.DOTALL)
    
    # Also look for incomplete think tags or other reasoning blocks
    clean_text = re.sub(r'Alternatively,.*?\.', '', clean_text, re.DOTALL)
    clean_text = re.sub(r'Yes, because.*?\.', '', clean_text, re.DOTALL)
    clean_text = re.sub(r'So, the query should be.*?\.', '', clean_text, re.DOTALL)
    
    # Remove code block formatting
    clean_text = re.sub(r'```sql|```', '', clean_text, re.IGNORECASE)
    
    # Find SQL query pattern - most SQL queries start with SELECT, WITH, etc.
    # and typically end with a semicolon
    sql_pattern = r'((?:SELECT|WITH|CREATE|INSERT|UPDATE|DELETE|ALTER)[\s\S]*?;)'
    matches = re.findall(sql_pattern, clean_text, re.IGNORECASE)
    
    if matches:
        # Return the last complete SQL statement
        return matches[-1].strip()
    
    # If no complete SQL found, look for partial SQL
    partial_sql_pattern = r'((?:SELECT|WITH)[\s\S]*)'
    partial_matches = re.findall(partial_sql_pattern, clean_text, re.IGNORECASE)
    
    if partial_matches:
        sql = partial_matches[-1].strip()
        # Add semicolon if missing
        if not sql.endswith(';'):
            sql += ';'
        return sql
    
    # Last resort: if the text contains SELECT or similar keywords, 
    # try to extract everything from there to the end
    for keyword in ['SELECT', 'WITH', 'CREATE', 'INSERT', 'UPDATE', 'DELETE', 'ALTER']:
        if keyword in clean_text:
            parts = clean_text.split(keyword, 1)
            if len(parts) > 1:
                sql = keyword + parts[1].strip()
                if not sql.endswith(';'):
                    sql += ';'
                return sql
    
    # If all else fails, just return the cleaned text
    return clean_text.strip()


def generate_sql(user_input):
    # Prepare column details string
    column_detail_str = "\n".join([f"- {col}: {desc}" for col, desc in column_details.items()])
    
    # Format the prompt with all the details
    formatted_prompt = prompt.format_messages(
        column_details=column_detail_str,
        example_queries=example_queries,
        input=user_input
    )
    
    # Call the LLM
    response = llm.invoke(formatted_prompt)
    raw_response = response.content.strip()
    
    # Debug prints should be commented out in production
    # print("Raw LLM Response:", raw_response)
    
    # Extract the actual SQL query
    sql_query = extract_sql_query(raw_response)
    
    # Ensure the query ends with a semicolon
    if not sql_query.endswith(';'):
        sql_query = sql_query.rstrip() + ';'
    
    return sql_query


def post_process_sql_query(sql_query):
    """
    Additional post-processing to clean up any remaining non-SQL content
    """
    # Remove any obvious non-SQL content
    non_sql_patterns = [
        r'I should.*?\.', 
        r'Finally,.*?\.', 
        r'This query.*?\.', 
        r'Let me.*?\.', 
        r'Now.*?\.', 
        r'Here\'s.*?:',
        r'Alternatively,.*?\.',
        r'Yes, because.*?\.',
        r'So, the query should be.*?\.',
        r'.*\n</think>\n',  # Handle incomplete think tags
        r'</?think>'  # Remove any remaining think tags without content
    ]
    
    clean_query = sql_query
    for pattern in non_sql_patterns:
        clean_query = re.sub(pattern, '', clean_query, flags=re.IGNORECASE | re.DOTALL)
    
    # If we have a semicolon in the middle, keep only up to the first semicolon
    if ';' in clean_query:
        parts = clean_query.split(';')
        clean_query = parts[0] + ';'
    
    # Final cleanup of any whitespace issues
    clean_query = clean_query.strip()
    
    return clean_query


def generate_query(user_input):
    sql_query = generate_sql(user_input)
    
    # Additional post-processing
    sql_query = post_process_sql_query(sql_query)
    
    # Return the result
    response_json = {
        "detail": "Query generated successfully",
        "sql_query": sql_query
    }
    return json.dumps(response_json, indent=4)



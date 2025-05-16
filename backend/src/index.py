import json
import logging
from src.utils.language import detect_language, translate_language
from src.utils.generate_query import generate_query 
from src.utils.execute_query import execute_sql_query  
from src.utils.explain_query_result import explain_query_response  

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def result(text):
    try:
        # Detect language of the input text
        logger.info(f"Processing input text: {text}")
        lang = detect_language(text)
        logger.info(f"Detected language: {lang.name}")

        # Translate to English if necessary
        if lang.name.lower() != "english":
            logger.info(f"Translating from {lang.name} to English")
            eng_text = translate_language(text, "english")
            input_text = eng_text.translated
            logger.info(f"Translated text: {input_text}")
        else:
            input_text = text

        # Generate SQL query from natural language
        logger.info("Generating SQL query...")
        query_json_str = generate_query(input_text)
        query_data = json.loads(query_json_str)
        
        # Extract the SQL query from the response
        if "sql_query" in query_data:
            sql_query = query_data["sql_query"]
        else:
            logger.error("No SQL query found in generate_query response")
            raise ValueError("Failed to generate SQL query: No query in response")
        
        logger.info(f"Generated SQL Query: {sql_query}")

        # Execute the SQL query
        logger.info("Executing SQL query...")
        query_result_json = execute_sql_query(sql_query)
        logger.info(f"Query execution result: {query_result_json[:100]}...")  # Log first 100 chars
        
        # Check if there was an error in query execution
        query_result = json.loads(query_result_json)
        if "explanation" in query_result and query_result["explanation"].startswith("Error"):
            logger.warning(f"Query execution encountered an error: {query_result['explanation']}")

        # Generate explanation of results
        logger.info("Generating explanation of results...")
        summary_json = explain_query_response(query_result_json)
        logger.info("Processing complete")

        return json.loads(summary_json)
    
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        error_response = {
            "data": [],
            "summary": f"An error occurred: {str(e)}",
            "error": True
        }
        return error_response
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        error_response = {
            "data": [],
            "summary": f"An error occurred: {str(e)}",
            "error": True
        }
        return error_response
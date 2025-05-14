import json
from src.utils.language import detect_language, translate_language
from src.utils.generate_query import generate_query 
from src.utils.execute_query import execute_sql_query  
from src.utils.explain_query_result import explain_query_response  

def result(text):
    try:
        # Detect language of the input text
        lang = detect_language(text)

        # Translate to English if necessary
        if lang.name.lower() != "english":
            eng_text = translate_language(text, "english")
            input_text = eng_text.translated
        else:
            input_text = text

        # Generate SQL query from natural language
        query_json_str = generate_query(input_text)        
        query_data = json.loads(query_json_str)            
        sql_query = query_data["sql_query"]
        
        print("Generated SQL Query:", sql_query)

        # Execute the SQL query
        query_result_json = execute_sql_query(sql_query)  

        # Generate explanation of results
        summary_json = explain_query_response(query_result_json)

        return json.loads(summary_json)
    except Exception as e:
        
        error_response = {
            "data": [],
            "summary": f"An error occurred: {str(e)}",
            "error": True
        }
        return error_response
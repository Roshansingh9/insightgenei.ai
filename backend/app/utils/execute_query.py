import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from urllib.parse import urlparse
import json


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def parse_database_url(url):
    result = urlparse(url)
    return {
        "host": result.hostname,
        "port": result.port,
        "dbname": result.path[1:],  
        "user": result.username,
        "password": result.password
    }


def execute_sql_query(query):
    response = {"sql": query, "data": None, "explanation": None}
    try:
        
        db_params = parse_database_url(DATABASE_URL)

       
        conn = psycopg2.connect(
            host=db_params["host"],
            port=db_params["port"],
            dbname=db_params["dbname"],
            user=db_params["user"],
            password=db_params["password"]
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

      
        cursor.execute(query)

        
        rows = cursor.fetchall()
        columns = [desc.name for desc in cursor.description]

      
        data = [dict(row) for row in rows]
        response["data"] = data

        
        row_count = len(data)
        if row_count == 0:
            explanation = "The query returned no results."
        else:
            explanation = (
                f"The query returned {row_count} row" + ("s" if row_count > 1 else "") + 
                f". Columns returned: {', '.join(columns)}."
            )
        response["explanation"] = explanation

       
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        response["explanation"] = f"Error executing query: {str(e)}"
        response["data"] = []

    return json.dumps(response, default=str)

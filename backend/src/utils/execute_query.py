import os
import json
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def parse_database_url(url):
    """Parse PostgreSQL database URL into connection parameters"""
    if not url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    result = urlparse(url)
    return {
        "host": result.hostname,
        "port": result.port,
        "dbname": result.path[1:],  
        "user": result.username,
        "password": result.password
    }

def execute_sql_query(query):
    """Execute a SQL query and return the results as JSON"""
    response = {"sql": query, "data": None, "explanation": None}
    conn = None
    
    try:
        # Parse the database URL
        db_params = parse_database_url(DATABASE_URL)
        
        logger.info(f"Connecting to database at {db_params['host']}:{db_params['port']}/{db_params['dbname']}")
        
        # Connect to the database with timeout parameters
        conn = psycopg2.connect(
            host=db_params["host"],
            port=db_params["port"],
            dbname=db_params["dbname"],
            user=db_params["user"],
            password=db_params["password"],
            connect_timeout=10  # Add a connection timeout
        )
        
        # Set a statement timeout to prevent long-running queries
        conn.set_session(autocommit=False)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SET statement_timeout = '30s';")  # 30 second timeout for statements
        
        logger.info(f"Executing query: {query}")
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch results
        rows = cursor.fetchall()
        if cursor.description:  # Check if there are columns in the result
            columns = [desc.name for desc in cursor.description]
            # Convert to list of dictionaries
            data = [dict(row) for row in rows]
            response["data"] = data
            
            # Generate simple explanation
            row_count = len(data)
            if row_count == 0:
                explanation = "The query returned no results."
            else:
                explanation = (
                    f"The query returned {row_count} row" + ("s" if row_count > 1 else "") + 
                    f". Columns returned: {', '.join(columns)}."
                )
            response["explanation"] = explanation
            logger.info(f"Query returned {row_count} rows with columns: {', '.join(columns)}")
        else:
            # For queries that don't return data (like INSERT, UPDATE)
            response["data"] = []
            affected_rows = cursor.rowcount
            response["explanation"] = f"Query executed successfully. {affected_rows} rows affected."
            logger.info(f"Query executed successfully. {affected_rows} rows affected.")
        
        # Clean up
        conn.commit()
        cursor.close()
        
    except psycopg2.OperationalError as e:
        error_msg = f"Database connection error: {str(e)}"
        logger.error(error_msg)
        response["explanation"] = error_msg
        response["data"] = []
        
    except psycopg2.Error as e:
        error_msg = f"Database error: {str(e)}"
        logger.error(error_msg)
        response["explanation"] = error_msg
        response["data"] = []
        
    except Exception as e:
        error_msg = f"Error executing query: {str(e)}"
        logger.error(error_msg)
        response["explanation"] = error_msg
        response["data"] = []
        
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed")
            
    return json.dumps(response, default=str)
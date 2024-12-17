from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

# Flask Class instance
app = Flask(__name__)
CORS(app) # delete if broken 

# Fields will be empty for public repo.
DB_HOST = ''  
DB_NAME = ''                    
DB_USER = ''                
DB_PASSWORD = ''           

@app.route('/')
def root():
    return "In root node"


@app.route('/advertising', methods=['GET'])
def advertising():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM advertising;")  # Execute SQL code 
        results = cursor.fetchall()
        
        # Get column names to create a dictionary for each row
        column_names = [desc[0] for desc in cursor.description]
        
        # Format the results as a list of dictionaries
        data = []
        for row in results:
            data.append(dict(zip(column_names, row)))
        
        # Close cursor, connection
        cursor.close()
        connection.close()
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({"error": f"Error connecting to the database: {str(e)}"})




@app.route('/advertising', methods=['POST'])
def add_advertising():
    try:
        # Get the JSON data from the request body
        data = request.get_json()

        # Extract values
        tv = data.get('TV')
        radio = data.get('Radio')
        newspaper = data.get('Newspaper')
        sales = data.get('Sales')

        # Quick input check 
        if None in [tv, radio, newspaper, sales]:
            return jsonify({"error": "Missing values for one or more fields"}), 400

        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Insert procedure 
        insert_query = """
        INSERT INTO advertising (TV, Radio, Newspaper, Sales)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (tv, radio, newspaper, sales))  

        # Commit changed
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Success Indicator 
        return jsonify({"message": "New entry added successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Error inserting data: {str(e)}"}), 400


@app.route('/advertising/<int:id>', methods=['DELETE'])
def delete_advertising(id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        # Prepare the DELETE query
        cursor.execute("DELETE FROM advertising WHERE id = %s;", (id,))

        # Commit the transaction
        connection.commit()

        # verify procedure validity
        if cursor.rowcount > 0:
            message = f"Entry with ID {id} has been deleted successfully."
        else:
            message = f"No entry found with ID {id}."

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify({"message": message})

    except Exception as e:
        # Handle any errors that occur
        return jsonify({"error": f"Error deleting data: {str(e)}"})


# Driver class 
if __name__ == '__main__':
    app.run(debug=True)
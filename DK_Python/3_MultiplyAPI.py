from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/multiply', methods=['GET', 'POST'])
def multiply():
    try:
        if request.method == 'GET':
            # Get query parameters
            num1 = request.args.get('num1', type=int)
            num2 = request.args.get('num2', type=int)
        else:
            # Get JSON data
            data = request.get_json()
            if not data or 'num1' not in data or 'num2' not in data:
                return jsonify({'error': 'Please provide num1 and num2 in JSON body'}), 400
            num1 = data['num1']
            num2 = data['num2']

        # Validate input
        if num1 is None or num2 is None:
            return jsonify({'error': 'Please provide two valid integers'}), 400

        # Perform multiplication
        result = num1 * num2
        return jsonify({'num1': num1, 'num2': num2, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'GET':
            # Get query parameters
            num1 = request.args.get('num1', type=int)
            num2 = request.args.get('num2', type=int)
        else:
            # Get JSON data
            data = request.get_json()
            if not data or 'num1' not in data or 'num2' not in data:
                return jsonify({'error': 'Please provide num1 and num2 in JSON body'}), 400
            num1 = data['num1']
            num2 = data['num2']
        
        # Validate input
        if num1 is None or num2 is None:
            return jsonify({'error': 'Please provide two valid integers'}), 400
        
        # Perform addition
        result = num1 + num2
        return jsonify({'num1': num1, 'num2': num2, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subtract', methods=['GET', 'POST'])
def subtract():
    try:
        if request.method == 'GET':
            # Get query parameters
            num1 = request.args.get('num1', type=int)
            num2 = request.args.get('num2', type=int)
        else:
            # Get JSON data
            data = request.get_json()
            if not data or 'num1' not in data or 'num2' not in data:
                return jsonify({'error': 'Please provide num1 and num2 in JSON body'}), 400
            num1 = data['num1']
            num2 = data['num2']
        
        # Validate input
        if num1 is None or num2 is None:
            return jsonify({'error': 'Please provide two valid integers'}), 400
        
        # Perform subtraction
        result = num1 - num2
        return jsonify({'num1': num1, 'num2': num2, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

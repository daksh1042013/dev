from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/multiply', methods=['GET'])
def multiply():
    try:
        # Get query parameters
        num1 = request.args.get('num1', type=int)
        num2 = request.args.get('num2', type=int)

        # Validate input
        if num1 is None or num2 is None:
            return jsonify({'error': 'Please provide two valid integers'}), 400

        # Perform multiplication
        result = num1 * num2
        return jsonify({'num1': num1, 'num2': num2, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

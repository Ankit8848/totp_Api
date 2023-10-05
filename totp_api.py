from flask import Flask, request, jsonify
import pyotp
import os

app = Flask(__name__)

# Secret key for generating TOTP (you should store this securely)
SECRET_KEY = 'your_secret_key_here'


@app.route('/generate_totp', methods=['POST'])
def generate_totp():
    try:
        # Get the user's ID from the request JSON data
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({'error': 'Missing user_id in request JSON'}), 400

        # Create a TOTP instance with the user's ID and secret key
        totp = pyotp.TOTP(SECRET_KEY + user_id)

        # Generate a TOTP token
        token = totp.now()

        # Prepare the response JSON object
        response_data = {
            'user_id': user_id,
            'totp_token': token
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/validate_totp', methods=['POST'])
def validate_totp():
    try:
        # Get the user's ID and TOTP token from the request JSON data
        data = request.get_json()
        user_id = data.get('user_id')
        totp_token = data.get('totp_token')

        if not user_id or not totp_token:
            return jsonify({'error': 'Missing user_id or totp_token in request JSON'}), 400

        # Create a TOTP instance with the user's ID and secret key
        totp = pyotp.TOTP(SECRET_KEY + user_id)

        # Verify the TOTP token
        is_valid = totp.verify(totp_token)

        # Prepare the response JSON object
        response_data = {
            'user_id': user_id,
            'is_valid': is_valid
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=True)

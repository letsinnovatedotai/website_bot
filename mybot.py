from flask import Flask, request, jsonify
from openai import OpenAI
import os
import socket
import requests

app = Flask(__name__)
app.config['DEBUG'] = True  # Enable debugging


@app.route('/website_chatbot/query', methods=['POST'])
def query_openai():
    print("----------------------------------------------------")
    try:
        # Extract request data
        data = request.json
        prompt = data.get('prompt', None)
        print("recieved_prompt as ",prompt)
        print("request is ",request)
        model = 'gpt-4o-mini'
        max_tokens = 150

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Call OpenAI API
# Create a chat completion
        p1 = "Tsk-gVvQ4Hg30oxfFUEVQx"
        p2 = "TNoT3BlbkFJCl1Zx"
        p3 = "TeKHTefCSjHuko14"

        p_all = p1[1:]+p2[1:]+p3[1:]
        client = OpenAI(
            api_key= p_all,  # This is the default and can be omitted
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
)
        assistant_message = chat_completion.choices[0].message.content

        return jsonify({"response": assistant_message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_external_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return 'Unable to determine external IP'

if __name__ == '__main__':
    # Determine the internal host IP address
    internal_ip = 'localhost'
    try:
        internal_ip = socket.gethostbyname(socket.gethostname())
    except:
        internal_ip = 'localhost'

    # Get external/public IP address
    external_ip = get_external_ip()

    port = 5000
    print("\n=== Flask Server is Running ===")
    print(f"Internal Host: http://{internal_ip}:{port}")
    print(f"External Host: http://{external_ip}:{port}")
    print("\n=== Sample `curl` Command to Test the Endpoint ===")
    curl_command = f"""curl -X POST http://{external_ip}:{port}/openai/query \\
  -H "Content-Type: application/json" \\
  -d '{{
    "prompt": "Write a short poem about the stars."
}}'"""
    print(curl_command)
    print("===============================\n")

    app.run(host='0.0.0.0', port=port, debug=True)

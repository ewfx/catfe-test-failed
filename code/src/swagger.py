import os
import requests
import yaml
from groq import Groq


def generate_bdd_swagger(url):
    response = requests.get(url)
    response.raise_for_status()
    swagger_data = yaml.dump(response.json())
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)
    prompt = f"""
    Using the following Swagger API definition, generate BDD test scenarios using the Gherkin syntax:
    {swagger_data}
    """

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        print("Generated BDD Test Cases:")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")

#swagger_url = "http://localhost:8080/v3/api-docs"
#generate_bdd_swagger(swagger_url)
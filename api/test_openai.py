from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads .env file from current directory

client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="Say hello in French"
)

print(response.output_text)

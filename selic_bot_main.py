import os
from dotenv import load_dotenv
import requests
from ai_flow.selic_bot_agent import SelicAgent

if __name__ == "__main__":
    load_dotenv()
    agent = SelicAgent(api_key=os.getenv("OPEN_AI_KEY"))
    comment = agent.generate()
    

    if comment:
        try:
            r = requests.post("http://localhost:8888/mensagem", json={f"text": comment}, timeout=30)
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Other request exception occurred: {req_err}")

        print("\nGenerated comment about the Selic trend:\n")
        print(comment)
        
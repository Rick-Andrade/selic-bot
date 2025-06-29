import os
from dotenv import load_dotenv
from ai_flow.selic_bot_agent import SelicAgent

if __name__ == "__main__":
    load_dotenv()
    agent = SelicAgent(api_key=os.getenv("OPEN_AI_KEY"))
    comment = agent.generate()

    print("\n📊 Generated comment about the Selic trend:\n")
    print(comment)
    
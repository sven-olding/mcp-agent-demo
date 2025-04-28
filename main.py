from dotenv import load_dotenv
import os
from agents import Agent, Runner

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
print(f"Using model: {MODEL}")


def main():
    agent = Agent(
        name="Assistant", instructions="You are a helpful assistant", model=MODEL
    )

    result = Runner.run_sync(agent, "Write a haiku about recursion in programming")

    print(result.final_output)


if __name__ == "__main__":
    main()

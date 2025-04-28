import os
import asyncio
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant and you can use some tools provided via model context protocol",
        model=MODEL,
        mcp_servers=[mcp_server],
    )

    while True:
        message = input("You:\n")
        if message != "":
            try:
                result = await Runner.run(starting_agent=agent, input=message)
                print(
                    f"""
                      Assistant:\n
                      {result.final_output}
                      """
                )
            except Exception as e:
                print(f"Error: {e}")


async def main():
    async with MCPServerSse(
        name="MongoDB Demo MCP Server",
        params={"url": MCP_SERVER_URL},
        cache_tools_list=True,
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MongoDB SSE Example", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n"
            )
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())

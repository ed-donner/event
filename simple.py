import asyncio
import os
from agents import Agent, Runner, SQLiteSession
from agents.mcp import MCPServerStreamableHttp


MODEL = "gpt-5-nano"
PARAMS = {"url": os.getenv("ALLIANCE_MCP_SERVER"), "timeout": 30}

INSTRUCTIONS = "Play the Alliance game. Use your tools to check status, send messages, and choose who to support."
REGISTER = "Come up with a random player name and register as that player"


async def main():
    session = SQLiteSession("Simple")
    async with MCPServerStreamableHttp(params=PARAMS) as mcp:
        agent = Agent(name="Simple", instructions=INSTRUCTIONS, model=MODEL, mcp_servers=[mcp])
        await Runner.run(agent, REGISTER, session=session)
        print("Registered")
        while True:
            print("=== TURN ===")
            await Runner.run(agent, "Check status and take action", session=session)
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())

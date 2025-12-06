from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv()


llm = ChatOpenAI()

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["/Users/theesh/Desktop/AI/mcp-adaptors/servers/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            # Make sure you start your weather server on port 8000
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        }
    }
)


async def main():
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})

    print(math_response["messages"])
    print(weather_response["messages"])

    # async with client.session("math") as session:
    #     tools = await load_mcp_tools(session)
    #     print(tools)

    # async with client.session("weather") as session:
    #     weather_tools = await load_mcp_tools(session)
    #     print(weather_tools)


if __name__ == "__main__":
    asyncio.run(main())

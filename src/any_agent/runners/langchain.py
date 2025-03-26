from loguru import logger


@logger.catch(reraise=True)
def run_langchain_agent(agent, query):
    inputs = {"messages": [("user", query)]}
    for s in agent.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:   
            message.pretty_print()
    return message
from anthropic import Anthropic
# from anthropic.ext.agents import Agent

# client = Anthropic()

# # Create an agent
# agent = Agent(
#     client=client,
#     model="claude-opus-5"
# )

# # Run the agent
# result = agent.run("What is the capital of France?")
# print(result)

client = Anthropic()
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": "My name is Kushi?"},
    ]
)
print(response.content)

# response2 = client.messages.create(
#     model="claude-haiku-4-5",
#     max_tokens=2048,
#     messages=[
#         {"role": "user", "content": "What is my name?"},
#     ]
# )   
# print(response2.content)



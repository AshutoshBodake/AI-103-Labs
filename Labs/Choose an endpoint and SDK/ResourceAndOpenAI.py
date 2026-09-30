from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from openai import OpenAI

project_endpoint = "https://az-103-189-resource.services.ai.azure.com/api/projects/az-103-189"

project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)

project_openai_client  = project_client.get_openai_client()


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://ai.azure.com/.default"
)

openai_client = OpenAI(  
  base_url = "https://az-103-189-resource.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# Your model deployment name
model_name = "gpt-5.4-mini"

# Generate a response using the OpenAI-compatible client
response = openai_client.responses.create(
    model=model_name,  
    input="What is Microsoft Foundry?"
)

# Display the response
print(response.output_text)

response = openai_client.responses.create(
    model = model_name,
    input = "Explain machine learning in simple terms."
)

print(f"Response: {response.output_text}")
print(f"Response ID: {response.id}")
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Status: {response.status}")

response = response = openai_client.responses.create(
    model=model_name,
    instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
    input="Explain neural networks."
)

print(response.output_text)

# ---------------------------------------------------------
# Temperature and maximum output tokens
# ---------------------------------------------------------

response = openai_client.responses.create(
    model=model_name,
    instructions=(
        "You are a helpful AI assistant that answers questions clearly and concisely."
    ),
    input="Write a creative story about AI.",
    temperature=0.8,  # Higher temperature for more creativity
    max_output_tokens=1200  # Limit response length
)

print(response.output_text)

# ---------------------------------------------------------
# Using a Foundry direct model
# ---------------------------------------------------------

response = openai_client.responses.create(
    model="microsoft-phi-4",  # Example Foundry direct model
    instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
    input="What are the benefits of small language models?"
)

print(response.output_text)

# First turn in the conversation
response1 = openai_client.responses.create(
    model=model_name,
    instructions="You are a helpful AI assistant that explains technology concepts clearly.",
    input="What is machine learning?"
)

print("Assistant:", response1.output_text)

# Continue the conversation
response2 = openai_client.responses.create(
    model=model_name,
    instructions="You are a helpful AI assistant that explains technology concepts clearly.",
    input="Can you give me an example?",
    previous_response_id=response1.id
)

print("Assistant:", response2.output_text)

# Track responses
last_response_id = None
model_name = model_name;
# Loop until the user wants to quit
print("Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input('\nYou: ')
    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break

    # Get a response
    response = openai_client.responses.create(
                model=model_name,
                instructions="You are a helpful AI assistant that explains technology concepts clearly.",
                input=input_text,
                previous_response_id=last_response_id
    )
    assistant_text = response.output_text
    print("\nAssistant:", assistant_text)
    last_response_id = response.id


completion = openai_client.chat.completions.create(
    model=model_name,  # Your model deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "When was Microsoft founded?"}
    ]
)

print(completion.choices[0].message.content)

# Retaining conversational context
# Initial messages
conversation_messages=[
    {
        "role": "system",
        "content": "You are a helpful AI assistant that answers questions and provides information."
    }
]

# Add the first user message
conversation_messages.append(
    {"role": "user",
    "content": "When was Microsoft founded?"}
)

# Get a completion
completion = openai_client.chat.completions.create(
    model=model_name,
    messages=conversation_messages
)
assistant_message = completion.choices[0].message.content
print("Assistant:", assistant_text)

# Append the response to the conversation
conversation_messages.append(
    {"role": "assistant", "content": assistant_text}
)

# Add the next user message
conversation_messages.append(
    {"role": "user",
    "content": "Who founded it?"}
)

# Get a completion
completion = openai_client.chat.completions.create(
    model=model_name,
    messages=conversation_messages
)
assistant_message = completion.choices[0].message.content
print("Assistant:", assistant_text)

# and so on...

# In a real application, the conversation is likely to be implemented in a loop; like this:

# Initial messages
conversation_messages=[
    {
        "role": "system",
        "content": "You are a helpful AI assistant that answers questions and provides information."
    }
]

# Loop until the user wants to quit
print("Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input('\nYou: ')
    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break

    # Add the user message
    conversation_messages.append(
        {"role": "user",
        "content": input_text}
    )

    # Get a completion
    completion = openai_client.chat.completions.create(
        model=model_name,
        messages=conversation_messages
    )
    assistant_message = completion.choices[0].message.content
    print("\nAssistant:", assistant_message)

    # Append the response to the conversation
    conversation_messages.append(
        {"role": "assistant", "content": assistant_message}
    )
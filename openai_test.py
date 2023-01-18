import openai
import local_settings


# Set your API key
openai.api_key = local_settings.OPEAAI_API_KEY
# Use the GPT-3 model
completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt="我该如何使用python写一个telegram机器人？",
    max_tokens=1024,
    temperature=0.5
)
# Print the generated text
print(completion.choices[0].text)


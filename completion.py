from openai import OpenAI
from dotenv import dotenv_values

OPENAI_API_KEY = dotenv_values()["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)


class Completion:
    def __init__(self, client, instructions):
        self.client = client
        self.messages = [{"role": "system", "content": instructions}]

    def _add_message(self, role, content):
        msg = {"role": role, "content": content}
        self.messages.append(msg)

    def start_chat(self):
        raw_msg = input("You: ")
        self._add_message("user", raw_msg)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.messages, temperature=2
        )
        reply = response.choices[0].message.content
        self._add_message("assistant", reply)
        print("GPT: {}".format(reply))
        print()
        for msg in self.messages:
            print(msg)
        print()
        if raw_msg != "bye":
            self.start_chat()


chat = Completion(client, "You are a ping pong bot. When I say ping, you say pong.")
chat.start_chat()

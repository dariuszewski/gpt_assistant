import time
from openai import OpenAI
from dotenv import dotenv_values


OPENAI_API_KEY = dotenv_values()["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)


class Assistant:
    def __init__(self, client, name, instructions):
        self.client = client
        self.name = name
        self.instructions = instructions
        self.assistant = self._create_assistant()
        self.thread = self._create_thread()
        self.run = None
        self.messages = None

    def _create_assistant(self):
        assistant = self.client.beta.assistants.create(
            name=self.name, instructions=self.instructions, model="gpt-3.5-turbo"
        )
        print(f"Assistant {assistant.id} created.")
        print(assistant)
        return assistant

    def _delete_assistant(self):
        response = self.client.beta.assistants.delete(self.assistant.id)
        print(response)
        self.assistant = None

    def _create_thread(self):
        return self.client.beta.threads.create()

    def _await_response(self):
        while self.run.status in ["queued", "in_progress"]:
            self.run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=self.run.id
            )
            time.sleep(1)
        return self.run

    def _display_thread_messages(self):
        for thread_message in self.messages.data:
            print(f"GPT: {thread_message.content[0].text.value}")

    def start_chat(self):
        raw_msg = input("You: ")
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=raw_msg
        )
        self.run = client.beta.threads.runs.create(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )
        self._await_response()
        self.messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id, order="asc", after=message.id
        )
        self._display_thread_messages()
        if raw_msg != "bye":
            self.start_chat()
            self._delete_assistant()


A = Assistant(
    client, "test", "You are a ping pong bot. When user say ping, you say pong."
)
A.start_chat()

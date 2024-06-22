# GPT ASSISTANT

## Components

### Assistants

- Chosen LLM
- Has access to tools: files, code interpreter

```python3
>>> assistant = client.beta.assistants.create(
        name="Name of the assistant",
        instructions="Purpose of the assistant",
        tools=[{"type": "tool-type"}],
        model="model-name"
    )
>>> assistant.id
'asst_dasdaf123das'
```

### Threads

- List of messages from a user and the assistant.
- NOT linked to an assistant

```python3
>>> thread = client.beta.threads.create()
>>> thread.id
'thread_dasdaf123das'
```

### Messages

- Stored in a thread
- Latest message has index [0]

```python3
>>> message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Message content"
)
```

### Runs

- Allow to call a thread
- Stores Run Steps: [sending messages, getting replies, running code, reading files etc.]

```python3
>>> message = client.beta.threads.run.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
>>> run.status
queued
```

- Runs don't get executed immedietly

```
>>> run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)
>>> run.status
completed
```

### Retreiving messages

```
>>> messages = client.beta.threads.messages.list(thread_id=thread.id)
>>> messages
SyncCursorPage...
>>> messages.data[0].content[0].text.value
'Most recent message value'
```

### Retreiving run steps

```
>>> steps = client.beta.threads.runs.steps.list(
    thread_id=thread.id,
)
>>> steps
SyncCursorPage[iterable]
```

## Assistant Workflow

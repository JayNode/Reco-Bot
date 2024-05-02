from openai import OpenAI

def aimodel(userGames):

  client = OpenAI()

  assistant = client.beta.assistants.create(
    name="Video Game Recommendation Analyzer",
    instructions="_EMPTY_",
    model="gpt-3.5-turbo",
    tools=[{"type": "code_interpreter"}]
  )

  thread = client.beta.threads.create()

  # list of user games sent to content
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=(userGames)
  )

  # instruction for finding most common genre from list of games
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Based on the most common genre of the list, name a game that is not in the list"
  )

  while run.status != "completed":
      running = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
      )

      if running.status == "completed":
          break       

  all_messages = client.beta.threads.messages.list(
      thread_id=thread.id
  )

  print("----------------------------------------------------------------")
  # list of games
  print(f"User games: {message.content[0].text.value}")

  print("----------------------------------------------------------------")
  # results from chatgpt ai
  VGRB = all_messages.data[0].content[0].text.value
  print(f"VGRB: {VGRB}")

  return VGRB
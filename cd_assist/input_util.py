def should_exit(user_input):
    return user_input.lower() in {"exit", "quit", "bye"}

def should_explain(user_input):
    return user_input.lower() == "explain" or user_input.lower().startswith("explain ")

def should_ask(user_input):
    return user_input.lower() == "ask" or user_input.lower().startswith("ask ")

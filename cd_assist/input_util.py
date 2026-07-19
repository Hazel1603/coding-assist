def should_exit(user_input):
    return user_input.lower() in {"exit", "quit", "bye"}

def should_explain(user_input):
    return user_input.lower().startswith("explain ")

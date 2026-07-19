import argparse

from cd_assist.client import init_openai_client
from cd_assist.agent import ModelResponseError, init_agent
from cd_assist.tools import FileParseError, search_files
from cd_assist.context import build_working_context
from cd_assist.print import *
from cd_assist.input_util import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    return parser.parse_args()

def handle_explain_command(user_input, agent):
    # validate arguments
    parts = user_input.split(" ", 1)
    if len(parts) < 2:
        print_no_file()
        return
    requested_path = parts[1]

    # call agent
    try:
        response = agent.explain_file(requested_path)
    except (FileParseError, ModelResponseError) as error:
        print_exception(error)
        return
    
    print_agent_response(response)


def handle_ask_command(user_input, agent, workspace):
    parts = user_input.split(" ", 1)
    if len(parts) < 2:
        print_no_query()
        return

    query = parts[1]

    try:
        search_results = search_files(workspace, query)
        context = build_working_context(search_results)
        response = agent.ask_question(query, context)
    except (FileParseError, ModelResponseError) as error:
        print_exception(error)
        return

    print_agent_response(response)

def run_app(client, workspace, agent):
    print_intro(workspace)

    try: 
        while True:
            user_input = input("➜] : ") 

            if should_exit(user_input):
                print_goodbye()
                break

            elif should_explain(user_input):
                handle_explain_command(user_input, agent)

            elif should_ask(user_input):
                handle_ask_command(user_input, agent, workspace)
    
    except (KeyboardInterrupt, EOFError):
        print_goodbye()



def main():
    client = init_openai_client()
    args = parse_args()
    workspace = args.workspace
    agent = init_agent(workspace, client)

    run_app(client, workspace, agent)


if __name__ == "__main__":
    main()

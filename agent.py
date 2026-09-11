"""A simple AI agent built on the Anthropic SDK.

The agent can answer questions about the company's employees by calling
tools that read from employees.json. It uses the SDK's Tool Runner, which
handles the request -> execute tool -> loop cycle automatically.

Setup:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...   # never hardcode the key

Usage:
    python agent.py                       # interactive chat
    python agent.py "Who earns the most?"  # one-shot question
"""

import json
import os
import sys

import anthropic
from anthropic import beta_tool

MODEL = "claude-opus-5"


def load_employees():
    json_path = os.path.join(os.path.dirname(__file__), "employees.json")
    with open(json_path, "r") as f:
        return json.load(f)["employees"]


EMPLOYEES = load_employees()


# --- Tools the agent can call ------------------------------------------------

@beta_tool
def list_employees() -> str:
    """List every employee with their core details."""
    return json.dumps(EMPLOYEES)


@beta_tool
def get_employee(employee_id: int) -> str:
    """Look up a single employee by their numeric id."""
    employee = next((e for e in EMPLOYEES if e["id"] == employee_id), None)
    if employee is None:
        return json.dumps({"error": f"no employee with id {employee_id}"})
    return json.dumps(employee)


@beta_tool
def find_by_department(department: str) -> str:
    """Return all employees in the given department (case-insensitive)."""
    matches = [e for e in EMPLOYEES if e["department"].lower() == department.lower()]
    if not matches:
        return json.dumps({"error": f"no employees in {department}"})
    return json.dumps(matches)


TOOLS = [list_employees, get_employee, find_by_department]

SYSTEM_PROMPT = (
    "You are a helpful HR assistant. Answer questions about the company's "
    "employees using the provided tools. Be concise and cite specific "
    "employees by name when relevant."
)


def ask(client, question):
    """Send one question through the tool-running agent loop."""
    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=[{"role": "user", "content": question}],
    )
    final = runner.until_done()
    return "".join(block.text for block in final.content if block.type == "text")


def main():
    client = anthropic.Anthropic()

    # One-shot mode: question passed as command-line args.
    if len(sys.argv) > 1:
        print(ask(client, " ".join(sys.argv[1:])))
        return

    # Interactive mode.
    print("Employee agent ready. Ask a question (Ctrl-C or 'quit' to exit).")
    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"quit", "exit"}:
            break
        if question:
            print(ask(client, question))


if __name__ == "__main__":
    main()

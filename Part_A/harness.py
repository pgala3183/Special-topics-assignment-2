import os
import json
import requests
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()
console = Console()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL = os.getenv("MODEL", "google/gemini-pro")

if not OPENROUTER_API_KEY:
    console.print("[bold red]Warning: OPENROUTER_API_KEY is not set in environment or .env file.[/bold red]")

def execute_command(command: str) -> str:
    """Executes a terminal command and returns the output."""
    try:
        console.print(f"[bold yellow]Running command:[/bold yellow] {command}")
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout if result.stdout else "Command executed successfully with no output."
        else:
            return f"Error ({result.returncode}):\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Exception executing command: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a file."""
    try:
        console.print(f"[bold yellow]Writing to file:[/bold yellow] {filepath}")
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Exception writing file: {str(e)}"

def read_file(filepath: str) -> str:
    """Reads content from a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Exception reading file: {str(e)}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Executes a shell command on the local machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command string to execute (e.g., 'ls -la', 'python script.py')"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes string content to a file on the local machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to write to."
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write into the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file from the local machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to read from."
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]

def call_openrouter(messages: list) -> dict:
    """Calls the OpenRouter API with the conversation history."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Simple Coding Harness",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto"
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
        
    return response.json()

def run_agent(task: str):
    """Main loop for the autonomous agent."""
    console.print(Panel.fit(f"[bold green]Starting Agent Task:[/bold green]\n{task}", title="Agent Harness"))
    
    messages = [
        {"role": "system", "content": "You are an autonomous coding assistant. You can execute commands, read, and write files to complete tasks. When the task is fully complete and verified, give a final summary of your work."}
    ]
    
    messages.append({"role": "user", "content": task})
    
    iteration = 0
    max_iterations = 20
    
    while iteration < max_iterations:
        iteration += 1
        console.print(f"\n[bold blue]=== Iteration {iteration} ===[/bold blue]")
        
        try:
            response = call_openrouter(messages)
        except Exception as e:
            console.print(f"[bold red]API Error:[/bold red] {e}")
            break
            
        message = response["choices"][0]["message"]
        
        # Add the assistant's message to the history
        messages.append(message)
        
        if message.get("content"):
            console.print(Markdown(message["content"]))
            
        if "tool_calls" in message and message["tool_calls"]:
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call["id"]
                
                console.print(f"[bold cyan]Tool Call:[/bold cyan] {function_name}({arguments})")
                
                # Execute tool
                if function_name == "execute_command":
                    result = execute_command(arguments["command"])
                elif function_name == "write_file":
                    result = write_file(arguments["filepath"], arguments["content"])
                elif function_name == "read_file":
                    result = read_file(arguments["filepath"])
                else:
                    result = f"Error: Unknown function {function_name}"
                
                # Print abbreviated result
                print_result = result[:500] + "..." if len(result) > 500 else result
                console.print(f"[dim]Tool Result:\n{print_result}[/dim]")
                
                # Add tool response to history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": function_name,
                    "content": result
                })
        else:
            # If no tool calls and there is content, the agent is likely done
            console.print("[bold green]Task completed.[/bold green]")
            break

if __name__ == "__main__":
    console.print("[bold magenta]Welcome to the Simple Coding Harness (Part A)[/bold magenta]")
    user_task = input("Enter the task you want the agent to complete: ")
    if user_task.strip():
        run_agent(user_task)
    else:
        console.print("[bold red]No task provided. Exiting.[/bold red]")

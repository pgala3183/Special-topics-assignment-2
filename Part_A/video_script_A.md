# Part A: Simple Coding Harness - Video Script

**Target Length:** 2 Minutes

**[0:00 - 0:15] Introduction & Goal**
*Visual: Title slide or screen showing the `Part_A/harness.py` open in a code editor.*
**Voiceover:** "Hi everyone, in this video I'll be demonstrating a simple coding harness built entirely from scratch in Python. The goal was to create an autonomous coding agent using the OpenRouter API that can progressively execute terminal commands and manipulate files."

**[0:15 - 0:45] Code Walkthrough**
*Visual: Scroll through `harness.py`, highlighting the `execute_command`, `write_file`, and `call_openrouter` functions.*
**Voiceover:** "Let's take a look at the code. We've defined core tools: `execute_command` for running shell commands and `write_file`/`read_file` for interacting with the local filesystem. We pass these tool definitions to OpenRouter's API in the `call_openrouter` function. The main loop tracks the conversation history, parses tool calls from the LLM, executes them locally, and feeds the output back into the loop."

**[0:45 - 1:30] Demonstration (Execution)**
*Visual: Switch to the terminal. Run `python harness.py`. When prompted, type a task: "Create a Python script that calculates the first 10 Fibonacci numbers and run it."*
**Voiceover:** "Now let's see it in action. I'm running the harness and giving it a task to write and execute a script to calculate Fibonacci numbers. 
As you can see, the agent first decides to use the `write_file` tool to create `fib.py`. Then, it receives confirmation that the file was written. Next, it uses the `execute_command` tool to run `python fib.py`. The output is returned directly to the agent."

**[1:30 - 2:00] Conclusion & Wrap-up**
*Visual: Show the agent's final success message in the terminal, then briefly show the generated `fib.py` file.*
**Voiceover:** "The agent successfully completed the task without any human intervention beyond the initial prompt. It correctly recognized when the task was finished and terminated the loop. This demonstrates the core functionality of a progressively built coding harness using a tool-calling LLM. Thanks for watching!"

import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET
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

def search_arxiv(query: str, max_results: int = 3) -> list:
    """Searches arXiv for the given query and returns a list of paper summaries."""
    console.print(f"[bold cyan]Searching arXiv for:[/bold cyan] {query}")
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
    
    response = requests.get(url)
    if response.status_code != 200:
        console.print(f"[bold red]Failed to fetch from arXiv:[/bold red] HTTP {response.status_code}")
        return []

    root = ET.fromstring(response.content)
    papers = []
    
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.replace('\n', ' ').strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.replace('\n', ' ').strip()
        papers.append({"title": title, "summary": summary})
        
    return papers

def generate_ml_script(papers: list, topic: str) -> str:
    """Uses OpenRouter API to generate an ML script based on the research papers."""
    console.print("[bold cyan]Generating ML script based on research...[/bold cyan]")
    
    context = "\n\n".join([f"Title: {p['title']}\nAbstract: {p['summary']}" for p in papers])
    
    prompt = f"""
    You are an expert Machine Learning Researcher. I want to build a prototype for: {topic}
    
    Here are the abstracts of recent relevant papers:
    {context}
    
    Based on this research, please write a comprehensive starter PyTorch script (in Python) 
    that implements a basic version or prototype of the proposed approach. 
    Include comments explaining how it connects to the research.
    Return ONLY the Python code enclosed in ```python ``` blocks.
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AutoResearch Harness",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI coding assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        return f"# Error generating script: {response.text}"
        
    result_text = response.json()["choices"][0]["message"]["content"]
    
    # Extract code from markdown block
    if "```python" in result_text:
        code = result_text.split("```python")[1].split("```")[0].strip()
    else:
        code = result_text.strip()
        
    return code

def run_autoresearch(topic: str):
    console.print(Panel.fit(f"[bold green]Starting ML Auto-Research for:[/bold green] {topic}", title="AutoResearch Harness"))
    
    papers = search_arxiv(topic)
    
    if not papers:
        console.print("[bold red]No papers found or error occurred.[/bold red]")
        return
        
    console.print(f"[bold green]Found {len(papers)} papers![/bold green]")
    for i, p in enumerate(papers):
        console.print(f"{i+1}. [bold]{p['title']}[/bold]")
        
    script_content = generate_ml_script(papers, topic)
    
    output_file = f"{topic.replace(' ', '_').lower()}_prototype.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(script_content)
        
    console.print(f"[bold green]Success![/bold green] Generated prototype script saved to [bold]{output_file}[/bold]")
    console.print("\n[bold cyan]Preview of Generated Code:[/bold cyan]")
    console.print(Markdown(f"```python\n{script_content[:500]}...\n```"))

if __name__ == "__main__":
    console.print("[bold magenta]Welcome to the ML Auto-Research Harness (Part C)[/bold magenta]")
    user_topic = input("Enter an ML research topic (e.g., 'Transformer for time series'): ")
    if user_topic.strip():
        run_autoresearch(user_topic.strip())
    else:
        console.print("[bold red]No topic provided. Exiting.[/bold red]")

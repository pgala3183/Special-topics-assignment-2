# Part C: ML Auto-Research Harness - Video Script

**Target Length:** 2 Minutes

**[0:00 - 0:20] Introduction & Goal**
*Visual: Title slide showing "ML Auto-Research Harness (Part C)" followed by the `autoresearch_harness.py` code open in an IDE.*
**Voiceover:** "Hello! For Part C of the assignment, I built a custom end-to-end ML Auto-Research Harness. This Python script automates the tedious process of literature review and initial prototyping. It queries the arXiv API for the latest papers on a given topic, feeds the abstracts to an LLM via OpenRouter, and generates a PyTorch prototype script based on the state-of-the-art research."

**[0:20 - 0:50] Code Walkthrough**
*Visual: Scroll through `autoresearch_harness.py`, highlighting the `search_arxiv` and `generate_ml_script` functions.*
**Voiceover:** "The harness is lightweight but powerful. The `search_arxiv` function fetches recent papers and extracts the titles and abstracts. Then, `generate_ml_script` constructs a prompt with this context, asking the LLM to act as an ML researcher and write the PyTorch code. The main loop orchestrates these steps seamlessly."

**[0:50 - 1:30] Demonstration (Execution)**
*Visual: Terminal running `python autoresearch_harness.py`. Type the topic: "Vision Transformers for medical imaging".*
**Voiceover:** "Let's run a live demo. I'll execute the harness and ask it to research 'Vision Transformers for medical imaging'. 
Watch the terminal — it quickly queries arXiv and finds several relevant papers. Then, it sends this rich context to the coding assistant. And boom! It generates a complete PyTorch script tailored to the research it just found."

**[1:30 - 2:00] Conclusion & Wrap-up**
*Visual: Open the generated `vision_transformers_for_medical_imaging_prototype.py` script, scrolling through the code.*
**Voiceover:** "Let's take a look at the generated file. As you can see, we have a fully structured PyTorch script with a model definition, dataset loading stubs, and a training loop, complete with comments referencing the papers it analyzed. This auto-research harness is a massive time-saver for ML prototyping. Thanks for watching, and you can find all the code in the GitHub repo!"

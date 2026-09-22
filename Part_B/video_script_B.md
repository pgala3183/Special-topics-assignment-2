# Part B: DeepSeek Harness & Custom Plugins - Video Script

**Target Length:** 2 Minutes

**[0:00 - 0:20] Introduction & Setup**
*Visual: Show the `package.json` and `agent.cordis.yml` files in the code editor.*
**Voiceover:** "Welcome back! In Part B, I'll demonstrate setting up the DeepSeek Harness with multiple plugins. Using Cordis, we've configured our harness in `agent.cordis.yml`. You can see I've added 5 popular plugins from the marketplace, including the web UI, TUI, better sidebar, pocket, and mirage. I've also linked two custom plugins we built from scratch."

**[0:20 - 1:00] Custom Plugins Walkthrough**
*Visual: Switch to `plugins/dsh-plugin-second-brain/index.ts`, then `plugins/dsh-plugin-ui-dino/index.ts`.*
**Voiceover:** "Let's dive into the custom plugins. The first is a 'Second Brain' plugin. It listens for `agent/insight` events emitted by the harness and automatically writes them to markdown files locally, essentially acting as an automated knowledge base for the agent. The second plugin is a fun UI widget called 'UI Dino'. When the application mounts, it injects HTML and a script into the DeepSeek Harness web interface to render a floating dinosaur game on the screen."

**[1:00 - 1:40] Demonstration in Creator Mode**
*Visual: Terminal running `npm run dev` to start the harness. Then open a browser to `localhost:8080` showing the DeepSeek Harness UI with Creator Mode enabled.*
**Voiceover:** "Let's start it up. I'm running `npm run dev` to start the harness. Opening the web interface, we can see the 'Creator Mode' toggle is active. Look at the bottom right — there's our floating dinosaur from the `ui-dino` plugin! Now, let's trigger the Second Brain. I'll ask the agent to summarize a topic. As it thinks and emits insights, we can see the terminal logging the file creation."

**[1:40 - 2:00] Conclusion**
*Visual: Open the `knowledge_base/` folder and show the generated markdown file.*
**Voiceover:** "And here is the generated markdown file in our `knowledge_base` directory. Both plugins loaded seamlessly into the DeepSeek Harness architecture. This shows how modular and extensible the DeepSeek agent framework is using Cordis. Thanks for watching!"

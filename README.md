
# Aider v0.72.3.dev Coding Assistant with Rate and Token Limits

This is a modified version of [Aider](https://github.com/Aider-AI/aider), an AI pair programming tool that lets you edit code through natural language conversations.

## Rate and Token Limiting Features

This version adds comprehensive rate limiting functionality to prevent hitting API provider limits:

- Per-provider rate limits for OpenAI, Anthropic, Azure, and Cohere
- Multiple time window limits (per minute, hour, day) 
- Both request count and token count tracking
- Environment variable configuration
- Thread-safe operation using locks

### Default Provider Limits

**OpenAI:**
- 500 requests per minute
- 10,000 requests per hour
- 150,000 requests per day

**Anthropic:**
- 50 requests per minute 
- 40,000 input tokens per minute
- 8,000 output tokens per minute

**Azure OpenAI:**
- 240 requests per minute
- 14,400 requests per hour
- 60,000 input tokens per minute
- 24,000 output tokens per minute

**Cohere:**
- 100 requests per minute
- 6,000 requests per hour
- 30,000 input tokens per minute

## Installation

1. Remove any existing Aider installation:
```bash
pip uninstall aider-chat
```

2. Clone this repository:
```bash
git clone https://github.com/your-repo/aider.git
cd aider
```

3. Create a Python 3.12 virtual environment:
```bash
python3.12 -m venv venv
```

4. Activate the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

5. Install in editable mode:
```bash
pip install -e .
```

6. Configure your environment:
```bash
cp .env-example .env
# Edit .env with your API keys and custom rate limits
```

7. Verify installation:
```bash
aider --version  # Should show "aider 0.72.3.dev.r1+parse"
```

## Credits

- Original [Aider project](https://github.com/Aider-AI/aider)
- Rate limiting implementation: 80% coded by Aider + Claude 3.5 Sonnet
- Integration and testing: Leamsi Fontánez from [R1 Software](https://r1software.com)


<!-- SCREENCAST START -->
<p align="center">
  <img
    src="https://aider.chat/assets/screencast.svg"
    alt="aider screencast"
  >
</p>
<!-- SCREENCAST END -->

<!-- VIDEO START
<p align="center">
  <video style="max-width: 100%; height: auto;" autoplay loop muted playsinline>
    <source src="/assets/shell-cmds-small.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>
VIDEO END -->

<p align="center">
  <a href="https://discord.gg/Tv2uQnR88V">
    <img src="https://img.shields.io/badge/Join-Discord-blue.svg"/>
  </a>
  <a href="https://aider.chat/docs/install.html">
    <img src="https://img.shields.io/badge/Read-Docs-green.svg"/>
  </a>
</p>

See the
[usage documentation](https://aider.chat/docs/usage.html)
for more details.

## Features

- Run aider with the files you want to edit: `aider <file1> <file2> ...`
- Ask for changes:
  - Add new features or test cases.
  - Describe a bug.
  - Paste in an error message or or GitHub issue URL.
  - Refactor code.
  - Update docs.
- Aider will edit your files to complete your request.
- Aider [automatically git commits](https://aider.chat/docs/git.html) changes with a sensible commit message.
- [Use aider inside your favorite editor or IDE](https://aider.chat/docs/usage/watch.html).
- Aider works with [most popular languages](https://aider.chat/docs/languages.html): python, javascript, typescript, php, html, css, and more...
- Aider can edit multiple files at once for complex requests.
- Aider uses a [map of your entire git repo](https://aider.chat/docs/repomap.html), which helps it work well in larger codebases.
- Edit files in your editor or IDE while chatting with aider,
and it will always use the latest version.
Pair program with AI.
- [Add images to the chat](https://aider.chat/docs/usage/images-urls.html) (GPT-4o, Claude 3.5 Sonnet, etc).
- [Add URLs to the chat](https://aider.chat/docs/usage/images-urls.html) and aider will read their content.
- [Code with your voice](https://aider.chat/docs/usage/voice.html).
- Built-in rate limiting respects each LLM provider's limits (OpenAI, Anthropic, Azure, Cohere).
- Aider works best with Claude 3.5 Sonnet, DeepSeek V3, o1 & GPT-4o and can [connect to almost any LLM](https://aider.chat/docs/llms.html).


## Top tier performance

[Aider has one of the top scores on SWE Bench](https://aider.chat/2024/06/02/main-swe-bench.html).
SWE Bench is a challenging software engineering benchmark where aider
solved *real* GitHub issues from popular open source
projects like django, scikitlearn, matplotlib, etc.

## More info

- [Documentation](https://aider.chat/)
- [Installation](https://aider.chat/docs/install.html)
- [Usage](https://aider.chat/docs/usage.html)
- [Tutorial videos](https://aider.chat/docs/usage/tutorials.html)
- [Connecting to LLMs](https://aider.chat/docs/llms.html)
- [Configuration](https://aider.chat/docs/config.html)
- [Troubleshooting](https://aider.chat/docs/troubleshooting.html)
- [LLM Leaderboards](https://aider.chat/docs/leaderboards/)
- [GitHub](https://github.com/Aider-AI/aider)
- [Discord](https://discord.gg/Tv2uQnR88V)
- [Blog](https://aider.chat/blog/)


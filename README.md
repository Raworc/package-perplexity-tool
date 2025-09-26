# Perplexity AI CLI Tool

A minimal command-line interface for the Perplexity AI API that provides AI-powered search with real-time web results and citations.

## Features

- **Real-time web search**: Get AI-powered answers with current information from the web
- **Citations**: Automatic citations from web sources
- **Related questions**: Get suggestions for follow-up questions
- **Domain filtering**: Filter search results to specific domains (e.g., arxiv.org, reddit.com)
- **Recency filtering**: Filter results by time (hour, day, week, month)
- **Multiple output formats**: Pretty-print or JSON output
- **File saving**: Save responses to files for later reference

## Setup

1. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key:**

   ```bash
   export PERPLEXITY_API_KEY="your-api-key-here"
   ```

   Or add it to your `.env` file:

   ```
   PERPLEXITY_API_KEY=your-api-key-here
   ```

## Usage

### Basic Usage

```bash
# Simple question
python main.py "What is machine learning?"

# With citations and related questions
python main.py "Latest AI research 2025" --citations --related-questions

# Limit response length
python main.py "Python best practices" --max-tokens 300
```

### Advanced Usage

```bash
# Filter by domain
python main.py "Machine learning research" --domain-filter arxiv.org --recency week

# Multiple domains
python main.py "Climate change data" --domain-filter nature.com science.org --recency month

# JSON output
python main.py "Startup funding trends" --json --max-tokens 500

# Save to file
python main.py "Tech industry analysis" --save analysis.txt --citations --related-questions
```

### Command Line Options

| Option                | Description                       | Example                                |
| --------------------- | --------------------------------- | -------------------------------------- |
| `question`            | Question to ask Perplexity AI     | `"What is quantum computing?"`         |
| `--api-key`           | API key (or use env var)          | `--api-key "pplx-..."`                 |
| `--model`             | Model to use (default: sonar)     | `--model sonar`                        |
| `--max-tokens`        | Maximum tokens in response        | `--max-tokens 300`                     |
| `--temperature`       | Sampling temperature (0-1)        | `--temperature 0.7`                    |
| `--citations`         | Include citations (default: true) | `--citations`                          |
| `--no-citations`      | Exclude citations                 | `--no-citations`                       |
| `--images`            | Include images in response        | `--images`                             |
| `--related-questions` | Show related questions            | `--related-questions`                  |
| `--domain-filter`     | Filter to specific domains        | `--domain-filter arxiv.org reddit.com` |
| `--recency`           | Filter by recency                 | `--recency week`                       |
| `--json`              | Output raw JSON response          | `--json`                               |
| `--save`              | Save response to file             | `--save output.txt`                    |

### Recency Options

- `hour`: Results from the past hour
- `day`: Results from the past day
- `week`: Results from the past week
- `month`: Results from the past month

## Examples

### Research Query with Citations

```bash
python main.py "Latest developments in quantum computing 2024" \
  --citations \
  --related-questions \
  --domain-filter arxiv.org nature.com \
  --recency month \
  --max-tokens 500
```

### News and Current Events

```bash
python main.py "Current tech industry layoffs" \
  --recency week \
  --citations \
  --save tech_news.txt
```

### Academic Research

```bash
python main.py "BERT vs GPT transformer architectures" \
  --domain-filter arxiv.org scholar.google.com \
  --citations \
  --related-questions
```

## API Information

- **Endpoint**: https://api.perplexity.ai/chat/completions
- **Authentication**: Bearer token via `Authorization` header
- **Model**: Uses Perplexity's `sonar` model by default
- **Rate limits**: Check Perplexity AI documentation for current limits

## Error Handling

The tool handles common errors gracefully:

- Missing API key
- Network timeouts
- API rate limits
- Invalid responses
- File save errors

## Requirements

- Python 3.7+
- `requests` library
- Valid Perplexity AI API key

## Getting an API Key

1. Visit [Perplexity AI](https://www.perplexity.ai/)
2. Sign up for an account
3. Navigate to API settings
4. Generate a new API key
5. Add the key to your environment variables

## Security Note

Never commit your API key to version control. Always use environment variables or secure configuration files.

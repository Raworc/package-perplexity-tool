#!/usr/bin/env python3
"""
Minimal CLI for Perplexity AI API

Instructions:
  If user asks for information that can be fetched from internet:
   - Use this tool to get AI-powered search results with citations
   - Save the information to a file if needed
   - Parse responses to extract specific information

Usage:
  # Set API key as environment variable (recommended)
  export PERPLEXITY_API_KEY="your-api-key"
  python main.py "What is machine learning?" --citations --related-questions
  python main.py "Latest AI research 2024" --domain-filter arxiv.org --recency week

  # Or pass API key directly (not recommended for security)
  python main.py "Climate change data" --api-key "your-api-key" --json --max-tokens 500

Env:
  PERPLEXITY_API_KEY must be set as environment variable (recommended for security)

Docs:
  Endpoint: https://api.perplexity.ai/chat/completions
  Auth header: Authorization: Bearer <API_KEY>
  Models: sonar (recommended for research)

Setup:
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\\Scripts\\activate
  pip install requests
"""

import requests
import json
import argparse
import sys
import os
from typing import Optional, List, Dict, Any


class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "sonar",
        max_tokens: Optional[int] = None,
        temperature: float = 0.2,
        top_p: float = 0.9,
        return_citations: bool = True,
        search_domain_filter: Optional[List[str]] = None,
        return_images: bool = False,
        return_related_questions: bool = False,
        search_recency_filter: Optional[str] = None,
        top_k: int = 0,
        stream: bool = False,
        presence_penalty: float = 0,
        frequency_penalty: float = 1
    ) -> Dict[str, Any]:
        """Send a chat completion request to Perplexity API"""
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "return_citations": return_citations,
            "return_images": return_images,
            "return_related_questions": return_related_questions,
            "top_k": top_k,
            "stream": stream,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty
        }

        if search_domain_filter:
            payload["search_domain_filter"] = search_domain_filter

        if search_recency_filter:
            payload["search_recency_filter"] = search_recency_filter

        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
            if hasattr(e.response, 'text'):
                error_detail["response_text"] = e.response.text
            return error_detail

    def ask(self, question: str, **kwargs) -> Dict[str, Any]:
        """Simple method to ask a question to Perplexity"""
        messages = [{"role": "user", "content": question}]
        return self.chat_completion(messages, **kwargs)


def main():
    parser = argparse.ArgumentParser(description="Perplexity AI CLI Tool")
    parser.add_argument("question", help="Question to ask Perplexity AI")
    parser.add_argument("--api-key",
                        default=os.getenv("PERPLEXITY_API_KEY"),
                        help="Perplexity API key (or set PERPLEXITY_API_KEY env var)")
    parser.add_argument("--model", default="sonar",
                        help="Model to use")
    parser.add_argument("--max-tokens", type=int, help="Maximum tokens in response")
    parser.add_argument("--temperature", type=float, default=0.2,
                        help="Sampling temperature")
    parser.add_argument("--citations", action="store_true", default=True,
                        help="Include citations in response")
    parser.add_argument("--no-citations", action="store_true",
                        help="Exclude citations from response")
    parser.add_argument("--images", action="store_true",
                        help="Include images in response")
    parser.add_argument("--related-questions", action="store_true",
                        help="Include related questions")
    parser.add_argument("--domain-filter", nargs="*",
                        help="Filter search to specific domains")
    parser.add_argument("--recency", choices=["hour", "day", "week", "month"],
                        help="Filter by search recency")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON response")
    parser.add_argument("--pretty", action="store_true", default=True,
                        help="Pretty print output (default)")
    parser.add_argument("--save", type=str,
                        help="Save response to file (specify filename)")

    args = parser.parse_args()

    # Validate API key
    if not args.api_key:
        print("Error: Perplexity API key is required!", file=sys.stderr)
        print("Either set PERPLEXITY_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)

    client = PerplexityClient(args.api_key)

    kwargs = {
        "model": args.model,
        "temperature": args.temperature,
        "return_citations": args.citations and not args.no_citations,
        "return_images": args.images,
        "return_related_questions": args.related_questions
    }

    if args.max_tokens:
        kwargs["max_tokens"] = args.max_tokens

    if args.domain_filter:
        kwargs["search_domain_filter"] = args.domain_filter

    if args.recency:
        kwargs["search_recency_filter"] = args.recency

    response = client.ask(args.question, **kwargs)

    if "error" in response:
        print(f"Error: {response['error']}", file=sys.stderr)
        if "status_code" in response:
            print(f"Status Code: {response['status_code']}", file=sys.stderr)
        if "response_text" in response:
            print(f"Response: {response['response_text']}", file=sys.stderr)
        sys.exit(1)

    # Prepare output
    if args.json:
        output = json.dumps(response, indent=2 if args.pretty else None)
    else:
        try:
            content = response["choices"][0]["message"]["content"]
            output_parts = [content]

            if args.citations and response.get("citations"):
                output_parts.append("\nCitations:")
                for i, citation in enumerate(response["citations"], 1):
                    output_parts.append(f"{i}. {citation}")

            if args.related_questions and response.get("related_questions"):
                output_parts.append("\nRelated Questions:")
                for question in response["related_questions"]:
                    output_parts.append(f"• {question}")

            output = "\n".join(output_parts)

        except (KeyError, IndexError) as e:
            print(f"Error parsing response: {e}", file=sys.stderr)
            print(json.dumps(response, indent=2), file=sys.stderr)
            sys.exit(1)

    # Display output
    print(output)

    # Save to file if requested
    if args.save:
        try:
            with open(args.save, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\nResponse saved to: {args.save}", file=sys.stderr)
        except Exception as e:
            print(f"Error saving file: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
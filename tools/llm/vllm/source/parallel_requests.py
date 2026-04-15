#!/usr/bin/env python3
"""
Parallel async requests to LLM chat completions endpoint.
Usage: python parallel_requests.py --model MODEL --content CONTENT --num-requests N --max-tokens T --url URL
"""

import argparse
import asyncio
import json
import sys
import time

import aiohttp


async def send_request(
    session: aiohttp.ClientSession,
    url: str,
    model: str,
    content: str,
    max_tokens: int,
    request_id: int,
) -> dict:
    """Send a single chat completions request."""
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "max_tokens": max_tokens,
    }

    headers = {"Content-Type": "application/json"}

    try:
        start = time.monotonic()
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            elapsed_ms = (time.monotonic() - start) * 1000
            return {
                "request_id": request_id,
                "status": response.status,
                "response": result,
                "usage": result.get("usage", {}),
                "content": (
                    result.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    if result.get("choices")
                    else ""
                ),
                "response_time_ms": round(elapsed_ms, 1),
            }
    except aiohttp.ClientError as e:
        return {"request_id": request_id, "status": None, "error": str(e)}
    except Exception as e:
        return {"request_id": request_id, "status": None, "error": str(e)}


def format_result(r: dict) -> str:
    """Format a single request result with stats and content."""
    rid = r["request_id"]
    status = r["status"]
    usage = r.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    content = r.get("content", "")

    lines = [
        f"─" * 60,
        f"Request #{rid}  status={status}  response_time={r.get('response_time_ms', 0)}ms",
        f"  prompt_tokens={prompt_tokens}  completion_tokens={completion_tokens}  total_tokens={total_tokens}",
        f"  content: {content[:300]}{'...' if len(content) > 300 else ''}",
        f"",
    ]
    return "\n".join(lines)


def print_summary(results: list[dict]):
    """Print overall summary stats."""
    total_prompt = sum(r.get("usage", {}).get("prompt_tokens", 0) for r in results)
    total_completion = sum(r.get("usage", {}).get("completion_tokens", 0) for r in results)
    total_all = sum(r.get("usage", {}).get("total_tokens", 0) for r in results)
    statuses = [r["status"] for r in results]
    successes = sum(1 for s in statuses if s == 200)
    total_time = sum(r.get("response_time_ms", 0) for r in results)
    avg_time = total_time / len(results) if results else 0

    lines = [
        f"═" * 60,
        f"SUMMARY  ({len(results)} requests, {successes} succeeded, {len(results)-successes} failed)",
        f"  total_prompt_tokens={total_prompt}",
        f"  total_completion_tokens={total_completion}",
        f"  total_tokens={total_all}",
        f"  avg_prompt_tokens={total_prompt // len(results) if results else 0}",
        f"  avg_completion_tokens={total_completion // len(results) if results else 0}",
        f"  avg_response_time={avg_time:.1f}ms",
        f"  statuses={statuses}",
        f"═" * 60,
    ]
    print("\n".join(lines))


async def run_parallel_requests(
    url: str,
    model: str,
    content: str,
    max_tokens: int,
    num_requests: int,
) -> list[dict]:
    """Run N parallel requests and return all results."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_request(session, url, model, content, max_tokens, i)
            for i in range(num_requests)
        ]
        results = await asyncio.gather(*tasks)
        return list(results)


def main():
    parser = argparse.ArgumentParser(description="Parallel async LLM chat completions requests")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/v1/chat/completions",
        help="API endpoint URL",
    )
    parser.add_argument(
        "--model",
        default="DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking",
        help="Model name",
    )
    parser.add_argument(
        "--content",
        default="Hi there",
        help="User message content",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Max tokens to generate",
    )
    parser.add_argument(
        "--num-requests",
        type=int,
        default=1,
        help="Number of parallel requests",
    )

    args = parser.parse_args()

    print(
        f"Sending {args.num_requests} request(s) to {args.url}",
        f"  model   : {args.model}",
        f"  max_tokens: {args.max_tokens}",
        f"  content : {args.content}",
        sep="\n",
        file=sys.stderr,
    )

    results = asyncio.run(
        run_parallel_requests(
            args.url,
            args.model,
            args.content,
            args.max_tokens,
            args.num_requests,
        )
    )

    for r in results:
        print(format_result(r))

    print_summary(results)


if __name__ == "__main__":
    main()
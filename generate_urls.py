#!/usr/bin/env python3
"""
Generate unique participant URLs for the Cultural Face Perception Experiment.

Usage:
    python generate_urls.py --base-url https://USERNAME.github.io/cultural-face-experiment --n 50
    python generate_urls.py --base-url https://USERNAME.github.io/cultural-face-experiment --n 50 --prefix PILOT
    python generate_urls.py --base-url https://USERNAME.github.io/cultural-face-experiment --n 50 --output urls.txt
"""

import argparse
import sys


def generate_participant_urls(base_url: str, n: int, prefix: str = "P", output_file: str = None):
    """
    Generate N unique participant URLs.

    Args:
        base_url: Base URL of the experiment (e.g., https://user.github.io/experiment)
        n: Number of URLs to generate
        prefix: Prefix for participant IDs (default: "P")
        output_file: Optional file to write URLs to
    """
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')

    urls = []
    for i in range(1, n + 1):
        pid = f"{prefix}{i:03d}"
        url = f"{base_url}/?pid={pid}"
        urls.append((pid, url))

    # Output
    output_lines = []
    output_lines.append(f"Generated {n} participant URLs")
    output_lines.append(f"Base URL: {base_url}")
    output_lines.append(f"Prefix: {prefix}")
    output_lines.append("-" * 60)
    output_lines.append("")

    for pid, url in urls:
        output_lines.append(f"{pid}\t{url}")

    output_text = "\n".join(output_lines)

    if output_file:
        with open(output_file, 'w') as f:
            # Write just the URLs for easy copy-paste
            for _, url in urls:
                f.write(url + "\n")
        print(f"URLs written to {output_file}")
        print(output_text)
    else:
        print(output_text)

    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Generate unique participant URLs for the Cultural Face Perception Experiment"
    )
    parser.add_argument(
        "--base-url", "-b",
        required=True,
        help="Base URL of the experiment (e.g., https://user.github.io/cultural-face-experiment)"
    )
    parser.add_argument(
        "--n", "-n",
        type=int,
        default=50,
        help="Number of URLs to generate (default: 50)"
    )
    parser.add_argument(
        "--prefix", "-p",
        default="P",
        help="Prefix for participant IDs (default: P)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file to write URLs to"
    )

    args = parser.parse_args()

    generate_participant_urls(
        base_url=args.base_url,
        n=args.n,
        prefix=args.prefix,
        output_file=args.output
    )


if __name__ == "__main__":
    main()

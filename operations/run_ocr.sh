#!/bin/bash

# OCR Benchmark Runner
# Exports the API key and runs the OCR benchmark

export GEMINI_API_KEY='AIzaSyA8G65lQN5hweWpYE1ag7imAVQxYEnr5gE'

cd "$(dirname "$0")"
source ../.venv/bin/activate

echo "Starting NID OCR Benchmark Processing..."
echo "API Key: ${GEMINI_API_KEY:0:20}..."
echo ""

python3 ocr_benchmark.py "$@"

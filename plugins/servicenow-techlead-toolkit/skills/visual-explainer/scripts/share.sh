#!/bin/bash
# Share a visual-explainer HTML file via Vercel (zero-auth claimable deployment)
# Usage: bash share.sh <path-to-html-file>
# Requires: vercel CLI (npm install -g vercel)

set -e

HTML_FILE="$1"

if [ -z "$HTML_FILE" ]; then
  echo "Usage: bash share.sh <path-to-html-file>"
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "Error: file not found: $HTML_FILE"
  exit 1
fi

if ! command -v vercel &> /dev/null; then
  echo "Error: vercel CLI not found. Install with: npm install -g vercel"
  exit 1
fi

TEMP_DIR=$(mktemp -d)
cp "$HTML_FILE" "$TEMP_DIR/index.html"

echo "Deploying to Vercel..."
cd "$TEMP_DIR"
DEPLOY_OUTPUT=$(vercel --prod --yes 2>&1)
DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -E "^https://" | tail -1)

rm -rf "$TEMP_DIR"

echo ""
echo "✓ Shared successfully!"
echo "Live URL:  $DEPLOY_URL"
echo "Claim URL: https://vercel.com/import?s=$DEPLOY_URL"

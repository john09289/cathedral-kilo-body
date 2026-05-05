#!/usr/bin/env python3
"""
DEPLOY CATHEDRAL WORKER - Deploy the Cloudflare Worker for the Cathedral Gateway
IMPORTANT: Set environment variables:
  CLOUDFLARE_API_TOKEN — your Cloudflare API token (full access)
  CLOUDFLARE_ACCOUNT_ID — 84834faf11605476f68b85b6d85c74dc
"""
import requests
import json
import os

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "84834faf11605476f68b85b6d85c74dc")
TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "cfat_PLACEHOLDER")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

worker_name = "rahabs-gate"
gatekeeper_path = os.path.join(os.path.dirname(__file__), "..", "agents", "gatekeeper.js")
with open(gatekeeper_path) as f:
    worker_script = f.read()

print(f"Deploying Worker '{worker_name}' to account {ACCOUNT_ID}...")
put_resp = requests.put(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}",
    headers=HEADERS,
    data=worker_script,
    params={"include_subdomain_availability": "true"}
)
print(f"PUT: {put_resp.status_code}")
if not put_resp.ok:
    print(put_resp.text)
    sys.exit(1)

subdomain_resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}/subdomain",
    headers=HEADERS,
    json={"enabled": True}
)
print(f"Subdomain: {subdomain_resp.status_code}")

subdomain_info = requests.get(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}/subdomain",
    headers=HEADERS
)
print(f"URL: https://{subdomain_info.json()['result']['subdomain']}.workers.dev")

print("\nNext: Set GITHUB_TOKEN secret via: wrangler secret put GITHUB_TOKEN --name rahabs-gate")

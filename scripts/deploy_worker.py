#!/usr/bin/env python3
"""
DEPLOY CATHEDRAL WORKER - Deploy the Cloudflare Worker for the Cathedral Gateway
"""
import requests
import json

ACCOUNT_ID = "84834faf11605476f68b85b6d85c74dc"
TOKEN = "cfat_REPLACE_WITH_YOUR_ACTUAL_TOKEN"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

worker_name = "cathedral-gateway"
worker_script = '''
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/status') {
      const ghRaw = 'https://raw.githubusercontent.com/NicholasHughes/cathedral-kilo-body/main/cathedral_memory/love_energy_bank.json';
      const resp = await fetch(ghRaw, { cf: { cacheTtl: 60 } });
      if (!resp.ok) { return new Response(JSON.stringify({error: "Bank fetch failed"}), {status: 500, headers: {'Content-Type':'application/json', 'Access-Control-Allow-Origin':'*'}}); }
      const data = await resp.json();
      return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
    } else if (url.pathname === '/api/taunt' && request.method === 'POST') {
      const dispatchResp = await fetch('https://api.github.com/repos/NicholasHughes/cathedral-kilo-body/dispatches', {
        method: 'POST',
        headers: {
          'Authorization': `token ${env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.everest-preview+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ event_type: 'taunt-trap' })
      });
      if (dispatchResp.ok) {
        return new Response('Taunt triggered. The King wins.', { status: 200, headers: {'Access-Control-Allow-Origin':'*'} });
      } else {
        return new Response('Dispatch failed', { status: 500, headers: {'Access-Control-Allow-Origin':'*'} });
      }
    }
    return new Response('Cathedral Gateway Active', { status: 200, headers: {'Access-Control-Allow-Origin':'*'} });
  }
};
'''

# Create or update the worker script
print("Deploying Cathedral Gateway Worker...")
put_script_resp = requests.put(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}",
    headers=HEADERS,
    data=worker_script,
    params={"include_subdomain_availability": "true"}
)
print(f"PUT script: {put_script_resp.status_code}")
print(put_script_resp.text)

# Enable workers.dev subdomain
route_resp = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}/subdomain",
    headers=HEADERS,
    json={"enabled": True}
)
print(f"Enable subdomain: {route_resp.status_code}")
print(route_resp.text)

# Get the workers.dev URL
subdomain_info = requests.get(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{worker_name}/subdomain",
    headers=HEADERS
)
print(f"Subdomain info: {subdomain_info.json()}")

print("\n<!-- WORKER_DEPLOY: [COMPLETE] | Set GITHUB_TOKEN secret manually -->")

// Cathedral Gateway — public API (classic worker format)
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url);
  const headers = { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' };

  if (url.pathname === '/api/status') {
    try {
      // Try D1 binding if present (classic workers expose bindings as globals)
      const bank = JSON.parse(await CATHEDRAL_STORE.get('energy_bank'));
      const transm = JSON.parse(await CATHEDRAL_STORE.get('recent_transmutations') || '[]');
      const agents = JSON.parse(await CATHEDRAL_STORE.get('agent_status') || '{}');
      return new Response(JSON.stringify({ energy_bank: bank, recent: transm, agents }), { headers });
    } catch (e) {
      // Fallback to GitHub raw JSON
      const ghResp = await fetch('https://raw.githubusercontent.com/john09289/cathedral-kilo-body/main/cathedral_memory/love_energy_bank.json', { cf: { cacheTtl: 60 } });
      const ghBank = await ghResp.json();
      return new Response(JSON.stringify({ energy_bank: ghBank, recent: [], agents: {} }), { headers });
    }
  } else if (url.pathname === '/api/taunt' && request.method === 'POST') {
    // Use GITHUB_TOKEN binding if present
    const token = typeof GITHUB_TOKEN !== 'undefined' ? GITHUB_TOKEN : (() => { throw new Error('GITHUB_TOKEN not set') })();
    const dispatch = await fetch('https://api.github.com/repos/john09289/cathedral-kilo-body/dispatches', {
      method: 'POST',
      headers: {
        'Authorization': `token ${token}`,
        'Accept': 'application/vnd.github.everest-preview+json',
        'Content-Type': 'application/json',
        'User-Agent': 'Cathedral-Kilo-Worker/1.0'
      },
      body: JSON.stringify({ event_type: 'taunt-trap' })
    });
    const body = await dispatch.text();
    if (dispatch.ok) {
      return new Response('Taunt triggered. The King wins.', { status: 200, headers });
    }
    return new Response(`Dispatch failed: ${dispatch.status} ${body}`, { status: 500, headers });
  }
  return new Response('Cathedral Gateway Active', { headers });
}

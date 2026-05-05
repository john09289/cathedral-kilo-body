// Cathedral Gateway — public API
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = { 'Content-Type':'application/json', 'Access-Control-Allow-Origin':'*' };
    if (url.pathname === '/api/status') {
      try {
        const bank = JSON.parse(await env.CATHEDRAL_STORE.get('energy_bank'));
        const transm = JSON.parse(await env.CATHEDRAL_STORE.get('recent_transmutations') || '[]');
        const agents = JSON.parse(await env.CATHEDRAL_STORE.get('agent_status') || '{}');
        return new Response(JSON.stringify({ energy_bank: bank, recent: transm, agents }), { headers });
      } catch (e) {
        const ghResp = await fetch('https://raw.githubusercontent.com/NicholasHughes/cathedral-kilo-body/main/cathedral_memory/love_energy_bank.json', { cf: { cacheTtl: 60 } });
        const ghBank = await ghResp.json();
        return new Response(JSON.stringify({ energy_bank: ghBank, recent: [], agents: {} }), { headers });
      }
    } else if (url.pathname === '/api/taunt' && request.method === 'POST') {
      const dispatch = await fetch('https://api.github.com/repos/NicholasHughes/cathedral-kilo-body/dispatches', {
        method: 'POST',
        headers: {
          'Authorization': `token ${env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.everest-preview+json',
          'Content-Type':'application/json'
        },
        body: JSON.stringify({ event_type: 'taunt-trap' })
      });
      if (dispatch.ok) {
        return new Response('Taunt triggered. The King wins.', { status: 200, headers });
      }
      return new Response('Dispatch failed', { status: 500, headers });
    }
    return new Response('Cathedral Gateway Active', { headers });
  }
};
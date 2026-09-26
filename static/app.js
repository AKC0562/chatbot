// Kyurem frontend — minimal professional chat + Black/White theme
(() => {
  const chat = document.getElementById('chat');
  const form = document.getElementById('composer');
  const input = document.getElementById('input');
  const send = document.getElementById('send');
  const sugg = document.getElementById('suggestions');
  const statusText = document.getElementById('status-text');
  const modelStatus = document.getElementById('model-status');

  const API = { chat: '/api/chat', health: '/api/health', clear: '/api/clear' };
  let sid = localStorage.getItem('kyurem-sid') || ('kyurem_' + Math.random().toString(36).slice(2, 10));
  localStorage.setItem('kyurem-sid', sid);
  let busy = false;

  /* ---------- theme: dark = Black Kyurem, light = White Kyurem ---------- */
  const root = document.documentElement;
  const saved = localStorage.getItem('kyurem-theme') || 'dark';
  root.setAttribute('data-theme', saved);
  const toggleTheme = () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('kyurem-theme', next);
  };
  document.getElementById('theme-btn').onclick = toggleTheme;
  const sideT = document.getElementById('theme-toggle-side');
  if (sideT) sideT.onclick = toggleTheme;

  /* ---------- sidebar mobile ---------- */
  const sidebar = document.getElementById('sidebar');
  const scrim = document.getElementById('scrim');
  document.getElementById('menu-btn').onclick = () => { sidebar.classList.add('open'); scrim.classList.add('show'); };
  scrim.onclick = () => { sidebar.classList.remove('open'); scrim.classList.remove('show'); };

  /* ---------- helpers ---------- */
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  function md(t) {
    let h = esc(t);
    h = h.replace(/```(\w*)\n([\s\S]*?)```/g, (_, l, c) => `<pre><code>${c.replace(/^\n/, '')}</code></pre>`);
    h = h.replace(/`([^`]+)`/g, '<code>$1</code>');
    h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    return h;
  }
  const time = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  function scrollDown() { requestAnimationFrame(() => chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' })); }

  function avatarHTML() {
    return `<div class="avatar"><img src="/static/kyurem.png" alt="K" onerror="this.outerHTML='<div class=af>K</div>'"></div>`;
  }

  function addMsg(text, who) {
    const div = document.createElement('div');
    div.className = 'msg ' + who;
    if (who === 'bot') {
      div.innerHTML = `${avatarHTML()}<div class="bubble-wrap"><div class="bubble">${md(text)}</div>
        <div class="meta"><span>${time()} · Kyurem</span><button class="copy-btn">Copy</button></div></div>`;
      div.querySelector('.copy-btn').onclick = (e) => {
        navigator.clipboard.writeText(text).catch(() => {});
        e.target.textContent = 'Copied';
        setTimeout(() => e.target.textContent = 'Copy', 1200);
      };
    } else {
      div.innerHTML = `<div class="bubble-wrap"><div class="bubble">${esc(text)}</div>
        <div class="meta" style="justify-content:flex-end"><span>${time()} · You</span></div></div>`;
    }
    chat.appendChild(div);
    scrollDown();
    return div;
  }

  function showWelcome() {
    if (chat.children.length) return;
    const w = document.createElement('div');
    w.className = 'welcome';
    w.innerHTML = `
      <img class="w-logo" src="/static/kyurem.png" alt="Kyurem" onerror="this.style.display='none'">
      <h2>K Y U R E M</h2>
      <div class="w-sub">#646 · BOUNDARY POKÉMON · UNOVA</div>
      <p>I am <strong>Kyurem</strong> — the hollow shell of the Original Dragon.
      Fused with Zekrom I become <strong>Black Kyurem</strong> (dark mode).
      Fused with Reshiram I become <strong>White Kyurem</strong> (light mode).<br><br>
      Ask me anything — lore, code, or counsel.</p>`;
    chat.appendChild(w);
    addMsg('Greetings, trainer. I am Kyurem. The boundary awaits your question. ❄', 'bot');
  }

  function typing() {
    const d = document.createElement('div');
    d.className = 'msg bot'; d.id = 'typing';
    d.innerHTML = `${avatarHTML()}<div class="typing"><span></span><span></span><span></span></div>`;
    chat.appendChild(d); scrollDown();
    return d;
  }

  /* ---------- send ---------- */
  async function sendMsg(text) {
    text = (text || input.value || '').trim();
    if (!text || busy) return;
    busy = true;
    document.querySelector('.welcome')?.remove();
    addMsg(text, 'user');
    input.value = ''; input.style.height = 'auto'; send.disabled = true;
    const t = typing();
    try {
      const r = await fetch(API.chat, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sid })
      });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const d = await r.json();
      t.remove();
      if (d.reply) { if (d.session_id) { sid = d.session_id; localStorage.setItem('kyurem-sid', sid); } addMsg(d.reply, 'bot'); }
      else addMsg('My ice flickered — ' + (d.error || 'unknown error'), 'bot');
    } catch {
      t.remove();
      addMsg('Cannot reach server. Open the Flask-served page http://127.0.0.1:5000 (not client/index.html, not file://) and hard-refresh (Ctrl+Shift+R).', 'bot');
    }
    busy = false; input.focus();
  }

  form.addEventListener('submit', (e) => { e.preventDefault(); sendMsg(); });
  input.addEventListener('input', () => {
    send.disabled = !input.value.trim() || busy;
    input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 140) + 'px';
  });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMsg(); }
  });
  sugg.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-q]');
    if (b) sendMsg(b.dataset.q);
  });

  async function newChat() {
    try { await fetch(API.clear, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ session_id: sid }) }).then(r => r.json()).then(d => { if (d.session_id) { sid = d.session_id; localStorage.setItem('kyurem-sid', sid); } }); } catch {}
    chat.innerHTML = ''; showWelcome(); sidebar.classList.remove('open'); scrim.classList.remove('show');
  }
  document.getElementById('new-chat-btn').onclick = newChat;
  document.getElementById('clear-btn').onclick = newChat;

  /* ---------- health ---------- */
  async function health() {
    try {
      const r = await fetch(API.health, { cache: 'no-store' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const d = await r.json();
      console.log('[Kyurem] health:', d);
      if (d.gemini_online) {
        statusText.textContent = 'Online';
        modelStatus.textContent = d.model + ' · live';
      } else {
        // Server IS reachable — only the AI key is missing. Don't call this "offline".
        statusText.textContent = 'Online (limited AI)';
        modelStatus.textContent = d.model + ' · server up, needs GEMINI_API_KEY';
      }
    } catch (err) {
      console.warn('[Kyurem] health check failed:', err);
      statusText.textContent = 'Unreachable';
      modelStatus.textContent = 'open http://127.0.0.1:5000 (Flask), not file://';
    }
  }

  showWelcome();
  health(); setInterval(health, 30000);
  input.focus();
})();

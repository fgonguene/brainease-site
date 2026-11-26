/* BrainEase site script: shared facts, navigation, motion, Talk to Eze and appointment requests.
   Every practical fact lives in BE below: change it here and it changes on every page. */
{
const BE = {
  address: '440 Quadrangle Dr., Suite I, Bolingbrook, IL 60440',
  mapsUrl: 'https://www.google.com/maps/search/?api=1&query=440+Quadrangle+Dr+Suite+I+Bolingbrook+IL+60440',
  phone: '331-330-7228',
  phoneHref: 'tel:+13313307228',
  smsHref: 'sms:+13313307228',
  email: 'wecare@braineasehealth.org',
  hours: 'Monday to Friday, 9 am to 5 pm',
  inPerson: 'Thursdays, in Bolingbrook',
  insurance: ['BCBSIL', 'Aetna', 'UnitedHealthcare / Optum', 'Blue Cross Community Health Plans (BCCHP)'],
  /* Back end (set by Muse). While null, the site runs in demo mode and sends nothing. */
  bookingEndpoint: null,   // POST JSON, see the technical file
  chatEndpoint: null       // POST JSON {lang, messages}, returns {reply}
};
window.BE = BE;

/* ---------- shared facts ---------- */
document.querySelectorAll('[data-cfg]').forEach(el => {
  const k = el.dataset.cfg;
  if (k === 'insurance') { el.textContent = ''; BE.insurance.forEach(i => { const li = document.createElement('li'); li.textContent = i; el.appendChild(li); }); return; }
  if (BE[k] != null) el.textContent = BE[k];
});
document.querySelectorAll('[data-href]').forEach(el => { if (BE[el.dataset.href]) el.href = BE[el.dataset.href]; });
const yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();

/* ---------- header and mobile menu ---------- */
const hd = document.querySelector('.hd');
const onScroll = () => hd && hd.classList.toggle('scrolled', scrollY > 8);
addEventListener('scroll', onScroll, {passive: true}); onScroll();
const burger = document.querySelector('.burger'), drawer = document.getElementById('drawer');
if (burger && drawer) burger.addEventListener('click', () => {
  const open = burger.getAttribute('aria-expanded') !== 'true';
  burger.setAttribute('aria-expanded', open); drawer.classList.toggle('open', open);
  document.body.style.overflow = open ? 'hidden' : '';
});

/* ---------- motion: reveal on scroll, Eze draws himself when seen ---------- */
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add(e.target.classList.contains('ez') ? 'live' : 'in');
  io.unobserve(e.target);
}), {threshold: .18});
document.querySelectorAll('.reveal, svg.ez').forEach(el => io.observe(el));

/* ---------- appointment request (chat card and contact page share this) ---------- */
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const nextWeekdays = n => {
  const out = []; const d = new Date(); d.setHours(12, 0, 0, 0);
  while (out.length < n) { d.setDate(d.getDate() + 1); const w = d.getDay(); if (w > 0 && w < 6) out.push(new Date(d)); }
  return out;
};
const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
let uid = 0;
const optGroup = (name, items, type = 'radio') => items.map(([v, l]) => `<label class="opt"><input type="${type}" name="${name}" value="${v}"><span>${l}</span></label>`).join('');
const bookingHTML = (compact) => {
  const id = 'bk' + (++uid);
  const days = nextWeekdays(compact ? 6 : 10).map(d => [iso(d), `${DAYS[d.getDay()]} ${MON[d.getMonth()]} ${d.getDate()}`]);
  return `<form class="form" novalidate data-booking id="${id}">
  <fieldset class="field"><legend>I am…</legend><div class="opts">${optGroup('patientType', [['new', 'New: free 15-min intro call'], ['current', 'A current patient']])}</div></fieldset>
  <fieldset class="field"><legend>Preferred days <span class="small">(pick one or more)</span></legend><div class="opts">${optGroup('days', days.concat([['any', 'Any day']]), 'checkbox')}</div></fieldset>
  <fieldset class="field"><legend>Preferred time</legend><div class="opts">${optGroup('time', [['morning', 'Morning 9–12'], ['afternoon', 'Afternoon 12–5'], ['any', 'Any time']])}</div></fieldset>
  <div class="two">
    <div class="field"><label for="${id}n">Full name</label><input id="${id}n" name="name" type="text" autocomplete="name" required></div>
    <div class="field"><label for="${id}p">Phone</label><input id="${id}p" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
  </div>
  <div class="field"><label for="${id}e">Email <span class="small">(phone or email)</span></label><input id="${id}e" name="email" type="email" autocomplete="email"></div>
  <fieldset class="field"><legend>Language</legend><div class="opts">${optGroup('language', [['en', 'English'], ['fr', 'Français']])}</div></fieldset>
  <label class="hp" aria-hidden="true">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label>
  <label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I agree to be contacted by phone, text or email about this request. I won't share health information here.</span></label>
  <p class="err" role="alert"></p>
  <button class="btn" type="submit">Send my request</button>
  <p class="small">This is a request, not a confirmed appointment. In an emergency, call or text 988 or call 911.</p>
</form>
<div class="done" role="status"><svg class="ez live" viewBox="-40 -80 80 86" width="90" height="98" aria-hidden="true">${figure('wave')}</svg><h3 style="margin-top:8px">Request sent</h3><p class="small" style="margin-top:6px">Sariette aims to get back to you within one business day.</p></div>`;
};
const readForm = f => {
  const fd = new FormData(f);
  return {
    patientType: fd.get('patientType') || '', preferredDays: fd.getAll('days'), timeWindow: fd.get('time') || '',
    name: (fd.get('name') || '').trim(), phone: (fd.get('phone') || '').trim(), email: (fd.get('email') || '').trim(),
    language: fd.get('language') || 'en', consent: fd.get('consent') === 'yes', website: fd.get('website') || '',
    page: location.pathname, sentAt: new Date().toISOString()
  };
};
const validate = d => {
  if (!d.patientType) return 'Please tell us whether you are a new or current patient.';
  if (!d.preferredDays.length) return 'Please pick at least one day, or “Any day”.';
  if (!d.timeWindow) return 'Please pick a preferred time.';
  if (d.name.length < 2) return 'Please add your full name.';
  if (!d.phone && !d.email) return 'Please add a phone number or an email so Sariette can reach you.';
  if (d.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return 'That email address looks incomplete.';
  if (!d.consent) return 'Please check the consent box.';
  return '';
};
const sendBooking = async d => {
  if (d.website) return true;            // honeypot: silently ignore bots
  if (!BE.bookingEndpoint) { await new Promise(r => setTimeout(r, 700)); return 'demo'; }
  const r = await fetch(BE.bookingEndpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(d)});
  if (!r.ok) throw new Error('send');
  return true;
};
const wireBooking = (root, onDone) => {
  const f = root.querySelector('form[data-booking]'); if (!f) return;
  const err = f.querySelector('.err'), btn = f.querySelector('button[type=submit]');
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const d = readForm(f), m = validate(d);
    err.textContent = m; err.classList.toggle('on', !!m); if (m) return;
    btn.disabled = true; btn.textContent = 'Sending…';
    try {
      const res = await sendBooking(d);
      root.classList.add('sent');
      if (res === 'demo') { const n = document.createElement('p'); n.className = 'small'; n.textContent = 'Preview mode: nothing was sent. The live site emails this request to Sariette.'; root.querySelector('.done').appendChild(n); }
      onDone && onDone(d, res);
    } catch (x) {
      err.textContent = `It didn't go through. Please call or text ${BE.phone}, or email ${BE.email}.`; err.classList.add('on');
      btn.disabled = false; btn.textContent = 'Send my request';
    }
  });
};
document.querySelectorAll('[data-booking-page]').forEach(c => { c.insertAdjacentHTML('afterbegin', bookingHTML(false)); wireBooking(c); c.querySelectorAll('svg.ez').forEach(s => io.observe(s)); });

/* ---------- Eze figure (shared by widget and forms) ---------- */
function figure(pose) {
  const P = {
    sit: [['c', -2, -41, 9], ['p', 'M-1.5 -32 L0 0'], ['p', 'M-1 -23 L9 -12 L15 -4'], ['p', 'M0 0 L16 1'], ['leg', 'M16 1 L18 19 L25 19']],
    wave: [['c', 0, -63, 9], ['p', 'M0 -54 L0 -24'], ['p', 'M0 -24 L-7 0'], ['p', 'M0 -24 L7 0'], ['p', 'M0 -46 L-9 -31'], ['wv', 'M0 -46 L11 -56 L14 -69']]
  };
  const parts = P[pose].map((s, i) => {
    const st = `style="--d:${(i * .2).toFixed(1)}s"`;
    if (s[0] === 'c') return `<circle class="d" cx="${s[1]}" cy="${s[2]}" r="${s[3]}" pathLength="1" ${st}/>`;
    const path = `<path class="d" d="${s[1]}" pathLength="1" ${st}/>`;
    return s[0] === 'leg' ? `<g class="leg">${path}</g>` : s[0] === 'wv' ? `<g class="wv">${path}</g>` : path;
  }).join('');
  return `<g fill="none" stroke="var(--ez,#3d7f1f)" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">${parts}</g>`;
}
const avatar = `<svg viewBox="-24 -54 52 76" aria-hidden="true"><g style="--ez:#fffaf2">${figure('sit')}</g></svg>`;

/* ---------- Talk to Eze ---------- */
const T = {
  en: {
    hi: `Hi, I'm Eze, the BrainEase assistant. I can help with hours, location, insurance, telehealth, or a request for an appointment. Please don't share health information here.`,
    hours: `We're open ${BE.hours}. Office visits are on ${BE.inPerson}; telehealth covers all of Illinois.`,
    location: `In-person visits are on Thursdays at ${BE.address}. Telehealth is available anywhere in Illinois.`,
    telehealth: `Telehealth is available anywhere in Illinois, Monday to Friday. You need to be in Illinois at the time of your visit.`,
    insurance: `We accept ${BE.insurance.join(', ')}. Have another plan or no insurance? Ask us and we'll check your options.`,
    intro: `Everything starts with a free 15-minute intro call by phone: a chance to meet Sariette, ask your questions and see if BrainEase is the right fit. It isn't a psychiatric evaluation yet.`,
    book: `Happy to help. Fill in this short request (under a minute). Sariette aims to reply within one business day.`,
    french: `Yes! Sariette sees patients in English and French, in the office and by telehealth.`,
    ages: `BrainEase sees children, teens and adults, from 8 to 65 years old.`,
    services: `BrainEase offers psychiatric evaluations, medication management guided by genetic testing and lab work, and lifestyle coaching, for anxiety, ADHD, depression and mood disorders, and trauma. To talk about your own situation, the free intro call with Sariette is the right place.`,
    notoffered: `BrainEase doesn't offer couples or marriage therapy, long-term psychotherapy on its own, or emergency care.`,
    contact: `You can call or text ${BE.phone}, or email ${BE.email}. Sariette aims to reply within one business day.`,
    crisis: `If you're in crisis or thinking about harming yourself, please call or text 988 (Suicide & Crisis Lifeline) right now, or call 911. I'm the clinic's assistant and can't help in an emergency.`,
    fallback: `I can only help with practical questions: hours, location, insurance, telehealth or requesting an appointment. For anything else, call or text ${BE.phone} or email ${BE.email}.`,
    sent: n => `Thank you, ${n}. Your request is on its way to Sariette. She aims to get back to you within one business day.`,
    q: [['hours', 'Hours & location'], ['insurance', 'Insurance'], ['intro', 'Free intro call'], ['french', 'Français ?']],
    ph: 'Ask Eze a practical question', foot: 'Eze is an assistant, not a clinician. No health information, please.'
  },
  fr: {
    hi: `Bonjour, je suis Eze, l'assistant de BrainEase. Je réponds aux questions pratiques : horaires, adresse, assurances, télésanté, demande de rendez-vous. Merci de ne pas partager d'informations de santé ici.`,
    hours: `Nous sommes ouverts du lundi au vendredi, de 9 h à 17 h. Les visites au cabinet ont lieu le jeudi à Bolingbrook ; la télésanté couvre tout l'Illinois.`,
    location: `Les visites au cabinet ont lieu le jeudi, au ${BE.address}. La télésanté est possible partout en Illinois.`,
    telehealth: `La télésanté est possible partout en Illinois, du lundi au vendredi. Il faut se trouver en Illinois au moment de la séance.`,
    insurance: `Nous acceptons ${BE.insurance.join(', ')}. Une autre assurance, ou pas d'assurance ? Demandez-nous, nous regardons les options avec vous.`,
    intro: `Tout commence par une consultation d'introduction gratuite de 15 minutes, par téléphone : un moment pour faire connaissance avec Sariette et poser vos questions. Ce n'est pas encore une évaluation psychiatrique.`,
    book: `Avec plaisir. Remplissez cette courte demande (moins d'une minute). Sariette vise une réponse sous un jour ouvré.`,
    french: `Oui ! Sariette reçoit ses patients en anglais et en français, au cabinet comme en télésanté.`,
    ages: `BrainEase reçoit enfants, adolescents et adultes, de 8 à 65 ans.`,
    services: `BrainEase propose des évaluations psychiatriques, une gestion des médicaments guidée par le test génétique et les analyses, et un accompagnement du mode de vie, pour l'anxiété, le TDAH, la dépression et les troubles de l'humeur, et le trauma. Pour parler de votre situation, la consultation gratuite avec Sariette est le bon endroit.`,
    notoffered: `BrainEase ne propose pas de thérapie de couple, de psychothérapie de longue durée seule, ni de soins d'urgence.`,
    contact: `Appelez ou écrivez au ${BE.phone}, ou par e-mail à ${BE.email}. Sariette vise une réponse sous un jour ouvré.`,
    crisis: `Si vous êtes en crise ou pensez à vous faire du mal, appelez ou écrivez au 988 (Suicide & Crisis Lifeline) dès maintenant, ou composez le 911. Je suis l'assistant de la clinique et je ne peux pas aider dans l'urgence.`,
    fallback: `Je ne peux répondre qu'aux questions pratiques : horaires, adresse, assurances, télésanté ou demande de rendez-vous. Pour le reste, appelez ou écrivez au ${BE.phone}, ou à ${BE.email}.`,
    sent: n => `Merci, ${n}. Votre demande est partie chez Sariette. Elle vise une réponse sous un jour ouvré.`,
    q: [['hours', 'Horaires et adresse'], ['insurance', 'Assurances'], ['intro', 'Consultation gratuite'], ['french', 'English?']],
    ph: 'Posez une question pratique à Eze', foot: 'Eze est un assistant, pas un soignant. Pas d’informations de santé, merci.'
  }
};
const CRISIS = /suicid|kill myself|end my life|want to die|hurt myself|harm myself|self[- ]?harm|overdose|emergency|crisis|me tuer|mourir|me faire du mal|urgence|en danger/i;
const INTENTS = [
  ['book', /book|appointment|schedule|reschedul|cancel|rendez|rdv|prendre un/i],
  ['intro', /intro|first (visit|call|step)|free|consult|start|new patient|premi[eè]re|gratuit|commencer/i],
  ['insurance', /insur|bcbs|blue cross|aetna|united|optum|medicaid|bcchp|cigna|humana|pay|cost|price|self-pay|assuranc|prix|tarif|payer/i],
  ['telehealth', /telehealth|online|virtual|video|remote|zoom|t[ée]l[ée]sant|distance|en ligne/i],
  ['location', /where|address|office|location|bolingbrook|thursday|in person|in-person|adresse|cabinet|jeudi|o[uù] /i],
  ['hours', /hour|open|close|time|when|horaire|ouvert|heure|quand/i],
  ['french', /french|fran[cç]ais|parlez|speak|english|anglais|langu/i],
  ['ages', /age|child|kid|teen|son|daughter|adolescent|enfant|ado|fils|fille|adult/i],
  ['notoffered', /couple|marriage|mariage|long[- ]term|longue dur/i],
  ['services', /service|medic|genetic|gene|test|evaluat|lifestyle|adhd|tdah|anxi|depress|trauma|mood|humeur/i],
  ['contact', /phone|call|text|email|e-mail|contact|t[ée]l[ée]phone|appeler|joindre/i]
];
const isFr = s => /[éèàçùêô]|\b(bonjour|merci|vous|je|est-ce|quels?|quelle|comment|pourquoi|avez|acceptez)\b/i.test(s);

const fab = document.createElement('button');
fab.className = 'ezfab'; fab.type = 'button'; fab.setAttribute('aria-expanded', 'false'); fab.setAttribute('aria-controls', 'ezp');
fab.innerHTML = `<span class="av">${avatar}</span>Talk to Eze`;
const panel = document.createElement('section');
panel.className = 'ezp'; panel.id = 'ezp'; panel.setAttribute('aria-label', 'Talk to Eze'); panel.setAttribute('role', 'dialog');
panel.innerHTML = `<header><span class="av">${avatar}</span><div><b>Talk to Eze</b><small>BrainEase assistant · practical answers</small></div><button type="button" aria-label="Close">×</button></header>
<div class="ezlog" aria-live="polite"></div><div class="qrs"></div>
<form class="ezin"><label class="hp" for="ezq">Question</label><input id="ezq" type="text" autocomplete="off" maxlength="300"><button type="submit" aria-label="Send"><svg width="18" height="18" viewBox="0 0 18 18"><path d="M2 9h12M9 3l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button></form>
<p class="ezfoot"></p>`;
document.body.append(fab, panel);
const log = panel.querySelector('.ezlog'), qrs = panel.querySelector('.qrs'), inp = panel.querySelector('#ezq');
let lang = 'en', started = false, history = [];
const add = (cls, text) => { const m = document.createElement('div'); m.className = 'msg ' + cls; m.textContent = text; log.appendChild(m); log.scrollTop = log.scrollHeight; return m; };
const typing = () => { const m = document.createElement('div'); m.className = 'msg bot'; m.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>'; log.appendChild(m); log.scrollTop = log.scrollHeight; return m; };
const say = (text, alert) => new Promise(r => { const t = typing(); setTimeout(() => { t.remove(); add('bot' + (alert ? ' alert' : ''), text); history.push({role: 'assistant', content: text}); r(); }, 650); });
const drawQrs = () => {
  qrs.textContent = '';
  const b = document.createElement('button'); b.type = 'button'; b.className = 'qr go'; b.textContent = lang === 'fr' ? 'Demander un rendez-vous' : 'Request an appointment';
  b.addEventListener('click', () => intent('book', b.textContent)); qrs.appendChild(b);
  T[lang].q.forEach(([k, l]) => {
    const q = document.createElement('button'); q.type = 'button'; q.className = 'qr'; q.textContent = l;
    q.addEventListener('click', () => { if (k === 'french') { lang = lang === 'en' ? 'fr' : 'en'; drawQrs(); intent('french', l); } else intent(k, l); });
    qrs.appendChild(q);
  });
  inp.placeholder = T[lang].ph; panel.querySelector('.ezfoot').textContent = T[lang].foot;
};
const showBooking = () => {
  const card = document.createElement('div'); card.className = 'bk';
  card.innerHTML = bookingHTML(true);
  log.appendChild(card); log.scrollTop = card.offsetTop - 8;
  wireBooking(card, d => { const first = d.name.split(' ')[0]; say(T[lang].sent(first)); });
};
async function intent(k, userText) {
  if (userText) { add('me', userText); history.push({role: 'user', content: userText}); }
  if (k === 'crisis') return say(T[lang].crisis, true);
  await say(T[lang][k] || T[lang].fallback);
  if (k === 'book' || k === 'intro') showBooking();
}
const ask = async text => {
  if (isFr(text)) lang = 'fr'; drawQrs();
  if (CRISIS.test(text)) return intent('crisis', text);
  const hit = INTENTS.find(([, re]) => re.test(text));
  if (BE.chatEndpoint && !(hit && (hit[0] === 'book'))) {
    add('me', text); history.push({role: 'user', content: text});
    const t = typing();
    try {
      const r = await fetch(BE.chatEndpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({lang, messages: history.slice(-10)})});
      const j = await r.json(); t.remove();
      const reply = String(j.reply || T[lang].fallback);
      add('bot', reply); history.push({role: 'assistant', content: reply});
      if (j.action === 'booking') showBooking();
    } catch (e) { t.remove(); await say(hit ? T[lang][hit[0]] : T[lang].fallback); }
    return;
  }
  intent(hit ? hit[0] : 'fallback', text);
};
const openEze = book => {
  panel.classList.add('open'); fab.setAttribute('aria-expanded', 'true');
  if (!started) { started = true; lang = document.documentElement.lang === 'fr' ? 'fr' : 'en'; drawQrs(); say(T[lang].hi).then(() => { if (book) intent('book'); }); }
  else if (book) intent('book');
  setTimeout(() => inp.focus({preventScroll: true}), 300);
};
const closeEze = () => { panel.classList.remove('open'); fab.setAttribute('aria-expanded', 'false'); fab.focus(); };
fab.addEventListener('click', () => openEze(false));
panel.querySelector('header button').addEventListener('click', closeEze);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('open')) closeEze(); });
panel.querySelector('.ezin').addEventListener('submit', e => { e.preventDefault(); const v = inp.value.trim(); if (!v) return; inp.value = ''; ask(v); });
document.querySelectorAll('[data-eze]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); if (drawer && drawer.classList.contains('open')) burger.click(); openEze(b.dataset.eze === 'book'); }));
}

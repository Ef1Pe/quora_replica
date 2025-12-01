const toast = document.querySelector('.toast');

/**
 * Display a lightweight toast message used across the replica.
 */
function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.classList.remove('hidden');
  requestAnimationFrame(() => toast.classList.add('show'));

  clearTimeout(showToast.timeout);
  showToast.timeout = setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.classList.add('hidden'), 250);
  }, 2600);
}

function wireLoginForm() {
  const form = document.querySelector('[data-login-form]');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const email = formData.get('email') || formData.get('Email') || 'user';
    showToast(`Welcome back, ${email}!`);
  });
}

function wireOAuthButtons() {
  document.querySelectorAll('[data-mock-oauth]').forEach((button) => {
    button.addEventListener('click', () => {
      const provider = button.dataset.mockOauth;
      showToast(`${provider} sign in is ready for API hookup.`);
    });
  });
}

const FEED_DATA = [
  {
    section: 'home',
    topic: 'Technology',
    author: 'Aparna Patel · Product @ DeepVision',
    question: 'What quiet AI breakthroughs are founders sleeping on in 2025?',
    answer:
      'Bounded-context copilots are quietly becoming the new default dev stack. Teams ship custom copilots to every internal tool rather than a single chat box. It keeps data local while still tapping frontier models.',
    stats: {
      views: '142k views',
      upvotes: '3.9k upvotes',
      shares: '132 shares',
    },
  },
  {
    section: 'spaces',
    topic: 'Spaces',
    author: 'Curated by Systems Thinking',
    question: 'This week in Systems Thinking',
    answer:
      'How Southwest Airlines rewired ops after the 2022 meltdown, plus a teardown on how grocery dark stores coordinate with EV fleets.',
    stats: {
      views: '68k readers',
      upvotes: 'Top space',
      shares: '28 highlights',
    },
  },
  {
    section: 'answers',
    topic: 'Career Advice',
    author: 'Sid Kapur · YC alum',
    question: 'My Series B startup paused raises—how do I keep morale high?',
    answer:
      'Narrate the plan every Monday. Show the 3 metrics that matter, make every meeting public, and over-index on customer calls. Teams stay when they feel the scoreboard, not when you slack “stay calm.”',
    stats: {
      views: '34k views',
      upvotes: '2.3k upvotes',
      shares: '76 reshares',
    },
  },
  {
    section: 'notifications',
    topic: 'Notifications',
    author: 'Digest',
    question: 'Your answers from last week are trending in Spain',
    answer:
      'Upvotes are spiking across two Spanish translations. Tip: toggle “Auto translate answers” inside settings to keep momentum.',
    stats: {
      views: 'Global reach',
      upvotes: 'Mixed languages',
      shares: '7 invites',
    },
  },
  {
    section: 'profile',
    topic: 'Profile',
    author: 'You',
    question: 'Draft answer · How will AI re-shape local politics?',
    answer:
      'Save your notes here. This card doubles as a creative scratchpad where injected data can turn drafts into polished takes.',
    stats: {
      views: 'Private',
      upvotes: 'Not yet published',
      shares: '—',
    },
  },
];

const SIDEBAR_DATA = [
  {
    title: 'Trending Spaces',
    pills: ['Applied AI Daily', 'Gen Z Finance', 'Design Systems Lab', 'Future of Cities'],
  },
  {
    title: 'Suggested Topics',
    pills: ['Quantum Hardware', 'Creator Economy', 'Healthtech', 'Global Supply Chains'],
  },
  {
    title: 'Quick Actions',
    pills: ['Draft answer', 'Create space', 'Host session'],
  },
];

function renderFeed(section) {
  const feed = document.querySelector('.dynamic-feed');
  if (!feed || feed.children.length) return;

  const cards = FEED_DATA.filter((item) => item.section === section || section === 'home').map(
    (item) => {
      return `
        <article class="feed-card">
          <div class="feed-card__meta">${item.topic} · ${item.author}</div>
          <h2 class="feed-card__question">${item.question}</h2>
          <p class="feed-card__answer">
            ${item.answer}
          </p>
          <div class="feed-card__footer">
            <span>${item.stats.views}</span>
            <span>${item.stats.upvotes}</span>
            <span>${item.stats.shares}</span>
          </div>
        </article>
      `;
    }
  );

  feed.innerHTML = cards.join('');
}

function renderSidebar() {
  const sidebar = document.querySelector('.sidebar-widgets');
  if (!sidebar || sidebar.children.length) return;

  const widgets = SIDEBAR_DATA.map((widget) => {
    const pills = widget.pills
      .map((pill) => `<span class="widget-pill">${pill}</span>`)
      .join('');
    return `
      <section class="widget-card">
        <h3>${widget.title}</h3>
        <div>${pills}</div>
      </section>
    `;
  });

  sidebar.innerHTML = widgets.join('');
}

document.addEventListener('DOMContentLoaded', () => {
  wireLoginForm();
  wireOAuthButtons();

  const section = document.body.dataset.section || 'home';
  renderFeed(section);
  renderSidebar();
});

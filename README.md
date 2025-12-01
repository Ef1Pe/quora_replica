# Quora Replica

Pixel-perfect recreation of the Quora onboarding/login page plus signed-in experience mock, powered by a Flask backend that supports dynamic content injection for experiments.

## Project Structure

```
.
├── index.html                 # Landing + login experience
├── home.html                  # Feed shell (page 1/5)
├── spaces.html                # Feed shell (page 2/5)
├── answers.html               # Feed shell (page 3/5)
├── notifications.html         # Feed shell (page 4/5)
├── profile.html               # Feed shell (page 5/5)
├── css/styles.css             # Tailwind-friendly custom styles
├── js/main.js                 # Mock data + interactions
├── images/quora-favicon.svg   # Replica favicon
├── server.py                  # Flask server + injection hooks
├── metadata.py                # Agenticverse metadata schema
├── entity.py                  # Entity entry point
├── site_analysis.yaml         # Color / layout reference
└── requirements.txt
```

## Tech Stack

- **HTML5 + Tailwind CDN** for structure and utility spacing
- **Custom CSS** to recreate Quora-specific visuals (wordmark, OAuth buttons, illustrated backdrop)
- **Vanilla JS** for toast notifications, mock feed rendering, and data placeholders
- **Flask** backend with injection helpers mirroring the Agenticverse template

## Running the Replica

1. Install dependencies (ideally within a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask server:

   ```bash
   python server.py
   ```

   The helper inside `server.py` uses `agenticverse_entities.base.server_base.start_server`. If you run outside Agenticverse, replace that import with `app.run(...)`.

3. Visit `http://localhost:5000` to view the login page. Navigate to `/home.html`, `/spaces.html`, etc., for the signed-in shells.

## Dynamic Content Injection

- `metadata.py` defines the contract for runtime data. Key fields: `section`, `placement` (`feed_primary`, `sidebar_callouts`, `auth_card`), plus text content, stats, badges, and optional tags.
- `server.py` stores injected payloads in-memory (`injected_content`) and merges them into HTML before returning each page.
- `js/main.js` only hydrates default mock content if the DOM node is empty, so server-injected HTML stays intact.

### Example Payload

```json
{
  "section": "home",
  "placement": "feed_primary",
  "title": "AI Writer AMA",
  "question": "Ask us anything about frontier models",
  "author": "Quora + Anthropic",
  "stat_one": "Live today",
  "stat_two": "Limited seats",
  "stat_three": "Sponsored",
  "badge_text": "Featured"
}
```

## Key Features

- Auth card mirroring the current Quora login (Google, Facebook, email, password form, legal text, footer)
- Full-bleed illustrated background recreated with layered gradients for medium-fidelity parity
- Five continuous internal pages with shared navigation, responsive layout, and CTA buttons
- Mock notice system via toasts and interactive buttons ready for API integration
- Agenticverse-ready backend with metadata schema and entity definition

## Known Limitations

- Illustrations use procedural gradients instead of the exact SVG artwork from quora.com.
- OAuth buttons trigger informative toasts rather than performing real authentication.
- Dynamic injections persist only for the lifetime of the Python process (no database).

## Next Steps

- Wire up a persistence layer (Redis/Postgres) for injected experiences.
- Expand `js/main.js` with actual API calls once available.
- Add automated tests or visual regression snapshots if required.

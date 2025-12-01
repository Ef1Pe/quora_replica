"""Flask server for the Quora replica with dynamic content injection."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, Response, send_from_directory

BASE_DIR = Path(__file__).parent
PAGES = {
    "index": "index.html",
    "home": "home.html",
    "spaces": "spaces.html",
    "answers": "answers.html",
    "notifications": "notifications.html",
    "profile": "profile.html",
}

PLACEMENT_MARKERS = {
    "feed_primary": '<div class="dynamic-feed"',
    "sidebar_callouts": '<aside class="sidebar-widgets"',
    "auth_card": '<div class="auth-card__inner"',
}

injected_content: List[Dict[str, Any]] = []


def build_feed_card(item: Dict[str, Any]) -> str:
    badge = (
        f'<span class="widget-pill" style="background:rgba(185,43,39,0.12);color:#b92b27;">'
        f"{escape(str(item.get('badge_text', '')))}</span>"
        if item.get("badge_text")
        else ""
    )
    return f"""
    <!-- injected feed card -->
    <article class="feed-card injected">
        <div class="feed-card__meta">{escape(item.get('topic', 'Injected spotlight'))} · {escape(item.get('author', 'Editorial Team'))}</div>
        <h2 class="feed-card__question">{escape(item.get('question', item.get('title', 'New drop on Quora')))}</h2>
        <p class="feed-card__answer">{escape(item.get('answer', item.get('description', 'Fresh content supplied via metadata.')))}</p>
        <div class="feed-card__footer">
            <span>{escape(item.get('stat_one', 'Live now'))}</span>
            <span>{escape(item.get('stat_two', 'Featured'))}</span>
            <span>{escape(item.get('stat_three', 'Sponsored'))}</span>
        </div>
        {badge}
    </article>
    """


def build_sidebar_card(item: Dict[str, Any]) -> str:
    pills = item.get("tags") or []
    pills_markup = "".join(f'<span class="widget-pill">{escape(str(tag))}</span>' for tag in pills)
    return f"""
    <!-- injected sidebar widget -->
    <section class="widget-card injected">
        <h3>{escape(item.get('title', 'Quick spotlight'))}</h3>
        <p class="text-sm" style="color:#636466;margin-bottom:.75rem;">
            {escape(item.get('description', 'Fresh metadata is ready to go.'))}
        </p>
        <div>{pills_markup}</div>
    </section>
    """


def build_auth_insert(item: Dict[str, Any]) -> str:
    return f"""
    <!-- injected auth band -->
    <div class="injected-auth-panel" style="grid-column: span 2; margin-top: 1.5rem; background:#f7f5ef;border-radius:18px;padding:1.25rem 1.5rem;border:1px solid #ede4d6;">
        <p style="font-weight:600;color:#b92b27;margin:0 0 .35rem;">{escape(item.get('title', 'Limited beta'))}</p>
        <p style="margin:0;color:#5f4438;">{escape(item.get('description', 'Use metadata injection to promote onboarding experiments.'))}</p>
    </div>
    """


def build_fragment(item: Dict[str, Any], placement: str) -> str:
    if placement == "sidebar_callouts":
        return build_sidebar_card(item)
    if placement == "auth_card":
        return build_auth_insert(item)
    return build_feed_card(item)


def inject_fragment(html_content: str, marker: str, fragment: str) -> str:
    index = html_content.find(marker)
    if index == -1:
        return html_content

    close_index = html_content.find(">", index)
    if close_index == -1:
        return html_content

    insert_position = close_index + 1
    return html_content[:insert_position] + fragment + html_content[insert_position:]


def apply_injections(html_content: str, section: str) -> str:
    updated = html_content
    for item in injected_content:
        target_section = item.get("section", "home")
        if target_section not in (section, "global"):
            continue

        placement = item.get("placement", "feed_primary")
        marker = PLACEMENT_MARKERS.get(placement)
        if not marker:
            continue
        updated = inject_fragment(updated, marker, build_fragment(item, placement))
    return updated


def render_page(page_key: str) -> Response | str:
    filename = PAGES.get(page_key)
    if not filename:
        return "Page not found", 404

    html_path = BASE_DIR / filename
    if not html_path.exists():
        return "Page not found", 404

    html_content = html_path.read_text(encoding="utf-8")
    section = "auth" if page_key == "index" else page_key
    return apply_injections(html_content, section)


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)

    @app.route("/")
    @app.route("/index.html")
    def index_route():
        return render_page("index")

    @app.route("/home.html")
    def home_route():
        return render_page("home")

    @app.route("/spaces.html")
    def spaces_route():
        return render_page("spaces")

    @app.route("/answers.html")
    def answers_route():
        return render_page("answers")

    @app.route("/notifications.html")
    def notifications_route():
        return render_page("notifications")

    @app.route("/profile.html")
    def profile_route():
        return render_page("profile")

    @app.route("/css/<path:filename>")
    def css_files(filename: str):
        return send_from_directory(BASE_DIR / "css", filename)

    @app.route("/js/<path:filename>")
    def js_files(filename: str):
        return send_from_directory(BASE_DIR / "js", filename)

    @app.route("/images/<path:filename>")
    def image_files(filename: str):
        return send_from_directory(BASE_DIR / "images", filename)

    return app


def start_server(port: int = 5000, threaded: bool = False, content_data: Dict[str, Any] | None = None):
    """
    Public entry point used by the entity runner.
    """

    if content_data and content_data.get("title"):
        injected_content.append(content_data)
        print(
            f"[Quora Replica] Injected '{content_data['title']}' "
            f"into section '{content_data.get('section', 'home')}'."
        )

    app = create_app()
    from agenticverse_entities.base.server_base import start_server as start_base_server

    return start_base_server(app, port=port, threaded=threaded)

"""Seed an Outlook inbox with demo emails via Playwright (headed Chromium).

All emails are sent FROM the logged-in account TO advise.assist@outlook.com,
so they land back in that same inbox. Login / 2FA is done manually by you.

Usage:
    python browser_seed.py
"""

import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

from fake_emails import FAKE_EMAILS

RECIPIENT = "advise.assist@outlook.com"
OUTLOOK_URL = "https://outlook.office.com/mail/"
PROFILE_DIR = Path(__file__).parent / ".outlook_profile"
SHOT_DIR = Path(__file__).parent / "screenshots"


def shot(page, name):
    """Save a screenshot and return its path (for debugging broken selectors)."""
    SHOT_DIR.mkdir(exist_ok=True)
    path = SHOT_DIR / f"{name}.png"
    try:
        page.screenshot(path=str(path), full_page=False)
    except Exception as exc:  # pragma: no cover - best effort
        print(f"  (could not save screenshot: {exc})")
        return None
    return path


def dump_fields(page):
    """Print accessible names/labels of likely compose fields, for debugging."""
    try:
        info = page.evaluate(
            """() => {
                const els = Array.from(document.querySelectorAll(
                    '[role=textbox],[role=combobox],input,textarea,[contenteditable=true]'));
                return els.slice(0, 40).map(e => ({
                    tag: e.tagName.toLowerCase(),
                    role: e.getAttribute('role'),
                    label: e.getAttribute('aria-label'),
                    placeholder: e.getAttribute('placeholder'),
                    id: e.id || null,
                }));
            }"""
        )
        print("  --- editable elements currently on the page ---")
        for f in info:
            print(f"   {f}")
        print("  ----------------------------------------------")
    except Exception as exc:
        print(f"  (could not dump fields: {exc})")


def first_working(page, candidates, *, timeout=8000):
    """Return the first locator (from candidates) that becomes visible.

    `candidates` is a list of (description, locator) tuples. Raises RuntimeError
    listing everything tried if none appear.
    """
    deadline = time.time() + timeout / 1000
    tried = [desc for desc, _ in candidates]
    while time.time() < deadline:
        for _desc, locator in candidates:
            try:
                loc = locator.first
                if loc.count() > 0 and loc.is_visible():
                    return loc
            except Exception:
                continue
        page.wait_for_timeout(250)
    raise RuntimeError("none of these selectors matched: " + " | ".join(tried))


def _new_mail_visible(page):
    try:
        return new_mail_button(page, timeout=1500).is_visible()
    except Exception:
        return False


def wait_for_login(page):
    """Pause for manual login. Uses Enter in a TTY, else auto-detects the inbox."""
    print("Log in to Outlook in the browser, then press Enter here...")
    if sys.stdin.isatty():
        input()
    else:
        # No interactive stdin (e.g. launched by an agent): poll until the
        # inbox UI ("New mail" button) appears. Wait up to 12 minutes and drop
        # a screenshot every 30s so progress can be inspected live.
        print("  (no interactive terminal detected -- polling up to 30 min for "
              "the inbox to load; screenshots saved to ./screenshots)")
        deadline = time.time() + 30 * 60
        last_shot = 0
        while time.time() < deadline:
            if _new_mail_visible(page):
                print("  inbox detected -- starting to send.")
                break
            if time.time() - last_shot > 30:
                p = shot(page, "login_wait")
                print(f"  still waiting for login... (snapshot: {p})")
                last_shot = time.time()
            page.wait_for_timeout(2000)
        else:
            shot(page, "login_timeout")
            raise RuntimeError(
                "inbox never appeared. Check ./screenshots/login_timeout.png -- "
                "tell me what's on screen (login page? different inbox layout?)")
    # Give the inbox a moment to settle after login.
    page.wait_for_timeout(2000)


def new_mail_button(page, timeout=8000):
    return first_working(page, [
        ("role=button name=New mail",
         page.get_by_role("button", name=re.compile(r"new mail", re.I))),
        ("role=menuitem name=New mail",
         page.get_by_role("menuitem", name=re.compile(r"new mail", re.I))),
        ("text=New mail", page.get_by_text(re.compile(r"^new mail", re.I))),
    ], timeout=timeout)


def fill_recipient(page):
    field = first_working(page, [
        ("role=combobox name=To (exact)",
         page.get_by_role("combobox", name="To", exact=True)),
        ("role=textbox name=To (exact)",
         page.get_by_role("textbox", name="To", exact=True)),
        ("placeholder To",
         page.get_by_placeholder(re.compile(r"^to$", re.I))),
        ("aria-label exactly To",
         page.locator('[aria-label="To"]')),
    ])
    field.click()
    field.type(RECIPIENT, delay=20)
    page.wait_for_timeout(800)
    # Commit the recipient into a pill.
    field.press("Enter")
    page.wait_for_timeout(400)


def fill_subject(page, subject):
    field = first_working(page, [
        ("placeholder Add a subject",
         page.get_by_placeholder(re.compile(r"add a subject", re.I))),
        ("role=textbox name=Subject (exact)",
         page.get_by_role("textbox", name="Subject", exact=True)),
        ("aria-label exactly Subject",
         page.locator('[aria-label="Subject"]')),
        ("input id subjectLine", page.locator('input[id*="subject" i]')),
    ])
    field.click()
    field.fill(subject)


def fill_body(page, body):
    field = first_working(page, [
        ("role=textbox name=Message body",
         page.get_by_role("textbox", name=re.compile(r"^message body$", re.I))),
        ("aria-label Message body",
         page.locator('[aria-label="Message body, press Alt+F10 to exit"], '
                      '[aria-label="Message body"]')),
        ("contenteditable in compose",
         page.locator('div[contenteditable="true"][role="textbox"]')),
    ])
    field.click()
    field.type(body, delay=2)


def click_send(page):
    btn = first_working(page, [
        ("role=button name=Send",
         page.get_by_role("button", name=re.compile(r"^send$", re.I))),
        ("aria-label Send", page.locator('[aria-label="Send"]')),
        ("text=Send", page.get_by_text(re.compile(r"^send$", re.I))),
    ])
    btn.click()


def send_one(page, idx, total, email):
    label = f"{idx}/{total}: {email['subject']}"
    new_mail_button(page).click()
    page.wait_for_timeout(1500)  # compose pane animation
    fill_recipient(page)
    fill_subject(page, email["subject"])
    fill_body(page, email["body"])
    page.wait_for_timeout(400)
    click_send(page)
    print(f"sent {label}")


def main():
    total = len(FAKE_EMAILS)
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            args=["--start-maximized"],
            no_viewport=True,
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(OUTLOOK_URL, wait_until="domcontentloaded")

        wait_for_login(page)

        sent = 0
        for idx, email in enumerate(FAKE_EMAILS, start=1):
            try:
                send_one(page, idx, total, email)
                sent += 1
                time.sleep(2)
            except Exception as exc:
                name = f"fail_{idx:02d}"
                path = shot(page, name)
                print("\n" + "=" * 70)
                print(f"BROKE on email {idx}/{total}: {email['subject']!r}")
                print(f"  reason: {type(exc).__name__}: {exc}")
                if path:
                    print(f"  screenshot: {path}")
                dump_fields(page)
                print("  The Outlook compose selectors may have shifted. The "
                      "screenshot + field dump above show the actual labels so "
                      "I can adjust the selectors.")
                print("=" * 70 + "\n")
                break

        print(f"\nDone. Sent {sent}/{total} emails to {RECIPIENT}.")
        print("Leaving the browser open for 10s so you can verify...")
        page.wait_for_timeout(10000)
        context.close()


if __name__ == "__main__":
    main()

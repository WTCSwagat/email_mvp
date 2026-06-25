"""Clear the Outlook inbox and re-seed it from fake_emails.py.

All emails are sent FROM and TO advise.assist@outlook.com so they land in the
inbox. Login / 2FA is manual.

Usage:
    python reseed_inbox.py
"""

import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from fake_emails import FAKE_EMAILS

RECIPIENT = "advise.assist@outlook.com"
OUTLOOK_URL = "https://outlook.office.com/mail/"
PROFILE_DIR = Path(__file__).parent / ".outlook_profile"
SHOT_DIR = Path(__file__).parent / "screenshots"


def shot(page, name):
  SHOT_DIR.mkdir(exist_ok=True)
  path = SHOT_DIR / f"{name}.png"
  try:
    page.screenshot(path=str(path), full_page=False)
  except Exception as exc:
    print(f"  (could not save screenshot: {exc})")
    return None
  return path


def dump_fields(page):
  try:
    info = page.evaluate(
      """() => {
          const els = Array.from(document.querySelectorAll(
              '[role=textbox],[role=combobox],input,textarea,[contenteditable=true],'
              + '[role=button],[role=checkbox],[role=treeitem],[role=option]'));
          return els.slice(0, 50).map(e => ({
              tag: e.tagName.toLowerCase(),
              role: e.getAttribute('role'),
              label: e.getAttribute('aria-label'),
              placeholder: e.getAttribute('placeholder'),
              text: (e.innerText || '').slice(0, 60),
          }));
      }"""
    )
    print("  --- visible controls on the page ---")
    for f in info:
      print(f"   {f}")
    print("  ------------------------------------")
  except Exception as exc:
    print(f"  (could not dump fields: {exc})")


def first_working(page, candidates, *, timeout=8000):
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


def inbox_ready(page):
  try:
    return new_mail_button(page, timeout=1500).is_visible()
  except Exception:
    return False


def wait_for_login(page):
  print("Log in to Outlook, then press Enter here...")
  if sys.stdin.isatty():
    input()
  else:
    print("  (no interactive terminal -- polling up to 30 min for inbox; "
          "screenshots in ./screenshots)")
    deadline = time.time() + 30 * 60
    last_shot = 0
    while time.time() < deadline:
      if inbox_ready(page):
        print("  inbox detected.")
        break
      if time.time() - last_shot > 30:
        p = shot(page, "login_wait")
        print(f"  still waiting for login... (snapshot: {p})")
        last_shot = time.time()
      page.wait_for_timeout(2000)
    else:
      shot(page, "login_timeout")
      raise RuntimeError(
        "inbox never appeared. See ./screenshots/login_timeout.png")
  page.wait_for_timeout(2000)


def go_to_inbox(page):
  first_working(page, [
    ("treeitem Inbox",
     page.get_by_role("treeitem", name=re.compile(r"^inbox\b", re.I))),
    ("link Inbox", page.get_by_role("link", name=re.compile(r"^inbox\b", re.I))),
    ("text Inbox", page.get_by_text(re.compile(r"^inbox$", re.I))),
  ], timeout=10000).click()
  page.wait_for_timeout(1500)


def message_list(page):
  return first_working(page, [
    ("listbox message list",
     page.get_by_role("listbox", name=re.compile(r"message list|conversation", re.I))),
    ("region message list",
     page.get_by_role("region", name=re.compile(r"message list|conversation", re.I))),
    ("listbox generic",
     page.locator('[role="listbox"]').filter(
       has=page.locator('[role="option"], [role="listitem"]'))),
  ], timeout=3000)


def message_rows(page):
  rows = page.locator(
    '[role="option"][aria-label*="Collapsed" i], '
    '[role="option"][aria-label*="Unread" i], '
    '[role="option"][aria-label*="Expanded" i]'
  )
  if rows.count() > 0:
    return rows
  try:
    lst = message_list(page)
    return lst.locator('[role="option"], [role="listitem"]')
  except Exception:
    return page.locator('[role="option"]')


def count_messages(page):
  try:
    return message_rows(page).count()
  except Exception:
    return -1


def inbox_empty(page):
  try:
    page_text = (page.locator("body").inner_text(timeout=3000) or "").lower()
    if any(p in page_text for p in (
      "enjoy your empty inbox",
      "all done for the day",
      "your inbox is empty",
      "no messages",
      "we didn't find anything",
    )):
      return True
  except Exception:
    pass

  n = count_messages(page)
  if n == 0:
    return True
  if n < 0:
    return message_rows(page).count() == 0
  return False


def delete_button(page):
  return first_working(page, [
    ("button Delete",
     page.get_by_role("button", name=re.compile(r"^delete$", re.I))),
    ("button Delete message",
     page.get_by_role("button", name=re.compile(r"delete message", re.I))),
    ("aria-label Delete",
     page.locator('[aria-label="Delete"]')),
  ], timeout=5000)


def select_all_messages(page):
  first_working(page, [
    ("checkbox Select all messages",
     page.get_by_role("checkbox", name=re.compile(
       r"select all messages", re.I))),
    ("checkbox Select all",
     page.get_by_role("checkbox", name=re.compile(r"^select all$", re.I))),
    ("aria-label Select all",
     page.locator('[aria-label*="Select all" i]')),
  ], timeout=5000).click()
  page.wait_for_timeout(500)


def delete_selected(page):
  delete_button(page).click()
  page.wait_for_timeout(1200)


def delete_one_message(page):
  rows = message_rows(page)
  if rows.count() == 0:
    raise RuntimeError("no messages left to delete")
  rows.first.click()
  page.wait_for_timeout(400)
  delete_selected(page)


def clear_inbox(page):
  go_to_inbox(page)
  deleted = 0
  max_rounds = 200

  for _ in range(max_rounds):
    if inbox_empty(page):
      break

    before = count_messages(page)
    if before <= 0:
      break

    try:
      select_all_messages(page)
      delete_selected(page)
      page.wait_for_timeout(1500)
      after = count_messages(page)
      removed = max(before - after, 1) if after >= 0 else before
      deleted += removed
      print(f"deleted {removed} old message(s) (batch)")
      if after == before:
        raise RuntimeError("select-all delete did not remove messages")
      continue
    except Exception:
      pass

    # Fallback: delete one at a time.
    try:
      delete_one_message(page)
      deleted += 1
      print(f"deleted 1 old message (one-by-one, total {deleted})")
    except RuntimeError as exc:
      if "no messages left" in str(exc).lower() or inbox_empty(page):
        break
      shot(page, "clear_inbox_fail")
      raise RuntimeError(f"could not delete messages: {exc}") from exc
    except Exception as exc:
      if inbox_empty(page):
        break
      shot(page, "clear_inbox_fail")
      raise RuntimeError(f"could not delete messages: {exc}") from exc

  if not inbox_empty(page):
    shot(page, "inbox_not_empty")
    remaining = count_messages(page)
    raise RuntimeError(
      f"inbox still has ~{remaining} message(s) after clearing. "
      "See ./screenshots/inbox_not_empty.png")

  print(f"inbox cleared ({deleted} message(s) deleted)")
  return deleted


def new_mail_button(page, timeout=8000):
  return first_working(page, [
    ("button New mail",
     page.get_by_role("button", name=re.compile(r"new mail", re.I))),
    ("menuitem New mail",
     page.get_by_role("menuitem", name=re.compile(r"new mail", re.I))),
    ("text New mail",
     page.get_by_text(re.compile(r"^new mail", re.I))),
  ], timeout=timeout)


def fill_recipient(page):
  field = first_working(page, [
    ("combobox To",
     page.get_by_role("combobox", name="To", exact=True)),
    ("textbox To",
     page.get_by_role("textbox", name="To", exact=True)),
    ("placeholder To",
     page.get_by_placeholder(re.compile(r"^to$", re.I))),
    ("aria-label To",
     page.locator('[aria-label="To"]')),
  ])
  field.click()
  field.fill(RECIPIENT)
  page.wait_for_timeout(600)
  field.press("Enter")
  page.wait_for_timeout(400)


def fill_subject(page, subject):
  field = first_working(page, [
    ("placeholder Add a subject",
     page.get_by_placeholder(re.compile(r"add a subject", re.I))),
    ("textbox Subject",
     page.get_by_role("textbox", name="Subject", exact=True)),
    ("aria-label Subject",
     page.locator('[aria-label="Subject"]')),
  ])
  field.click()
  field.fill(subject)


def fill_body(page, body):
  field = first_working(page, [
    ("textbox Message body",
     page.get_by_role("textbox", name=re.compile(r"^message body$", re.I))),
    ("aria-label Message body",
     page.locator('[aria-label="Message body, press Alt+F10 to exit"], '
                  '[aria-label="Message body"]')),
    ("contenteditable compose",
     page.locator('div[contenteditable="true"][role="textbox"]')),
  ])
  field.click()
  field.fill(body)


def click_send(page):
  first_working(page, [
    ("button Send",
     page.get_by_role("button", name=re.compile(r"^send$", re.I))),
    ("aria-label Send",
     page.locator('[aria-label="Send"]')),
  ]).click()


def close_stale_compose(page):
  """Dismiss open compose/draft panes before starting a new message."""
  page.keyboard.press("Escape")
  page.wait_for_timeout(300)
  for tab in page.locator('[role="tablist"] [role="tab"]').all():
    try:
      label = (tab.get_attribute("aria-label") or tab.inner_text() or "").lower()
      if "inbox" in label or "focused" in label:
        continue
      close = tab.locator(
        'button[aria-label="Close" i], button[aria-label*="Close compose" i]'
      )
      if close.count() and close.first.is_visible():
        close.first.click()
        page.wait_for_timeout(200)
    except Exception:
      pass
  page.wait_for_timeout(400)


def wait_for_compose(page, timeout=15000):
  first_working(page, [
    ("combobox To",
     page.get_by_role("combobox", name="To", exact=True)),
    ("textbox To",
     page.get_by_role("textbox", name="To", exact=True)),
    ("placeholder Add a subject",
     page.get_by_placeholder(re.compile(r"add a subject", re.I))),
    ("aria-label To",
     page.locator('[aria-label="To"]')),
  ], timeout=timeout)


def send_one(page, idx, total, email):
  close_stale_compose(page)
  new_mail_button(page).click()
  wait_for_compose(page)
  page.wait_for_timeout(800)
  fill_recipient(page)
  fill_subject(page, email["subject"])
  fill_body(page, email["body"])
  page.wait_for_timeout(400)
  click_send(page)
  page.wait_for_timeout(1500)  # let compose close before the next one
  print(f"sent {idx}/{total}: {email['subject']}")


def fail(page, phase, detail, exc):
  path = shot(page, f"fail_{phase}")
  print("\n" + "=" * 70)
  print(f"BROKE during {phase}: {detail}")
  print(f"  reason: {type(exc).__name__}: {exc}")
  if path:
    print(f"  screenshot: {path}")
  dump_fields(page)
  print("=" * 70 + "\n")


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

    # Phase 1 — clear inbox
    print("\n--- Phase 1: clear inbox ---")
    try:
      deleted = clear_inbox(page)
    except Exception as exc:
      fail(page, "clear_inbox", "could not empty the inbox", exc)
      context.close()
      sys.exit(1)

    # Phase 2 — send current fake_emails.py set
    print("\n--- Phase 2: send emails ---")
    sent = 0
    for idx, email in enumerate(FAKE_EMAILS, start=1):
      try:
        send_one(page, idx, total, email)
        sent += 1
        time.sleep(2)
      except Exception as exc:
        fail(page, "send", f"email {idx}/{total}: {email['subject']!r}", exc)
        break

    print(f"\nDone. Deleted {deleted} old message(s), sent {sent}/{total} "
          f"to {RECIPIENT}.")
    print("Leaving the browser open for 10s so you can verify...")
    page.wait_for_timeout(10000)
    context.close()


if __name__ == "__main__":
  main()

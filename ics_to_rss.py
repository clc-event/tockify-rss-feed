#!/usr/bin/env python3
"""Fetch a Tockify ICS feed and convert it to an RSS 2.0 feed."""
import sys
import re
import html
import urllib.request
from datetime import datetime, timezone
from email.utils import format_datetime

ICS_URL = "https://tockify.com/api/feeds/ics/evenements.la.cite"
CALENDAR_PAGE_URL = "hhttps://www.collegelacite.ca/evenements"


def fetch_ics(url):
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def unfold(raw_text):
    lines = raw_text.replace("\r\n", "\n").split("\n")
    unfolded = []
    for line in lines:
        if line.startswith((" ", "\t")) and unfolded:
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)
    return unfolded


def unescape_ics(value):
    return (value.replace("\\n", "\n").replace("\\N", "\n")
                 .replace("\\,", ",").replace("\\;", ";").replace("\\\\", "\\"))


def parse_events(lines):
    events = []
    current = None
    for line in lines:
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT":
            if current is not None:
                events.append(current)
            current = None
        elif current is not None and ":" in line:
            key_part, value = line.split(":", 1)
            key = key_part.split(";")[0]
            current[key] = unescape_ics(value)
    return events


def parse_dt(value):
    value = value.rstrip("Z")
    dt = datetime.strptime(value, "%Y%m%dT%H%M%S")
    return dt.replace(tzinfo=timezone.utc)


def xml_escape(text):
    return html.escape(text, quote=False)


def build_rss(calname, events):
    now = format_datetime(datetime.now(timezone.utc))
    items = []
    for ev in events:
        title = ev.get("SUMMARY", "").strip()
        link = ev.get("URL", "").strip()
        desc = ev.get("DESCRIPTION", "").strip()
        location = ev.get("LOCATION", "").strip()
        dtstart = ev.get("DTSTART")
        pubdate = format_datetime(parse_dt(dtstart)) if dtstart else now
        guid = ev.get("UID", link)

        body = desc
        if location:
            body += f"\n\nLieu: {location}"

        items.append(f"""    <item>
      <title>{xml_escape(title)}</title>
      <link>{xml_escape(link)}</link>
      <guid isPermaLink="false">{xml_escape(guid)}</guid>
      <pubDate>{pubdate}</pubDate>
      <description>{xml_escape(body)}</description>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="feed.xsl"?>
<rss version="2.0">
  <channel>
    <title>{xml_escape(calname)}</title>
    <link>{CALENDAR_PAGE_URL}</link>
    <description>Flux RSS des Événements de La Cite</description>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "rss.xml"

    raw = fetch_ics(ICS_URL)
    lines = unfold(raw)
    calname_match = re.search(r"^X-WR-CALNAME:(.*)$", raw, re.MULTILINE)
    calname = unescape_ics(calname_match.group(1).strip()) if calname_match else "Calendar Feed"

    events = parse_events(lines)
    events.sort(key=lambda e: e.get("DTSTART", ""))

    rss = build_rss(calname, events)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"Wrote {len(events)} items to {out_path}")


if __name__ == "__main__":
    main()

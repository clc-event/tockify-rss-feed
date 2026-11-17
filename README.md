Tockify ICS to RSS
A small Python script that fetches a Tockify calendar's ICS feed and converts it into an RSS 2.0 feed. Built for the Collège La Cité events calendar, but works with any Tockify (or generic ICS) feed by changing the URL.

What it does

Downloads the ICS feed from ICS_URL.

Un-folds ICS line continuations and parses each VEVENT block.

Filters out events that have already ended (keeps all-day and timed events that are still upcoming).

Sorts the remaining events by start date.

Writes an RSS 2.0 XML file with a title, link, GUID, publish date, categories, and a description (including location, when present) for each event.

Requirements

Python 3.7+

No third-party dependencies — only the standard library (urllib, html, re, datetime, email.utils).
Usage

python3 tockify_ics_to_rss.py [output_file]

output_file is optional and defaults to rss.xml in the current directory.

Example:

python3 tockify_ics_to_rss.py events_feed.xml
On success, it prints how many upcoming items were written:

Wrote 12 upcoming items to rss.xml

Configuration

Edit the constants near the top of the script to point at a different calendar:

Constant	Purpose

ICS_URL	The Tockify (or other) ICS feed URL to fetch.
CALENDAR_PAGE_URL	The human-facing calendar page linked from the RSS <channel>.
Notes
The generated feed references an XSL stylesheet (feed.xsl) via <?xml-stylesheet?> for optional browser-side styling. If you don't have a feed.xsl alongside the output file, this is simply ignored — it's only used when the XML is opened directly in a browser.
The RSS <description> field is plain text (HTML-escaped), not HTML markup.
To automate publishing (e.g., regenerate on a schedule and upload somewhere), wrap this script in a cron job or CI workflow that runs it and deploys the resulting XML file.
License
No license specified — add one if you plan to share or publish this script.

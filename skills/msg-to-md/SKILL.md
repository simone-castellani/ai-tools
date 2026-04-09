---
name: msg-to-md
description: |
  Convert Microsoft Outlook .msg files into a Markdown document that preserves
  important metadata (Subject, From, To, Cc, Date, Message-ID), message body
  (HTML or plain text), and attachments. Use this skill whenever the user
  needs to archive, review, or publish email content as human-readable Markdown
  (for notes, docs, PRs, or knowledge bases). The skill includes a small
  standalone script to extract attachments and convert HTML bodies to Markdown.
compatibility:
  - python: '>=3.8'
  - pip-packages: ['extract_msg', 'html2text']

---

What this skill does
- Converts a .msg file into a single Markdown file with a YAML frontmatter
  that contains canonical message metadata (Subject, From, To, Cc, Date,
  Message-ID, Attachments). The converted body is placed after the frontmatter
  as Markdown; HTML bodies are converted to Markdown when possible.
- Optionally extracts attachments to an attachments folder and inserts links to them in
  the Markdown output: pass `--save-attachments` to extract files. By default attachments are listed in the frontmatter but not saved.

When to use
- Use whenever a user asks to "convert", "export", "archive", "save as
  Markdown", or "render" an Outlook .msg message for documentation, review,
  or publishing.

Available tools
- `scripts/convert_msg.py` — CLI script that performs the conversion.
  - To extract attachments, add `--save-attachments`: `python scripts/convert_msg.py --input message.msg --save-attachments`

Prerequisites
- ask the user if they would like to save attachments; if yes, ensure the `attachments/` directory exists and is writable by the script.

Quick usage
1. Install requirements: `[ -d venv ] || python -m venv venv && source venv/bin/activate && pip install extract_msg html2text`
2. Run the script: 
  - if the user does not want to save attachments: `python scripts/convert_msg.py --input path/to/message.msg`
  - if the user wants to save attachments: `python scripts/convert_msg.py --input path/to/message.msg --save-attachments`

Output format (ALWAYS use this template)
```yaml
---
subject: "..."
from: "..."
to: ["...", "..."]
cc: ["...", "..."]
date: "2021-01-01T12:34:56Z"
message_id: "<...>"
attachments:
  - path: "attachments/message-name/file.pdf"
    filename: "file.pdf"
---

<message body as Markdown>
```

Notes and edge cases
- HTML email bodies are converted using `html2text`. Complex HTML (multipart,
  inline styles) may not render perfectly; inspect the attachments folder for
  images referenced inline.
- If a message contains embedded Microsoft Office attachments (e.g., .docx),
  the script will save the raw attachment file. Post-processing (converting
  .docx → .md) is out of scope but common; consider chaining this skill with
  a document-conversion skill.

Examples
- Convert one file in place:
  `python scripts/convert_msg.py --input Inbox/meeting-notes.msg`
- Convert and write outputs to a directory:
  `python scripts/convert_msg.py --input message.msg --output-dir exports/`
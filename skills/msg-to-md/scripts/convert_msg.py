#!/usr/bin/env python3
"""Convert a .msg file to Markdown, extracting metadata and attachments.

Usage:
  python scripts/convert_msg.py --input path/to/message.msg [--output-dir outdir]

Dependencies: extract_msg, html2text
Install: pip install extract_msg html2text
"""

import argparse
import os
import sys
import datetime
import json
from pathlib import Path

try:
    import extract_msg
except Exception:
    print(
        "Missing dependency: extract_msg. Install with `pip install extract_msg`",
        file=sys.stderr,
    )
    raise

try:
    import html2text
except Exception:
    print(
        "Missing dependency: html2text. Install with `pip install html2text`",
        file=sys.stderr,
    )
    raise


def safe_filename(name: str) -> str:
    # Replace path separators and control chars
    return "".join(c if c.isalnum() or c in "._-@ " else "_" for c in name).strip()


def isoformat(dt):
    if not dt:
        return None
    if isinstance(dt, str):
        return dt
    try:
        return dt.isoformat()
    except Exception:
        return str(dt)


def convert_msg(input_path: Path, output_dir: Path, save_attachments: bool = False):
    msg = extract_msg.Message(str(input_path))
    msg_sender = msg.sender
    msg_subject = msg.subject or ""
    msg_date = msg.date
    msg_to = msg.to
    msg_cc = msg.cc
    # extract_msg versions differ in attribute naming
    msg_message_id = getattr(msg, "message_id", None) or getattr(msg, "messageId", None)

    # prefer html body
    html_body = msg.htmlBody
    text_body = msg.body

    attachments = []
    if save_attachments:
        attach_dir = output_dir / "attachments" / safe_filename(input_path.stem)
        attach_dir.mkdir(parents=True, exist_ok=True)

        for i, att in enumerate(msg.attachments):
            # Determine a filename for the attachment (different extract_msg versions)
            filename = (
                getattr(att, "longFilename", None)
                or getattr(att, "shortFilename", None)
                or getattr(att, "filename", None)
                or f"attachment-{i}"
            )
            filename = safe_filename(filename)
            out_path = attach_dir / filename

            # Try multiple save strategies to support various extract_msg versions
            saved_path = None
            try:
                # Many versions accept a string path
                att.save(str(out_path))
                saved_path = out_path
            except TypeError:
                # Some Attachment.save() implementations take no args and write to cwd
                before = set(attach_dir.iterdir())
                cwd = os.getcwd()
                try:
                    os.chdir(str(attach_dir))
                    att.save()
                finally:
                    os.chdir(cwd)
                after = set(attach_dir.iterdir())
                new_files = sorted(after - before, key=lambda p: p.stat().st_mtime)
                if new_files:
                    saved_path = new_files[-1]
                    # rename to our expected filename if necessary
                    if saved_path.name != filename:
                        target = attach_dir / filename
                        try:
                            saved_path.rename(target)
                            saved_path = target
                        except Exception:
                            pass
            except Exception as e:
                print(f"Error saving attachment: {e}", file=sys.stderr)

            if not saved_path:
                # Final fallback: create an empty placeholder file
                saved_path = out_path
                try:
                    with open(saved_path, "wb") as fh:
                        fh.write(b"")
                except Exception:
                    pass

                attachments.append(
                    {
                        "path": str(saved_path.relative_to(output_dir)),
                        "filename": saved_path.name,
                    }
                )
    else:
        # Do not save attachments; only record filenames so frontmatter lists them.
        for i, att in enumerate(msg.attachments):
            filename = (
                getattr(att, "longFilename", None)
                or getattr(att, "shortFilename", None)
                or getattr(att, "filename", None)
                or f"attachment-{i}"
            )
            filename = safe_filename(filename)
            attachments.append({"path": "", "filename": filename})

    # Normalize body to str; some extract_msg versions return bytes
    if isinstance(html_body, bytes):
        try:
            html_body = html_body.decode("utf-8")
        except Exception:
            html_body = html_body.decode("latin-1", errors="replace")
    if isinstance(text_body, bytes):
        try:
            text_body = text_body.decode("utf-8")
        except Exception:
            text_body = text_body.decode("latin-1", errors="replace")

    # Convert HTML to markdown when possible
    body_markdown = ""
    if html_body and isinstance(html_body, str) and html_body.strip():
        h = html2text.HTML2Text()
        h.ignore_images = False
        h.body_width = 0
        body_markdown = h.handle(html_body)
    elif text_body:
        body_markdown = text_body
    else:
        body_markdown = ""

    # Build YAML frontmatter
    front = {
        "subject": msg_subject,
        "from": msg_sender,
        "to": [s.strip() for s in msg_to.split(";")] if msg_to else [],
        "cc": [s.strip() for s in msg_cc.split(";")] if msg_cc else [],
        "date": isoformat(msg_date),
        "message_id": msg_message_id,
        "attachments": attachments,
    }

    md_lines = []
    md_lines.append("---")
    # simple YAML emit
    for k, v in front.items():
        if k == "attachments":
            md_lines.append("attachments:")
            for a in v:
                md_lines.append(f'  - path: "{a["path"]}"')
                md_lines.append(f'    filename: "{a["filename"]}"')
        else:
            if isinstance(v, list):
                md_lines.append(f"{k}: {json.dumps(v)}")
            else:
                md_lines.append(f'{k}: "{v or ""}"')
    md_lines.append("---\n")
    md_lines.append(body_markdown or "")

    out_md_name = safe_filename(input_path.stem) + ".md"
    out_md_path = output_dir / out_md_name
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Wrote Markdown: {out_md_path}")
    if save_attachments and attachments:
        print(f"Extracted {len(attachments)} attachment(s) to: {attach_dir}")
    elif not save_attachments and attachments:
        print(f"Found {len(attachments)} attachment(s) but did not save them (use --save-attachments to extract).")


def main():
    p = argparse.ArgumentParser(description="Convert .msg to Markdown with attachments")
    p.add_argument("--input", "-i", required=True, help="Input .msg file")
    p.add_argument("--output-dir", "-o", default="./out", help="Output directory")
    p.add_argument(
        "--save-attachments",
        dest="save_attachments",
        action="store_true",
        help="Save attachments to an attachments/ subfolder (disabled by default)",
    )
    args = p.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(2)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        convert_msg(input_path, output_dir, save_attachments=bool(args.save_attachments))
    except Exception as e:
        print(f"Error converting message: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()

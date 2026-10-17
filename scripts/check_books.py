"""Book provenance, review integrity, and fail-closed affiliate activation."""

from datetime import date
from urllib.parse import parse_qs, urlparse
import json
import re


def isbn_valid(value):
    return bool(re.fullmatch(r"97[89]\d{10}", value)) and sum(
        int(digit) * (1 if index % 2 == 0 else 3)
        for index, digit in enumerate(value)
    ) % 10 == 0


def validate_books(books, programs):
    errors = []
    ids = set()
    for key, program in programs.items():
        if not isinstance(program.get("active"), bool):
            errors.append(f"{key}: active must be a boolean")
        if program.get("active") and not program.get("tracking_id", "").strip():
            errors.append(f"{key}: active program needs its assigned tracking ID")
    for book in books:
        identifier = book.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier) or identifier in ids:
            errors.append(f"invalid or duplicate book ID: {identifier}")
        ids.add(identifier)
        for field in ("title", "subtitle", "authors", "edition", "theme", "question", "summary", "audience", "skip", "source_label"):
            if not isinstance(book.get(field), str) or not book[field].strip():
                errors.append(f"{identifier}: missing {field}")
        if not isbn_valid(book.get("isbn", "")):
            errors.append(f"{identifier}: invalid ISBN-13")
        if not book.get("source_url", "").startswith("https://"):
            errors.append(f"{identifier}: publisher source must use HTTPS")
        if type(book.get("cover_id")) is not int or book["cover_id"] < 1:
            errors.append(f"{identifier}: verified Open Library cover ID required")
        try:
            date.fromisoformat(book.get("cover_checked", ""))
        except (TypeError, ValueError):
            errors.append(f"{identifier}: cover verification date required")
        if "—" in json.dumps(book, ensure_ascii=False):
            errors.append(f"{identifier}: em dash in book record")
        if not book.get("shops"):
            errors.append(f"{identifier}: at least one shop link required")
        for shop in book.get("shops", []):
            key = shop.get("program", "")
            program = programs.get(key)
            if not program:
                errors.append(f"{identifier}: unknown affiliate program {key}")
                continue
            ordinary = urlparse(shop.get("url", ""))
            if ordinary.scheme != "https" or not ordinary.hostname or ordinary.username or ordinary.password:
                errors.append(f"{identifier}: invalid ordinary shop URL")
            domain = {"amazon_us": "www.amazon.com", "amazon_de": "www.amazon.de"}.get(key)
            if domain and ordinary.hostname != domain:
                errors.append(f"{identifier}: ordinary Amazon shop uses the wrong storefront")
            if {"tag", "ascsubtag", "affid", "affiliate", "referral"}.intersection(parse_qs(ordinary.query)):
                errors.append(f"{identifier}: referral tag in ordinary link")
            paid = shop.get("affiliate_url", "")
            if not isinstance(paid, str):
                errors.append(f"{identifier}: affiliate_url must be an HTTPS URL or empty string")
                continue
            if paid:
                parsed = urlparse(paid)
                if not program.get("active"):
                    errors.append(f"{identifier}: affiliate URL before enrollment activation")
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    errors.append(f"{identifier}: invalid affiliate URL")
                if key.startswith("amazon_"):
                    if parsed.hostname != domain or parse_qs(parsed.query).get("tag") != [program.get("tracking_id")]:
                        errors.append(f"{identifier}: Amazon store or assigned tag mismatch")
    if sum(book.get("featured") is True for book in books) != 1:
        errors.append("exactly one featured reading selection required")
    return errors


def review_errors(text, books):
    def field(name):
        front = text.split("---", 2)[1] if text.startswith("---\n") else ""
        match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", front)
        return match[1].strip("\"'") if match else ""
    if field("post_type") != "book review":
        return []
    errors = []
    if field("book_id") not in {book["id"] for book in books}:
        errors.append("book review must reference a known book_id")
    if field("reading_basis") not in {"Full book", "Full book and author's reading notes"}:
        errors.append("full review requires a full-book reading basis, not a publisher summary")
    for marker in ("author_reviewed", "context_reviewed", "editorial_reviewed"):
        try:
            date.fromisoformat(field(marker))
        except ValueError:
            errors.append(f"book review requires {marker} date")
    if not field("material_relationship"):
        errors.append("book review must disclose review-copy or other material relationship status")
    return errors


def check_books(root, fail):
    books = json.loads((root / "_data/books.json").read_text(encoding="utf-8"))
    programs = json.loads((root / "_data/book_programs.json").read_text(encoding="utf-8"))
    errors = validate_books(books, programs)
    for path in (root / "_posts").glob("*.md"):
        errors.extend(f"{path.name}: {error}" for error in review_errors(path.read_text(encoding="utf-8"), books))
    if errors:
        fail("; ".join(errors))

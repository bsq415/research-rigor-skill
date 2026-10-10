#!/usr/bin/env python3
"""Verify bibliography identity/metadata, never citation relevance or truth.

Supports literal BibTeX fields; macros/concatenation stay unresolved. Online
lookups are opt-in. Offline records are fixtures/evidence, not live verification.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


def normalize(value):
    value = html.unescape(re.sub(r"<[^>]+>", "", value)).replace("\\&", " and ")
    value = re.sub(r"\\[\"'`^~=.]\{?([A-Za-z])\}?", r"\1", value)
    value = unicodedata.normalize("NFKD", value)
    return " ".join(re.findall(r"[^\W_]+", "".join(c for c in value if not unicodedata.combining(c)).casefold()))


def parse_bib(text):
    entries = []
    offset = 0
    pattern = re.compile(r"@(\w+)\s*([({])")
    while match := pattern.search(text, offset):
        start = match.end()
        opener, closer = match[2], "}" if match[2] == "{" else ")"
        depth, quoted, escaped, field_braces = 1, False, False, 0
        end = start
        while end < len(text) and depth:
            char = text[end]
            if char == '"' and not escaped and not field_braces and (opener == "(" or depth == 1):
                quoted = not quoted
            if not quoted and not escaped:
                if opener == "(" and char == "{":
                    field_braces += 1
                elif opener == "(" and char == "}":
                    field_braces -= 1
                elif char == opener and not field_braces:
                    depth += 1
                elif char == closer and not field_braces:
                    depth -= 1
            escaped = char == "\\" and not escaped
            end += 1
        if depth:
            raise ValueError("unbalanced bibliography entry")
        offset = end
        if match[1].lower() in {"comment", "preamble", "string"}:
            continue
        body = text[start:end-1]
        key, sep, fields = body.partition(",")
        if not sep or not key.strip():
            raise ValueError("bibliography entry lacks a key")
        result, unresolved = {"key": key.strip()}, []
        pos = 0
        while pos < len(fields):
            field = re.match(r"\s*,?\s*(\w+)\s*=\s*", fields[pos:])
            if not field:
                if fields[pos:].strip(" ,\r\n\t"):
                    unresolved.append("unparsed fields")
                break
            name = field[1].lower()
            pos += field.end()
            begin = pos
            if pos >= len(fields):
                raise ValueError("empty BibTeX field")
            if fields[pos] == "{":
                level = 1
                pos += 1
                begin = pos
                while pos < len(fields) and level:
                    if fields[pos] == "{" and fields[pos-1] != "\\": level += 1
                    if fields[pos] == "}" and fields[pos-1] != "\\": level -= 1
                    pos += 1
                value = fields[begin:pos-1]
                if level: raise ValueError("unbalanced field braces")
            elif fields[pos] == '"':
                pos += 1
                begin = pos
                while pos < len(fields) and not (fields[pos] == '"' and fields[pos-1] != "\\"):
                    pos += 1
                value = fields[begin:pos]
                if pos == len(fields): raise ValueError("unclosed quoted field")
                pos += 1
            else:
                while pos < len(fields) and fields[pos] not in ",#": pos += 1
                value = fields[begin:pos].strip()
                if not re.fullmatch(r"\d+", value): unresolved.append(name + ": macro")
            if pos < len(fields) and fields[pos:].lstrip().startswith("#"):
                unresolved.append(name + ": concatenation")
                break
            result[name] = value
        result["parse_notes"] = unresolved
        entries.append(result)
    if len({e["key"] for e in entries}) != len(entries):
        raise ValueError("duplicate bibliography key")
    if not entries:
        raise ValueError("no supported bibliography entries")
    return entries


def author_key(value):
    parts = value.split(",", 1)
    if len(parts) == 2:
        family, given = parts
    else:
        tokens = value.split()
        family, given = (tokens[-1], " ".join(tokens[:-1])) if len(tokens) > 1 else (value, "")
    given = normalize(given).split()
    return normalize(family), tuple(given)


def author_matches(left, right):
    if left[0] != right[0] or len(left[1]) != len(right[1]):
        return False
    return all(a == b or (min(len(a), len(b)) == 1 and a[0] == b[0])
               for a, b in zip(left[1], right[1]))


class Client:
    def __init__(self, cache, online=False, offline=None, provider="auto"):
        self.cache, self.online, self.offline, self.provider = cache, online, offline, provider
        self.last = 0

    def fetch(self, url, xml=False):
        key = hashlib.sha256(url.encode()).hexdigest()
        cache = self.cache / (key + ".json")
        if cache.exists():
            saved = json.loads(cache.read_text(encoding="utf-8"))
            if time.time() - saved["timestamp"] < 86400:
                return saved["body"]
        if not self.online:
            raise ValueError("online lookup not enabled and no recent cache")
        # arXiv-compatible serial pacing; no automatic retries or paid endpoint.
        time.sleep(max(0, 3.1 - (time.monotonic() - self.last)))
        self.last = time.monotonic()
        request = Request(url, headers={"User-Agent": "research-rigor-citation-audit/1.0", "Accept": "application/atom+xml" if xml else "application/json"})
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
        body = raw if xml else json.loads(raw)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(dict(timestamp=time.time(), url=url, body=body)), encoding="utf-8")
        return body

    def lookup(self, entry):
        doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", entry.get("doi", ""), flags=re.I).strip()
        arxiv = entry.get("eprint", "") if entry.get("archiveprefix", "arxiv").lower() == "arxiv" else ""
        if not arxiv:
            found = re.search(r"arxiv.org/(?:abs|pdf)/([^?#\s]+)", entry.get("url", ""))
            arxiv = found[1].removesuffix(".pdf") if found else ""
        identifier = doi or arxiv or entry.get("title", "")
        if self.offline is not None:
            record = self.offline.get(identifier)
            return [] if record is None else [record]
        if self.provider == "semantic-scholar":
            if not (doi or arxiv): raise ValueError("Semantic Scholar route requires DOI or arXiv identifier")
            pid = "DOI:"+doi if doi else "ARXIV:"+arxiv
            url = "https://api.semanticscholar.org/graph/v1/paper/"+quote(pid, safe="")+"?fields=title,authors,year,externalIds,url"
            data = self.fetch(url)
            return [dict(source="semantic-scholar", lookup_url=url, identifier=identifier,
                         title=data.get("title", ""), authors=[a["name"] for a in data.get("authors", [])],
                         years=[data["year"]] if data.get("year") else [], doi=data.get("externalIds", {}).get("DOI", ""))]
        if arxiv and not doi:
            if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[A-Za-z.-]+/\d{7})(?:v\d+)?", arxiv):
                raise ValueError("unsupported arXiv ID")
            url = "https://export.arxiv.org/api/query?"+urlencode({"id_list": arxiv})
            feed = ET.fromstring(self.fetch(url, xml=True))
            ns = {"a": "http://www.w3.org/2005/Atom"}
            records = []
            for e in feed.findall("a:entry", ns):
                rid = e.findtext("a:id", "", ns).split("/abs/")[-1]
                if re.sub(r"v\d+$", "", rid) != re.sub(r"v\d+$", "", arxiv): continue
                records.append(dict(source="arxiv", lookup_url=url, identifier=rid,
                                    title=e.findtext("a:title", "", ns), authors=[a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)],
                                    years=[int(e.findtext("a:published", "0000", ns)[:4])]))
            return records
        if doi:
            url = "https://api.crossref.org/works/"+quote(doi, safe="")
            data = self.fetch(url)["message"]
            candidates = [data]
        else:
            if not entry.get("title"): raise ValueError("missing title and identifier")
            url = "https://api.crossref.org/works?"+urlencode({"query.bibliographic": entry["title"], "rows": 5})
            candidates = self.fetch(url)["message"]["items"]
        records = []
        for data in candidates:
            years = sorted({d[0] for key in ("published", "published-print", "published-online", "issued")
                            for d in data.get(key, {}).get("date-parts", []) if d})
            records.append(dict(source="crossref", lookup_url=url, identifier=data.get("DOI", ""), doi=data.get("DOI", ""),
                                title=" ".join(data.get("title", [])),
                                authors=[a.get("family", a.get("name", ""))+", "+a.get("given", "") for a in data.get("author", [])], years=years))
        return records


def compare(entry, records):
    if entry["parse_notes"]:
        return dict(status="unresolved", reasons=entry["parse_notes"], candidates=records)
    if any(r.get("error") for r in records):
        return dict(status="unresolved", reasons=["provider/fixture error"], candidates=records)
    exact = [r for r in records if normalize(r.get("title", "")) == normalize(entry.get("title", "")) and normalize(entry.get("title", ""))]
    selected = exact if not entry.get("doi") else records
    if len(selected) != 1:
        return dict(status="unresolved", reasons=["no unique exact title match; absence is not proof of fabrication"], candidates=records)
    record = selected[0]
    missing, mismatch = [], []
    for field in ("title", "author", "year"):
        if not entry.get(field): missing.append(field)
    if not record.get("title") or not record.get("authors") or not record.get("years"):
        missing.append("provider metadata")
    if entry.get("title") and record.get("title") and normalize(entry["title"]) != normalize(record["title"]): mismatch.append("title")
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", entry.get("doi", ""), flags=re.I)
    if doi and record.get("doi", "").casefold() != doi.casefold(): mismatch.append("doi")
    authors = re.split(r"\s+and\s+", entry.get("author", ""))
    expected, actual = [author_key(a) for a in authors], [author_key(a) for a in record.get("authors", [])]
    if any(not a[1] for a in expected+actual) or any(normalize(a) in {"others", "et al"} for a in authors):
        missing.append("full interpretable author list")
    elif len(expected) != len(actual) or not all(author_matches(a, b) for a, b in zip(expected, actual)):
        mismatch.append("authors/order")
    if entry.get("year") and not re.fullmatch(r"\d{4}", entry["year"]): missing.append("literal year")
    elif entry.get("year") and record.get("years") and int(entry["year"]) not in record["years"]: mismatch.append("year")
    return dict(status="metadata_mismatch" if mismatch else "unresolved" if missing else "verified_metadata",
                reasons=mismatch+missing, matched_record=record,
                scope="bibliographic metadata only; ordered author names allow corresponding initials, not conflicting full names; ambiguous publication versions need review")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bib", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--offline", type=Path, help="normalized records JSON, explicitly labelled non-live")
    parser.add_argument("--provider", choices=("auto", "semantic-scholar"), default="auto")
    parser.add_argument("--cache-dir", type=Path, default=Path(".research/citation-cache"))
    args = parser.parse_args()
    report = dict(schema_version=1, mode="offline-evidence" if args.offline else "online" if args.online else "cache-only",
                  retrieved_utc=datetime.now(timezone.utc).isoformat(), entries=[])
    try:
        report["source_sha256"] = hashlib.sha256(args.bib.read_bytes()).hexdigest()
        offline = json.loads(args.offline.read_text(encoding="utf-8")) if args.offline else None
        client = Client(args.cache_dir, args.online, offline, args.provider)
        for entry in parse_bib(args.bib.read_text(encoding="utf-8")):
            try:
                result = compare(entry, client.lookup(entry))
            except (OSError, ValueError, KeyError, ET.ParseError, HTTPError) as exc:
                status = f" HTTP {exc.code}" if isinstance(exc, HTTPError) else ""
                result = dict(status="unresolved", reasons=[f"{type(exc).__name__}{status}: lookup unavailable; not proof of a fabricated source"])
            report["entries"].append(dict(key=entry["key"], **result))
        code = 0 if all(e["status"] == "verified_metadata" for e in report["entries"]) else 1
    except (OSError, ValueError) as exc:
        report["error"], code = str(exc), 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Citation metadata report: {args.output}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

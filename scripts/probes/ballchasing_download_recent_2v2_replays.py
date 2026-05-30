"""Download recent ranked-doubles replay files from Ballchasing.

This is a temporary data acquisition probe for parser validation. It writes only
under local_data/, which must stay ignored, and never prints or persists the API
token.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib import error, parse, request


API_BASE = "https://ballchasing.com/api"
REPO_ROOT = Path(__file__).resolve().parents[2]
REPLAY_DIR = REPO_ROOT / "local_data" / "ballchasing" / "replays"
METADATA_DIR = REPO_ROOT / "local_data" / "ballchasing" / "metadata"
INDEX_PATH = METADATA_DIR / "recent_2v2_index.json"
USER_AGENT = "fofo-arena-lab-ballchasing-probe/0.1"


class RateLimited(RuntimeError):
    """Raised when Ballchasing returns HTTP 429."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download recent ranked-doubles .replay files from Ballchasing."
    )
    parser.add_argument("--count", type=int, default=10, help="Maximum replay count.")
    parser.add_argument("--min-rank", default="champion-1")
    parser.add_argument("--max-rank", default="grand-champion")
    parser.add_argument(
        "--replay-date-after",
        default=None,
        help="Optional replay-date-after filter accepted by Ballchasing.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=1.0,
        help="Delay between replay file downloads. Minimum enforced: 1 second.",
    )
    return parser.parse_args()


def fetch_bytes(url: str, token: str) -> bytes:
    req = request.Request(
        url,
        headers={
            "Authorization": token,
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with request.urlopen(req, timeout=60) as response:
            return response.read()
    except error.HTTPError as exc:
        if exc.code == 429:
            retry_after = exc.headers.get("Retry-After", "not provided")
            raise RateLimited(
                f"Ballchasing returned HTTP 429. Retry-After: {retry_after}. "
                "Stopping safely."
            ) from exc
        body = exc.read(500).decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc


def fetch_json(url: str, token: str) -> dict[str, Any]:
    raw = fetch_bytes(url, token)
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON from {url}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected object JSON from {url}")
    return data


def load_index() -> dict[str, Any]:
    if not INDEX_PATH.exists():
        return {"items": []}
    try:
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"items": []}
    if not isinstance(data, dict):
        return {"items": []}
    if not isinstance(data.get("items"), list):
        data["items"] = []
    return data


def save_index(index: dict[str, Any], filters: dict[str, Any]) -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    index["source"] = "Ballchasing API"
    index["query_endpoint"] = f"{API_BASE}/replays"
    index["file_endpoint_template"] = f"{API_BASE}/replays/{{id}}/file"
    index["filters"] = filters
    index["updated_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    INDEX_PATH.write_text(json.dumps(index, indent=2, sort_keys=True), encoding="utf-8")


def safe_part(value: Any, fallback: str) -> str:
    text = str(value or fallback)
    text = text.replace(":", "-").replace("/", "-").replace("\\", "-")
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = text.strip("._-")
    return text or fallback


def rel_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def first_present(source: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = source.get(key)
        if value not in (None, ""):
            return value
    return None


def replay_date(entry: dict[str, Any]) -> str:
    value = first_present(entry, ("date", "replay_date", "replay-date", "created"))
    return str(value or "unknown-date")


def map_name(entry: dict[str, Any]) -> str:
    return str(first_present(entry, ("map_name", "map", "map_code")) or "")


def playlist_name(entry: dict[str, Any]) -> str:
    value = first_present(entry, ("playlist", "playlist_name"))
    if isinstance(value, dict):
        return str(first_present(value, ("name", "id")) or "")
    return str(value or "")


def existing_downloaded_ids(index: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in index.get("items", []):
        if not isinstance(item, dict):
            continue
        replay_id = item.get("id")
        file_path = item.get("file_path")
        if not replay_id or not file_path:
            continue
        if (REPO_ROOT / str(file_path)).exists():
            ids.add(str(replay_id))
    return ids


def upsert_index_item(index: dict[str, Any], item: dict[str, Any]) -> None:
    items = [row for row in index.get("items", []) if isinstance(row, dict)]
    replay_id = item["id"]
    for pos, existing in enumerate(items):
        if existing.get("id") == replay_id:
            items[pos] = item
            index["items"] = items
            return
    items.append(item)
    index["items"] = items


def build_query_url(filters: dict[str, Any]) -> str:
    params = {key: value for key, value in filters.items() if value not in (None, "")}
    return f"{API_BASE}/replays?{parse.urlencode(params)}"


def main() -> int:
    args = parse_args()
    if args.count < 1:
        print("--count must be at least 1", file=sys.stderr)
        return 2

    token = os.environ.get("BALLCHASING_API_KEY")
    if not token:
        print("BALLCHASING_API_KEY was not detected in the environment.", file=sys.stderr)
        return 2

    filters: dict[str, Any] = {
        "playlist": "ranked-doubles",
        "sort-by": "replay-date",
        "sort-dir": "desc",
        "count": args.count,
        "min-rank": args.min_rank,
        "max-rank": args.max_rank,
        "replay-date-after": args.replay_date_after,
    }
    query_url = build_query_url(filters)

    REPLAY_DIR.mkdir(parents=True, exist_ok=True)
    index = load_index()
    downloaded_ids = existing_downloaded_ids(index)
    sleep_seconds = max(1.0, args.sleep_seconds)

    print("BALLCHASING_API_KEY detected: yes")
    print(f"Query endpoint: GET {API_BASE}/replays")
    print(f"File endpoint: GET {API_BASE}/replays/{{id}}/file")

    try:
        response = fetch_json(query_url, token)
        replay_list = response.get("list", [])
        if not isinstance(replay_list, list):
            raise RuntimeError("Ballchasing response did not contain a list field.")

        selected = replay_list[: args.count]
        rows: list[dict[str, Any]] = []
        downloaded_this_run = 0
        skipped = 0

        for entry in selected:
            if not isinstance(entry, dict):
                continue
            replay_id = entry.get("id")
            if not replay_id:
                continue
            replay_id = str(replay_id)
            date_value = replay_date(entry)
            map_value = map_name(entry)
            playlist_value = playlist_name(entry)

            date_part = safe_part(date_value, "unknown-date")
            id_part = safe_part(replay_id, "unknown-id")
            destination = REPLAY_DIR / f"{date_part}_{id_part}.replay"

            if replay_id in downloaded_ids or destination.exists():
                skipped += 1
                size = destination.stat().st_size if destination.exists() else 0
                rows.append(
                    {
                        "id": replay_id,
                        "date": date_value,
                        "map": map_value,
                        "playlist": playlist_value,
                        "file_path": rel_path(destination),
                        "file_size": size,
                        "status": "skipped",
                    }
                )
                continue

            if downloaded_this_run > 0:
                time.sleep(sleep_seconds)

            file_url = f"{API_BASE}/replays/{parse.quote(replay_id, safe='')}/file"
            content = fetch_bytes(file_url, token)
            destination.write_bytes(content)
            downloaded_this_run += 1
            downloaded_ids.add(replay_id)

            item = {
                "id": replay_id,
                "date": date_value,
                "map": map_value,
                "playlist": playlist_value,
                "file_path": rel_path(destination),
                "file_size": len(content),
                "downloaded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            upsert_index_item(index, item)
            rows.append({**item, "status": "downloaded"})

        save_index(index, filters)
    except RateLimited as exc:
        save_index(index, filters)
        print(str(exc), file=sys.stderr)
        return 1

    print(
        f"Requested {args.count}; API returned {len(replay_list)}; "
        f"downloaded {downloaded_this_run}; skipped {skipped}."
    )
    print("id | date | map | playlist | file path | bytes | status")
    for row in rows:
        print(
            f"{row['id']} | {row['date']} | {row.get('map', '')} | "
            f"{row.get('playlist', '')} | {row['file_path']} | "
            f"{row.get('file_size', 0)} | {row['status']}"
        )
    print(f"Metadata index: {rel_path(INDEX_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

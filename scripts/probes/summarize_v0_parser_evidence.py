"""Summarize minimal parser-visible evidence for Normalized Replay V0.

This probe is intentionally bounded. It reads public subtr-actor fixtures,
calls only get_replay_frames_data and get_replay_meta, and prints a compact
stdout summary. It does not write dumps, define FOFO contracts, infer missing
attribution, or normalize parser variants.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURES = (
    REPO_ROOT
    / "external"
    / "subtr-actor"
    / "assets"
    / "recent-ranked-doubles-2026-03-10.replay",
    REPO_ROOT
    / "external"
    / "subtr-actor"
    / "assets"
    / "post-eac-ranked-doubles-2026-04-28.replay",
)
EVENT_KEYS = (
    "touch_events",
    "goal_events",
    "demolish_infos",
    "boost_pad_events",
    "dodge_refreshed_events",
    "player_stat_events",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print bounded Normalized Replay V0 parser evidence."
    )
    parser.add_argument(
        "fixtures",
        nargs="*",
        help="Optional replay fixture paths. Defaults to two public 2v2 fixtures.",
    )
    return parser.parse_args()


def rel_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def data_payload(frame: Any) -> dict[str, Any] | None:
    if isinstance(frame, dict):
        value = frame.get("Data")
        if isinstance(value, dict):
            return value
    return None


def variant_name(frame: Any) -> str:
    if isinstance(frame, dict):
        if "Data" in frame:
            return "Data"
        if "Empty" in frame:
            return "Empty"
        keys = ",".join(sorted(str(key) for key in frame.keys()))
        return f"dict({keys})"
    if isinstance(frame, str):
        return frame
    return type(frame).__name__


def player_entries(players: Any) -> list[tuple[Any, dict[str, Any]]]:
    entries: list[tuple[Any, dict[str, Any]]] = []
    for item in list_value(players):
        if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], dict):
            entries.append((item[0], item[1]))
    return entries


def team_names(players: Any) -> list[str]:
    names: list[str] = []
    for player in list_value(players):
        if isinstance(player, dict):
            name = player.get("name")
            if name not in (None, ""):
                names.append(str(name))
    return names


def format_names(names: list[str]) -> str:
    if not names:
        return "-"
    return ", ".join(name.replace("|", "\\|").replace("\n", " ") for name in names)


def count_null_field(items: Any, field: str) -> tuple[int, int]:
    nulls = 0
    present = 0
    for item in list_value(items):
        if not isinstance(item, dict):
            continue
        if item.get(field) is None:
            nulls += 1
        else:
            present += 1
    return nulls, present


def format_nulls(pair: tuple[int, int]) -> str:
    nulls, present = pair
    return f"null:{nulls}, present:{present}"


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "-"
    return ", ".join(f"{key}:{value}" for key, value in sorted(counter.items()))


def analyze_fixture(path: Path, subtr_actor: Any) -> dict[str, Any]:
    frames_output = subtr_actor.get_replay_frames_data(str(path))
    meta_output = subtr_actor.get_replay_meta(str(path))
    if not isinstance(frames_output, dict):
        raise RuntimeError(
            f"get_replay_frames_data returned {type(frames_output).__name__}, expected dict"
        )
    if not isinstance(meta_output, dict):
        raise RuntimeError(
            f"get_replay_meta returned {type(meta_output).__name__}, expected dict"
        )

    frame_data = frames_output.get("frame_data", {})
    if not isinstance(frame_data, dict):
        frame_data = {}
    frames_meta = frames_output.get("meta", {})
    if not isinstance(frames_meta, dict):
        frames_meta = {}
    replay_meta = meta_output.get("replay_meta", {})
    if not isinstance(replay_meta, dict):
        replay_meta = {}

    metadata_frames = list_value(frame_data.get("metadata_frames"))
    ball_data = frame_data.get("ball_data", {})
    ball_frames = list_value(ball_data.get("frames") if isinstance(ball_data, dict) else [])
    players = player_entries(frame_data.get("players"))
    player_lengths = [len(list_value(player_data.get("frames"))) for _id, player_data in players]

    ball_variants = Counter(variant_name(frame) for frame in ball_frames)
    player_variants: Counter[str] = Counter()
    player_team_null = 0
    player_team_present = 0
    for _player_id, player_data in players:
        player_frames = list_value(player_data.get("frames"))
        player_variants.update(variant_name(frame) for frame in player_frames)
        for frame in player_frames:
            data = data_payload(frame)
            if data is None:
                continue
            if data.get("team") is None:
                player_team_null += 1
            else:
                player_team_present += 1

    expected_frames = len(metadata_frames)
    aligned = (
        expected_frames == len(ball_frames)
        and all(length == expected_frames for length in player_lengths)
    )

    frames_team_zero = list_value(frames_meta.get("team_zero"))
    frames_team_one = list_value(frames_meta.get("team_one"))
    meta_team_zero = list_value(replay_meta.get("team_zero"))
    meta_team_one = list_value(replay_meta.get("team_one"))

    event_counts = {key: len(list_value(frames_output.get(key))) for key in EVENT_KEYS}
    optional_nulls = {
        "touch_events.player": count_null_field(frames_output.get("touch_events"), "player"),
        "goal_events.player": count_null_field(frames_output.get("goal_events"), "player"),
        "boost_pad_events.player": count_null_field(
            frames_output.get("boost_pad_events"), "player"
        ),
        "boost_pads.pad_id": count_null_field(frames_output.get("boost_pads"), "pad_id"),
        "PlayerFrame.Data.team": (player_team_null, player_team_present),
    }

    return {
        "path": path,
        "metadata_frames": expected_frames,
        "ball_frames": len(ball_frames),
        "player_tracks": len(players),
        "player_frame_min": min(player_lengths) if player_lengths else 0,
        "player_frame_max": max(player_lengths) if player_lengths else 0,
        "aligned": aligned,
        "team_zero_count": len(frames_team_zero),
        "team_one_count": len(frames_team_one),
        "team_zero_names": team_names(frames_team_zero),
        "team_one_names": team_names(frames_team_one),
        "meta_team_counts": f"{len(meta_team_zero)}+{len(meta_team_one)}",
        "boost_pads": len(list_value(frames_output.get("boost_pads"))),
        "event_counts": event_counts,
        "optional_nulls": optional_nulls,
        "ball_variants": ball_variants,
        "player_variants": player_variants,
    }


def print_summary(results: list[dict[str, Any]]) -> None:
    print("# FOFO V0 Parser Evidence Summary")
    print()
    print("Source boundary: get_replay_frames_data primary; get_replay_meta supporting.")
    print("Excluded: parse_replay, ndarray outputs, stats timelines, JS viewer models.")
    print()
    print("## Frame / Team Evidence")
    print()
    print(
        "| Fixture | Metadata Frames | Ball Frames | Player Tracks | Player Frame Range | "
        "Aligned | Team Zero | Team One | get_replay_meta Teams | Boost Pads |"
    )
    print("| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | ---: |")
    for result in results:
        print(
            f"| `{rel_path(result['path'])}` | {result['metadata_frames']} | "
            f"{result['ball_frames']} | {result['player_tracks']} | "
            f"{result['player_frame_min']}..{result['player_frame_max']} | "
            f"{result['aligned']} | "
            f"{result['team_zero_count']} ({format_names(result['team_zero_names'])}) | "
            f"{result['team_one_count']} ({format_names(result['team_one_names'])}) | "
            f"{result['meta_team_counts']} | {result['boost_pads']} |"
        )

    print()
    print("## Event Counts")
    print()
    print("| Fixture | Touches | Goals | Demos | Boost Pad Events | Dodge Refreshes | Player Stat Events |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for result in results:
        events = result["event_counts"]
        print(
            f"| `{rel_path(result['path'])}` | {events['touch_events']} | "
            f"{events['goal_events']} | {events['demolish_infos']} | "
            f"{events['boost_pad_events']} | {events['dodge_refreshed_events']} | "
            f"{events['player_stat_events']} |"
        )

    print()
    print("## Null / Optional Counts")
    print()
    print(
        "| Fixture | touch_events.player | goal_events.player | "
        "boost_pad_events.player | boost_pads.pad_id | PlayerFrame.Data.team |"
    )
    print("| --- | --- | --- | --- | --- | --- |")
    for result in results:
        nulls = result["optional_nulls"]
        print(
            f"| `{rel_path(result['path'])}` | "
            f"{format_nulls(nulls['touch_events.player'])} | "
            f"{format_nulls(nulls['goal_events.player'])} | "
            f"{format_nulls(nulls['boost_pad_events.player'])} | "
            f"{format_nulls(nulls['boost_pads.pad_id'])} | "
            f"{format_nulls(nulls['PlayerFrame.Data.team'])} |"
        )

    print()
    print("## Parser Variant Counts")
    print()
    print("| Fixture | BallFrame Variants | PlayerFrame Variants |")
    print("| --- | --- | --- |")
    for result in results:
        print(
            f"| `{rel_path(result['path'])}` | "
            f"{format_counter(result['ball_variants'])} | "
            f"{format_counter(result['player_variants'])} |"
        )


def main() -> int:
    args = parse_args()
    fixture_paths = [Path(value) for value in args.fixtures] if args.fixtures else list(DEFAULT_FIXTURES)
    fixture_paths = [path if path.is_absolute() else REPO_ROOT / path for path in fixture_paths]

    for path in fixture_paths:
        if not path.exists():
            print(f"Fixture not found: {rel_path(path)}", file=sys.stderr)
            return 1

    try:
        import subtr_actor  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - local environment probe
        print(f"Could not import subtr_actor: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    for path in fixture_paths:
        try:
            results.append(analyze_fixture(path, subtr_actor))
        except Exception as exc:
            print(
                f"Parser evidence summary failed for {rel_path(path)}: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return 3

    print_summary(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

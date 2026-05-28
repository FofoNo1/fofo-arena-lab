"""Temporary subtr_actor output inspection probe.

This script is intentionally exploratory. It prints bounded summaries of the
actual parser output shape from the built-in subtr-actor replay fixture without
creating FOFO-owned data contracts or writing dumps to disk.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import subtr_actor


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = (
    REPO_ROOT
    / "external"
    / "subtr-actor"
    / "assets"
    / "recent-ranked-doubles-2026-03-10.replay"
)

MAX_KEYS = 16
MAX_SAMPLE_ITEMS = 3
MAX_STRING_LENGTH = 80


def type_name(value: Any) -> str:
    return type(value).__name__


def count_label(value: Any) -> str:
    if isinstance(value, dict):
        return f"{len(value)} keys"
    if isinstance(value, (list, tuple)):
        return f"{len(value)} items"
    if isinstance(value, bytes):
        return f"{len(value)} bytes"
    if isinstance(value, (str, bytes)):
        return f"{len(value)} chars"
    return "scalar"


def clipped_repr(value: Any) -> str:
    text = repr(value)
    if len(text) > MAX_STRING_LENGTH:
        return f"{text[:MAX_STRING_LENGTH]}..."
    return text


def key_sample(mapping: dict[Any, Any]) -> list[str]:
    return [str(key) for key in list(mapping.keys())[:MAX_KEYS]]


def field_type_sample(mapping: dict[Any, Any]) -> dict[str, str]:
    return {
        str(key): type_name(value)
        for key, value in list(mapping.items())[:MAX_KEYS]
    }


def small_sample(value: Any, depth: int = 0) -> Any:
    if depth >= 2:
        return f"<{type_name(value)}: {count_label(value)}>"

    if isinstance(value, dict):
        return {
            str(key): small_sample(child, depth + 1)
            for key, child in list(value.items())[:MAX_SAMPLE_ITEMS]
        }

    if isinstance(value, (list, tuple)):
        return [
            small_sample(child, depth + 1)
            for child in list(value)[:MAX_SAMPLE_ITEMS]
        ]

    if isinstance(value, bytes):
        return f"<bytes: {len(value)}>"

    if isinstance(value, str):
        return value[:MAX_STRING_LENGTH]

    return value


def print_heading(title: str) -> None:
    print()
    print(f"## {title}")


def print_value_summary(label: str, value: Any, indent: int = 0) -> None:
    prefix = "  " * indent
    print(f"{prefix}{label}: {type_name(value)} ({count_label(value)})")


def print_dict_summary(label: str, value: Any, max_depth: int = 1) -> None:
    print_value_summary(label, value)
    if not isinstance(value, dict):
        print(f"  sample: {clipped_repr(small_sample(value))}")
        return

    print(f"  keys: {key_sample(value)}")
    print(f"  field_types: {field_type_sample(value)}")
    print_nested_summary(value, indent=1, depth=0, max_depth=max_depth)


def print_nested_summary(
    value: Any,
    indent: int,
    depth: int,
    max_depth: int,
) -> None:
    if depth >= max_depth:
        return

    prefix = "  " * indent

    if isinstance(value, dict):
        for key, child in list(value.items())[:MAX_KEYS]:
            key_label = str(key)
            print_value_summary(key_label, child, indent)
            if isinstance(child, dict):
                print(f"{prefix}  keys: {key_sample(child)}")
                print(f"{prefix}  field_types: {field_type_sample(child)}")
                print_nested_summary(child, indent + 1, depth + 1, max_depth)
            elif isinstance(child, (list, tuple)):
                print_sequence_sample(child, indent + 1, depth + 1, max_depth)
            else:
                print(f"{prefix}  sample: {clipped_repr(small_sample(child))}")
        return

    if isinstance(value, (list, tuple)):
        print_sequence_sample(value, indent, depth, max_depth)


def print_sequence_sample(
    values: list[Any] | tuple[Any, ...],
    indent: int,
    depth: int,
    max_depth: int,
) -> None:
    prefix = "  " * indent
    if not values:
        print(f"{prefix}sample: []")
        return

    sample = list(values)[:MAX_SAMPLE_ITEMS]
    print(f"{prefix}sample_types: {[type_name(item) for item in sample]}")

    first = sample[0]
    if isinstance(first, dict):
        print(f"{prefix}first_keys: {key_sample(first)}")
        print(f"{prefix}first_field_types: {field_type_sample(first)}")
        if depth < max_depth:
            print_nested_summary(first, indent, depth, max_depth)
    elif isinstance(first, (list, tuple)):
        print(f"{prefix}first_item_count: {len(first)}")
        print(f"{prefix}first_item_types: {[type_name(item) for item in first[:MAX_SAMPLE_ITEMS]]}")
        if depth < max_depth:
            print_sequence_sample(first, indent, depth + 1, max_depth)
    else:
        print(f"{prefix}sample: {clipped_repr(small_sample(sample))}")


def first_non_empty_sequence_item(values: Any) -> Any | None:
    if not isinstance(values, (list, tuple)):
        return None

    for item in values:
        if item is None:
            continue
        if isinstance(item, dict) and not item:
            continue
        if isinstance(item, (list, tuple)) and not item:
            continue
        return item
    return None


def get_nested(value: Any, *keys: str) -> Any | None:
    current = value
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def print_replay_meta(meta_output: dict[str, Any]) -> None:
    print_heading("get_replay_meta")
    print_dict_summary("meta_output", meta_output, max_depth=2)

    replay_meta = meta_output.get("replay_meta")
    if isinstance(replay_meta, dict):
        print_heading("get_replay_meta teams")
        for team_key in ("team_zero", "team_one"):
            team = replay_meta.get(team_key)
            print_value_summary(team_key, team)
            print_sequence_sample(team, indent=1, depth=0, max_depth=1) if isinstance(team, (list, tuple)) else None

    column_headers = meta_output.get("column_headers")
    if isinstance(column_headers, dict):
        print_heading("get_replay_meta column headers")
        print_header_summary(column_headers)


def print_column_headers(headers: dict[str, Any]) -> None:
    print_heading("get_column_headers")
    print_dict_summary("column_headers", headers, max_depth=1)
    print_header_summary(headers)


def print_header_summary(headers: dict[str, Any]) -> None:
    for header_key in ("global_headers", "player_headers"):
        values = headers.get(header_key)
        print_value_summary(header_key, values)
        if isinstance(values, (list, tuple)):
            print(f"  sample: {clipped_repr(list(values)[:MAX_SAMPLE_ITEMS])}")


def print_parse_replay(raw_replay: dict[str, Any]) -> None:
    print_heading("parse_replay")
    print_dict_summary("raw_replay", raw_replay, max_depth=1)


def print_replay_frames_data(frames_output: dict[str, Any]) -> None:
    print_heading("get_replay_frames_data")
    print_dict_summary("frames_output", frames_output, max_depth=1)

    frame_data = frames_output.get("frame_data")
    if isinstance(frame_data, dict):
        print_heading("frame_data")
        print_dict_summary("frame_data", frame_data, max_depth=1)
        print_frame_data_samples(frame_data)

    print_heading("event streams")
    for event_key in (
        "touch_events",
        "goal_events",
        "demolish_infos",
        "boost_pad_events",
        "boost_pads",
        "dodge_refreshed_events",
        "player_stat_events",
    ):
        values = frames_output.get(event_key)
        print_value_summary(event_key, values)
        if isinstance(values, (list, tuple)):
            print_sequence_sample(values, indent=1, depth=0, max_depth=1)


def print_frame_data_samples(frame_data: dict[str, Any]) -> None:
    metadata_frames = frame_data.get("metadata_frames")
    print_heading("metadata_frames")
    print_value_summary("metadata_frames", metadata_frames)
    if isinstance(metadata_frames, (list, tuple)):
        if metadata_frames:
            print("  first:")
            print_value_summary("frame", metadata_frames[0], indent=2)
            print(f"    sample: {clipped_repr(small_sample(metadata_frames[0]))}")
            print("  last:")
            print_value_summary("frame", metadata_frames[-1], indent=2)
            print(f"    sample: {clipped_repr(small_sample(metadata_frames[-1]))}")

    ball_frames = get_nested(frame_data, "ball_data", "frames")
    print_heading("ball_data.frames")
    print_value_summary("ball_frames", ball_frames)
    first_ball_frame = first_non_empty_sequence_item(ball_frames)
    if first_ball_frame is not None:
        print_value_summary("first_non_empty_ball_frame", first_ball_frame, indent=1)
        print(f"  sample: {clipped_repr(small_sample(first_ball_frame))}")

    players = frame_data.get("players")
    print_heading("players")
    print_value_summary("players", players)
    if isinstance(players, (list, tuple)):
        for index, player_track in enumerate(list(players)[:MAX_SAMPLE_ITEMS]):
            print_value_summary(f"player_track[{index}]", player_track, indent=1)
            print(f"    sample: {clipped_repr(small_sample(player_track))}")
            player_data = extract_player_data(player_track)
            player_frames = player_data.get("frames") if isinstance(player_data, dict) else None
            print_value_summary(f"player_track[{index}].frames", player_frames, indent=2)
            first_player_frame = first_non_empty_sequence_item(player_frames)
            if first_player_frame is not None:
                print_value_summary("first_non_empty_player_frame", first_player_frame, indent=3)
                print(f"      sample: {clipped_repr(small_sample(first_player_frame))}")


def extract_player_data(player_track: Any) -> Any | None:
    if isinstance(player_track, dict):
        if "frames" in player_track:
            return player_track
        for key in ("data", "player_data"):
            if key in player_track:
                return player_track[key]
        return None

    if isinstance(player_track, (list, tuple)) and len(player_track) >= 2:
        return player_track[1]

    return None


def print_stats_module_names(module_names: list[str]) -> None:
    print_heading("get_stats_module_names")
    print_value_summary("module_names", module_names)
    print(f"  sample: {clipped_repr(module_names[:MAX_KEYS])}")


def main() -> None:
    if not FIXTURE_PATH.exists():
        raise FileNotFoundError(f"Fixture not found: {FIXTURE_PATH}")

    replay_bytes = FIXTURE_PATH.read_bytes()
    meta_output = subtr_actor.get_replay_meta(str(FIXTURE_PATH))
    raw_replay = subtr_actor.parse_replay(replay_bytes)
    frames_output = subtr_actor.get_replay_frames_data(str(FIXTURE_PATH))
    module_names = subtr_actor.get_stats_module_names()
    column_headers = subtr_actor.get_column_headers()

    print(f"fixture: {FIXTURE_PATH.relative_to(REPO_ROOT)}")
    print(f"fixture_size_bytes: {FIXTURE_PATH.stat().st_size}")

    print_replay_meta(meta_output)
    print_parse_replay(raw_replay)
    print_replay_frames_data(frames_output)
    print_stats_module_names(module_names)
    print_column_headers(column_headers)


if __name__ == "__main__":
    main()

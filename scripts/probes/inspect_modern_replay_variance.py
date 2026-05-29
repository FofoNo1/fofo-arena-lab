"""Inspect parser-output variance across downloaded modern 2v2 replays.

This probe reads local_data/ballchasing/replays/*.replay, parses each replay via
subtr_actor, and emits a compact variance summary. It does not write parser JSON
dumps or define FOFO-owned data contracts.
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
from pathlib import Path
import sys
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPLAY_DIR = REPO_ROOT / "local_data" / "ballchasing" / "replays"
DEFAULT_REPORT_PATH = (
    REPO_ROOT / "local_data" / "ballchasing" / "reports" / "modern_2v2_variance_summary.md"
)
FIXTURE_VARIANCE_REPORT = REPO_ROOT / "docs" / "SUBTR_ACTOR_FIXTURE_VARIANCE_REPORT.md"
EVENT_KEYS = (
    "touch_events",
    "goal_events",
    "demolish_infos",
    "boost_pad_events",
    "boost_pads",
    "dodge_refreshed_events",
    "player_stat_events",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect subtr_actor parser-output variance for downloaded replays."
    )
    parser.add_argument("--replay-dir", default=str(DEFAULT_REPLAY_DIR))
    parser.add_argument("--max-replays", type=int, default=None)
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT_PATH))
    return parser.parse_args()


def rel_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def list_len(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def data_payload(frame: Any) -> dict[str, Any] | None:
    if isinstance(frame, dict):
        data = frame.get("Data")
        if isinstance(data, dict):
            return data
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


def null_count(events: Any, field: str) -> tuple[int, int]:
    if not isinstance(events, list):
        return (0, 0)
    nulls = 0
    present = 0
    for event in events:
        if not isinstance(event, dict):
            continue
        if event.get(field) is None:
            nulls += 1
        else:
            present += 1
    return nulls, present


def velocity_presence(frames: list[Any]) -> dict[str, int]:
    counts = {
        "linear_velocity_present": 0,
        "linear_velocity_null": 0,
        "angular_velocity_present": 0,
        "angular_velocity_null": 0,
    }
    for frame in frames:
        data = data_payload(frame)
        if data is None:
            continue
        rigid_body = data.get("rigid_body")
        if not isinstance(rigid_body, dict):
            counts["linear_velocity_null"] += 1
            counts["angular_velocity_null"] += 1
            continue
        if rigid_body.get("linear_velocity") is None:
            counts["linear_velocity_null"] += 1
        else:
            counts["linear_velocity_present"] += 1
        if rigid_body.get("angular_velocity") is None:
            counts["angular_velocity_null"] += 1
        else:
            counts["angular_velocity_present"] += 1
    return counts


def analyze_ball_frames(frames: Any) -> dict[str, Any]:
    if not isinstance(frames, list):
        frames = []
    return {
        "count": len(frames),
        "variants": Counter(variant_name(frame) for frame in frames),
        "velocity": velocity_presence(frames),
    }


def player_entries(players: Any) -> list[tuple[Any, dict[str, Any]]]:
    if not isinstance(players, list):
        return []
    entries: list[tuple[Any, dict[str, Any]]] = []
    for item in players:
        if isinstance(item, list) and len(item) == 2 and isinstance(item[1], dict):
            entries.append((item[0], item[1]))
        elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], dict):
            entries.append((item[0], item[1]))
    return entries


def analyze_player_tracks(players: Any) -> dict[str, Any]:
    entries = player_entries(players)
    frame_lengths: list[int] = []
    variants: Counter[str] = Counter()
    team_present = 0
    team_null = 0
    velocity = {
        "linear_velocity_present": 0,
        "linear_velocity_null": 0,
        "angular_velocity_present": 0,
        "angular_velocity_null": 0,
    }

    for _player_id, player in entries:
        frames = player.get("frames", [])
        if not isinstance(frames, list):
            frames = []
        frame_lengths.append(len(frames))
        variants.update(variant_name(frame) for frame in frames)
        for frame in frames:
            data = data_payload(frame)
            if data is None:
                continue
            if data.get("team") is None:
                team_null += 1
            else:
                team_present += 1
        frame_velocity = velocity_presence(frames)
        for key, value in frame_velocity.items():
            velocity[key] += value

    return {
        "count": len(entries),
        "frame_lengths": frame_lengths,
        "variants": variants,
        "team_present": team_present,
        "team_null": team_null,
        "velocity": velocity,
    }


def team_players(meta: dict[str, Any], key: str) -> list[Any]:
    players = meta.get(key)
    if isinstance(players, list):
        return players
    return []


def player_name(player: Any) -> str | None:
    if not isinstance(player, dict):
        return None
    name = player.get("name")
    if name in (None, ""):
        return None
    return str(name)


def player_names(players: list[Any]) -> list[str]:
    names: list[str] = []
    for player in players:
        name = player_name(player)
        if name is not None:
            names.append(name)
    return names


def format_names(names: list[str]) -> str:
    if not names:
        return "-"
    return ", ".join(name.replace("|", "\\|").replace("\n", " ") for name in names)


def analyze_output(replay_path: Path, output: dict[str, Any]) -> dict[str, Any]:
    meta = output.get("meta", {})
    if not isinstance(meta, dict):
        meta = {}
    frame_data = output.get("frame_data", {})
    if not isinstance(frame_data, dict):
        frame_data = {}

    metadata_frames = frame_data.get("metadata_frames", [])
    ball = frame_data.get("ball_data", {})
    ball_frames = ball.get("frames", []) if isinstance(ball, dict) else []
    players = frame_data.get("players", [])

    ball_analysis = analyze_ball_frames(ball_frames)
    player_analysis = analyze_player_tracks(players)
    player_lengths = player_analysis["frame_lengths"]
    team_zero_players = team_players(meta, "team_zero")
    team_one_players = team_players(meta, "team_one")

    event_counts = {key: list_len(output.get(key)) for key in EVENT_KEYS}
    optional_nulls = {
        "touch_events.player": null_count(output.get("touch_events"), "player"),
        "goal_events.player": null_count(output.get("goal_events"), "player"),
        "boost_pad_events.player": null_count(output.get("boost_pad_events"), "player"),
        "boost_pads.pad_id": null_count(output.get("boost_pads"), "pad_id"),
    }

    expected = list_len(metadata_frames)
    aligned = (
        expected == ball_analysis["count"]
        and all(length == expected for length in player_lengths)
    )

    return {
        "path": replay_path,
        "status": "success",
        "metadata_frames": expected,
        "ball_frames": ball_analysis["count"],
        "player_track_count": player_analysis["count"],
        "team_zero_players": len(team_zero_players),
        "team_one_players": len(team_one_players),
        "team_zero_names": player_names(team_zero_players),
        "team_one_names": player_names(team_one_players),
        "event_counts": event_counts,
        "optional_nulls": optional_nulls,
        "ball_variants": ball_analysis["variants"],
        "player_variants": player_analysis["variants"],
        "player_frame_min": min(player_lengths) if player_lengths else 0,
        "player_frame_max": max(player_lengths) if player_lengths else 0,
        "aligned": aligned,
        "player_team_present": player_analysis["team_present"],
        "player_team_null": player_analysis["team_null"],
        "ball_velocity": ball_analysis["velocity"],
        "player_velocity": player_analysis["velocity"],
    }


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "-"
    return ", ".join(f"{key}:{value}" for key, value in sorted(counter.items()))


def format_nulls(pair: tuple[int, int]) -> str:
    nulls, present = pair
    return f"null:{nulls}, present:{present}"


def aggregate_successes(results: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [result for result in results if result.get("status") == "success"]
    aggregate: dict[str, Any] = {
        "event_counts": Counter(),
        "ball_variants": Counter(),
        "player_variants": Counter(),
        "optional_nulls": Counter(),
        "aligned_count": 0,
        "ball_velocity": Counter(),
        "player_velocity": Counter(),
        "player_team_null": 0,
        "player_team_present": 0,
    }
    for result in successes:
        aggregate["event_counts"].update(result["event_counts"])
        aggregate["ball_variants"].update(result["ball_variants"])
        aggregate["player_variants"].update(result["player_variants"])
        if result["aligned"]:
            aggregate["aligned_count"] += 1
        for key, pair in result["optional_nulls"].items():
            nulls, present = pair
            aggregate["optional_nulls"][f"{key}.null"] += nulls
            aggregate["optional_nulls"][f"{key}.present"] += present
        aggregate["ball_velocity"].update(result["ball_velocity"])
        aggregate["player_velocity"].update(result["player_velocity"])
        aggregate["player_team_null"] += result["player_team_null"]
        aggregate["player_team_present"] += result["player_team_present"]
    return aggregate


def build_summary(results: list[dict[str, Any]], replay_dir: Path) -> str:
    successes = [result for result in results if result.get("status") == "success"]
    failures = [result for result in results if result.get("status") != "success"]
    aggregate = aggregate_successes(results)
    fixture_ref = rel_path(FIXTURE_VARIANCE_REPORT)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat()

    lines: list[str] = [
        "# Modern 2v2 Replay Variance Summary",
        "",
        f"Generated at UTC: {generated_at}",
        "",
        "## Scope",
        "",
        (
            "This is a local research summary for recent ranked-doubles replays "
            "downloaded from Ballchasing. It compares the same parser-output "
            f"variance categories used by `{fixture_ref}` without defining FOFO "
            "data contracts."
        ),
        "",
        "## Replay Set",
        "",
        f"- Replay directory: `{rel_path(replay_dir)}`",
        f"- Replay files scanned: {len(results)}",
        f"- Parse successes: {len(successes)}",
        f"- Parse failures: {len(failures)}",
        "",
        "## Per-Replay Counts",
        "",
        (
            "| Replay | Status | Metadata Frames | Ball Frames | Player Tracks | "
            "Team 0 | Team 1 | Team 0 Names | Team 1 Names | Aligned | Events |"
        ),
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]

    for result in results:
        if result.get("status") != "success":
            lines.append(
                f"| `{rel_path(result['path'])}` | failure: {result['error']} | - | - | - | - | - | - | - | - | - |"
            )
            continue
        events = ", ".join(
            f"{key}:{value}" for key, value in result["event_counts"].items()
        )
        lines.append(
            f"| `{rel_path(result['path'])}` | success | {result['metadata_frames']} | "
            f"{result['ball_frames']} | {result['player_track_count']} | "
            f"{result['team_zero_players']} | {result['team_one_players']} | "
            f"{format_names(result['team_zero_names'])} | "
            f"{format_names(result['team_one_names'])} | "
            f"{result['aligned']} | {events} |"
        )

    lines.extend(
        [
            "",
            "## Optional / Null Observations",
            "",
            "| Replay | touch_events.player | goal_events.player | boost_pad_events.player | boost_pads.pad_id | PlayerFrame.Data.team |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for result in successes:
        optional = result["optional_nulls"]
        lines.append(
            f"| `{rel_path(result['path'])}` | "
            f"{format_nulls(optional['touch_events.player'])} | "
            f"{format_nulls(optional['goal_events.player'])} | "
            f"{format_nulls(optional['boost_pad_events.player'])} | "
            f"{format_nulls(optional['boost_pads.pad_id'])} | "
            f"null:{result['player_team_null']}, present:{result['player_team_present']} |"
        )

    lines.extend(
        [
            "",
            "## Variant Observations",
            "",
            "| Replay | BallFrame Variants | PlayerFrame Variants | Player Frame Length Range |",
            "| --- | --- | --- | --- |",
        ]
    )
    for result in successes:
        lines.append(
            f"| `{rel_path(result['path'])}` | {format_counter(result['ball_variants'])} | "
            f"{format_counter(result['player_variants'])} | "
            f"{result['player_frame_min']}..{result['player_frame_max']} |"
        )

    lines.extend(
        [
            "",
            "## Velocity Observations",
            "",
            "| Replay | Ball rigid_body velocities | Player rigid_body velocities |",
            "| --- | --- | --- |",
        ]
    )
    for result in successes:
        lines.append(
            f"| `{rel_path(result['path'])}` | {dict(result['ball_velocity'])} | "
            f"{dict(result['player_velocity'])} |"
        )

    lines.extend(
        [
            "",
            "## Aggregate Comparison Notes",
            "",
            f"- Fixture baseline referenced: `{fixture_ref}`",
            (
                f"- Frame alignment in modern sample: {aggregate['aligned_count']} "
                f"of {len(successes)} successful parses had metadata, ball, and "
                "player frame lengths aligned."
            ),
            f"- Aggregate event counts: {dict(aggregate['event_counts'])}",
            f"- Aggregate BallFrame variants: {dict(aggregate['ball_variants'])}",
            f"- Aggregate PlayerFrame variants: {dict(aggregate['player_variants'])}",
            f"- Aggregate optional/null counts: {dict(aggregate['optional_nulls'])}",
            f"- Aggregate BallFrame velocity presence: {dict(aggregate['ball_velocity'])}",
            f"- Aggregate PlayerFrame velocity presence: {dict(aggregate['player_velocity'])}",
            (
                f"- Aggregate PlayerFrame.Data.team values: null "
                f"{aggregate['player_team_null']}, present "
                f"{aggregate['player_team_present']}"
            ),
            "",
            "## Runtime Verification Still Needed",
            "",
            "- This summary only covers the downloaded local sample.",
            "- It does not confirm JSON serialization shape beyond Python-visible values.",
            "- It does not decide whether any field should become a FOFO-owned contract.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    replay_dir = Path(args.replay_dir)
    replay_paths = sorted(replay_dir.glob("*.replay"))
    if args.max_replays is not None:
        replay_paths = replay_paths[: args.max_replays]

    if not replay_paths:
        print(f"No .replay files found in {rel_path(replay_dir)}", file=sys.stderr)
        return 1

    try:
        import subtr_actor  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - local environment probe
        print(f"Could not import subtr_actor: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    for replay_path in replay_paths:
        try:
            output = subtr_actor.get_replay_frames_data(str(replay_path))
            if not isinstance(output, dict):
                raise RuntimeError(f"Expected dict output, got {type(output).__name__}")
            results.append(analyze_output(replay_path, output))
            print(f"parsed: {rel_path(replay_path)}")
        except Exception as exc:
            results.append(
                {
                    "path": replay_path,
                    "status": "failure",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"failed: {rel_path(replay_path)}: {type(exc).__name__}: {exc}")

    summary = build_summary(results, replay_dir)
    print()
    print(summary)

    if args.write_summary:
        report_path = Path(args.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(summary, encoding="utf-8")
        print(f"Wrote summary: {rel_path(report_path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

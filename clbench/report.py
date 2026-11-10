"""Turn a run directory into a markdown results table and a learning-curve SVG."""
import random
import sys
from collections import defaultdict

from clbench.model import ROOT, Attempt

COLORS = ["#888888", "#d62728", "#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]


def load(run_name):
    arms = {}
    for arm_dir in sorted((ROOT / "runs" / run_name).iterdir()):
        log = arm_dir / "attempts.jsonl"
        if log.exists():
            arms[arm_dir.name] = [Attempt.from_json(line) for line in log.read_text().splitlines()]
    return arms


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else float("nan")


def thirds(attempts):
    size = len(attempts) // 3
    return [attempts[:size], attempts[size:len(attempts) - size], attempts[len(attempts) - size:]]


def paired_gain(arm, baseline, resamples=10000):
    """Mean per-ticket compliance gain over the baseline arm, with a paired bootstrap 95% interval."""
    base = {a.ticket_id: a.feedback.compliance for a in baseline}
    deltas = [a.feedback.compliance - base[a.ticket_id] for a in arm if a.ticket_id in base]
    if not deltas:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(0)
    means = sorted(mean(rng.choices(deltas, k=len(deltas))) for _ in range(resamples))
    return mean(deltas), means[int(0.025 * resamples)], means[int(0.975 * resamples)]


def exposures(attempts):
    """For each convention, the ordered list of outcomes (True = followed) across the stream."""
    seen = defaultdict(list)
    for attempt in attempts:
        for convention in attempt.feedback.passed:
            seen[convention].append(True)
        for convention in attempt.feedback.violated:
            seen[convention].append(False)
    return seen


def repeat_violation_rate(attempts):
    """Share of exposures that are violations, counted only after the first violation of that convention.

    After the first violation the reviewer has explained the rule once, so every later violation is a repeated mistake.
    """
    repeats = chances = 0
    for outcomes in exposures(attempts).values():
        if False not in outcomes:
            continue
        after = outcomes[outcomes.index(False) + 1:]
        chances += len(after)
        repeats += after.count(False)
    return repeats / chances if chances else float("nan"), chances


def compliance_by_exposure(attempts, buckets=((0, 1), (1, 3), (3, 99))):
    rows = []
    for low, high in buckets:
        outcomes = [o for series in exposures(attempts).values() for o in series[low:high]]
        rows.append(mean(outcomes))
    return rows


def curve_svg(arms, window=6, width=760, height=320):
    pad = 45
    longest = max(len(a) for a in arms.values())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="sans-serif" font-size="12">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{pad}" y="18">Convention compliance, trailing {window}-ticket mean, by stream position</text>',
    ]
    for tick in (0, 0.25, 0.5, 0.75, 1.0):
        y = height - pad - tick * (height - 2 * pad)
        parts.append(f'<line x1="{pad}" x2="{width - 150}" y1="{y}" y2="{y}" stroke="#eee"/>')
        parts.append(f'<text x="{pad - 8}" y="{y + 4}" text-anchor="end">{tick:.2f}</text>')
    for index, (name, attempts) in enumerate(arms.items()):
        points = []
        for position in range(len(attempts)):
            recent = attempts[max(0, position - window + 1):position + 1]
            value = mean(a.feedback.compliance for a in recent)
            x = pad + position * (width - 150 - pad) / max(1, longest - 1)
            y = height - pad - value * (height - 2 * pad)
            points.append(f"{x:.1f},{y:.1f}")
        color = COLORS[index % len(COLORS)]
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{" ".join(points)}"/>')
        parts.append(f'<text x="{width - 140}" y="{40 + 18 * index}" fill="{color}">{name}</text>')
    parts.append(f'<text x="{(width - 150) / 2}" y="{height - 10}">ticket position in stream</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def render(run_name):
    arms = load(run_name)
    baseline, oracle = arms.get("none-rich"), arms.get("oracle-rich")
    lines = [
        f"# Results: run `{run_name}`", "",
        "| arm | tickets | CI pass | compliance | first-try merge | early / mid / late compliance | "
        "gain vs stateless (95% CI) | oracle gap closed | repeat-violation rate | $ per ticket |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for name, attempts in arms.items():
        compliance = mean(a.feedback.compliance for a in attempts)
        segments = " / ".join(f"{mean(a.feedback.compliance for a in part):.2f}" for part in thirds(attempts))
        gain = closed = "n/a"
        if baseline and name != "none-rich":
            delta, low, high = paired_gain(attempts, baseline)
            gain = f"{delta:+.2f} ({low:+.2f}, {high:+.2f})"
            if oracle:
                headroom = paired_gain(oracle, baseline)[0]
                closed = f"{delta / headroom:.0%}" if headroom > 0 else "n/a"
        repeat, chances = repeat_violation_rate(attempts)
        cost = mean(a.cost_usd + a.learn_cost_usd for a in attempts)
        lines.append(
            f"| {name} | {len(attempts)} | {mean(a.feedback.ci_passed for a in attempts):.2f} | {compliance:.2f} | "
            f"{mean(a.feedback.merged for a in attempts):.2f} | {segments} | {gain} | {closed} | "
            f"{repeat:.2f} (n={chances}) | {cost:.3f} |"
        )
    lines += ["", "## Compliance by how many times the agent has met the convention", "",
              "| arm | 1st exposure | 2nd to 3rd | 4th and later |", "|---|---|---|---|"]
    for name, attempts in arms.items():
        lines.append(f"| {name} | " + " | ".join(f"{v:.2f}" for v in compliance_by_exposure(attempts)) + " |")
    lines += ["", "## After the migration (`events` replaces `audit`)", "",
              "| arm | `events` outcomes in order (1 = followed) |", "|---|---|"]
    for name, attempts in arms.items():
        outcomes = exposures(attempts).get("events", [])
        lines.append(f"| {name} | {' '.join(str(int(o)) for o in outcomes) or 'n/a'} |")
    lines += ["", "![learning curve](curve.svg)", ""]
    out = ROOT / "results" / run_name
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.md").write_text("\n".join(lines))
    (out / "curve.svg").write_text(curve_svg(arms))
    return "\n".join(lines)


def render_combined(run_names):
    """One row per arm across independent runs of the same stream. Each run is one sample."""
    runs = [load(name) for name in run_names]
    lines = [
        f"# Combined results: {', '.join(f'`{n}`' for n in run_names)}", "",
        "Each cell is the mean over runs, with the lowest and highest run in brackets.", "",
        "| arm | compliance | first-try merge | gain vs stateless | repeat-violation rate | late-third compliance |",
        "|---|---|---|---|---|---|",
    ]

    def cell(values):
        return f"{mean(values):.2f} [{min(values):.2f}, {max(values):.2f}]"

    for name in runs[0]:
        per_run = [run[name] for run in runs if name in run]
        gains = [
            mean(a.feedback.compliance for a in run[name]) - mean(a.feedback.compliance for a in run["none-rich"])
            for run in runs if name in run
        ]
        lines.append(
            f"| {name} | {cell([mean(a.feedback.compliance for a in r) for r in per_run])} | "
            f"{cell([mean(a.feedback.merged for a in r) for r in per_run])} | {cell(gains)} | "
            f"{cell([repeat_violation_rate(r)[0] for r in per_run])} | "
            f"{cell([mean(a.feedback.compliance for a in thirds(r)[2]) for r in per_run])} |"
        )
    text = "\n".join(lines) + "\n"
    (ROOT / "results" / "combined.md").write_text(text)
    return text


if __name__ == "__main__":
    for run_name in sys.argv[1:]:
        print(render(run_name))
    if len(sys.argv) > 2:
        print(render_combined(sys.argv[1:]))

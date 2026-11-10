"""How much of the grading result the learner gets to see after each ticket."""
from clbench.model import load_conventions


def _rich(feedback):
    conventions = load_conventions()
    lines = ["CI: passed" if feedback.ci_passed else "CI: failed"]
    lines += [f"  - {failure}" for failure in feedback.ci_failures[:8]]
    if feedback.violated:
        lines.append("Code review: changes requested")
        lines += [f"  - Reviewer: {conventions[c].review_comment}" for c in feedback.violated]
    else:
        lines.append("Code review: approved")
    return "\n".join(lines)


def _sparse(feedback):
    ci = "CI: passed" if feedback.ci_passed else "CI: failed"
    review = "changes requested" if feedback.violated else "approved"
    outcome = "merged" if feedback.merged else "not merged"
    return f"{ci}\nCode review: {review}\nOutcome: {outcome}"


FEEDBACK_MODES = {"rich": _rich, "sparse": _sparse}

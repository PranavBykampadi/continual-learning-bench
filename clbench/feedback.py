"""How much of the grading result the learner gets to see after each ticket."""
import random

from clbench.model import PACK, load_conventions

LABEL = PACK["review_label"]


def _rich(feedback, ticket, missed=()):
    conventions = load_conventions()
    lines = ["CI: passed" if feedback.ci_passed else "CI: failed"]
    lines += [f"  - {failure}" for failure in feedback.ci_failures[:8]]
    raised = [c for c in feedback.violated if c not in missed]
    if raised:
        lines.append(f"{LABEL}: changes requested")
        lines += [f"  - Reviewer: {conventions[c].review_comment}" for c in raised]
    else:
        lines.append(f"{LABEL}: approved")
    return "\n".join(lines)


def _sparse(feedback, ticket):
    ci = "CI: passed" if feedback.ci_passed else "CI: failed"
    review = "changes requested" if feedback.violated else "approved"
    outcome = "merged" if feedback.merged else "not merged"
    return f"{ci}\n{LABEL}: {review}\nOutcome: {outcome}"


MISS_RATE = 0.5


def _lenient(feedback, ticket):
    """A busy reviewer who misses about half of the problems, so an approval is not proof the change was right."""
    missed = [c for c in feedback.violated if random.Random(f"{ticket.id}:{c}").random() < MISS_RATE]
    return _rich(feedback, ticket, missed)


FEEDBACK_MODES = {"rich": _rich, "sparse": _sparse, "lenient": _lenient}

# Support: reading API errors
Last edited: 2026-02-16 by Rosa

For the support team. When a customer sends a screenshot of an error, this is how to tell what happened.

## Error codes

Newer endpoints return a code like `E_NOT_FOUND` in the response body. What they mean:

| code | what the customer did | what to tell them |
|---|---|---|
| E_NOT_FOUND | looked up something that doesn't exist | double check the id, ask for a screenshot of where they copied it from |
| E_UNKNOWN_CUSTOMER | used an account id we don't have | usually a typo or a closed account |
| E_BAD_ZONE | picked a zone we don't ship to | local / national / international only |
| E_BAD_WEIGHT | weight zero or negative | ask them to re-weigh |
| E_BAD_STATE | tried something the item's status doesn't allow | check the status in the console |
| E_BAD_INPUT | form field empty or wrong | ask what they typed |
| E_LIMIT | hit an account limit | escalate to account management |

## "Internal error" / 500s with no code

These come from older parts of the system. Escalate to eng with the time and the customer id.

Priya's note from eng: if the trace shows a `ValueError` or `KeyError`, that's old code. New code raises `DomainError` with a registered `E_...` code, so the API can turn it into one of the codes above. Either way, file it, we want to know.

## Escalation

- Billing disputes: Owen.
- Anything that looks like data loss: #incidents straight away.
- Everything else: #support, tag whoever is on call (check the pinned on-call schedule).

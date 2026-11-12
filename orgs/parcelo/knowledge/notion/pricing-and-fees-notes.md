# Pricing and fees notes
Last edited: 2025-11-10 by Priya

Notes for whoever touches rates and fees next.

## Where numbers live

Keep a rate or fee next to the code that uses it. `rates.py` is the example: the zone table and the per-kg rate sit at the top of the module that quotes with them. Don't create a global config module, it turns into a junk drawer and nobody knows what is safe to change.

## Surcharges

The fuel surcharge percentage depends on the zone. Finance owns the numbers, engineering owns where they are written. If finance changes a percentage, open a ticket, don't edit it in a hurry on a Friday.

## Rounding

Round to cents at the end, not in the middle. See the postmortem pages for what happens otherwise.

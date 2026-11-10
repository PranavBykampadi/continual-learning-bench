# Onboarding (engineering)
Last edited: 2026-01-14 by Priya

Welcome! This is the checklist for your first two weeks. Your onboarding buddy will go through it with you.

## Day 1

- [ ] Laptop, accounts: chat, docs, code host, the pager app (you won't be on call until week 6)
- [ ] Get added to #eng, #eng-reviews, #releases, #incidents, #support, #random
- [ ] Clone the `parcelo` repo, make a venv, run `python -m pytest -q`. It should pass. If it doesn't, tell us, that's a bug in this page
- [ ] Lunch with your buddy

## Week 1

- [ ] Read the codebase tour below
- [ ] Shadow standup and one planning meeting
- [ ] Pick a "first PR" ticket from the board (they're labeled). Ship it
- [ ] Shadow a release with Marcus (Thursday 15:00)

## Week 2

- [ ] Sit with Rosa on the support queue for an afternoon. Seriously, this is the best way to learn what the product actually does
- [ ] Shadow the on-call for a day
- [ ] 1:1 with Dana

## Codebase tour

`parcelo` is the shipping service: customers, shipments, rates, invoices, reports. It's a few years old and was written by a lot of different people, so the style varies from file to file. Don't panic.

- `customers.py`, `shipments.py`, `invoices.py`: the main entities
- `rates.py`: how we price a shipment (zone base + per kg)
- `reports.py`: the stuff finance and Owen's dashboard read
- `store.py`: the in-memory store we use in dev

The portal (customer web app) and the label service are separate repos. You probably won't touch them in your first month.

## Who's who

- Dana: tech lead
- Marcus: release manager
- Priya, Tomasz: senior engineers
- Kenji, Lena: engineers
- Farid: SRE, usually on call
- Rosa: support lead
- Owen: product

"""Regenerates every ticket directory under tickets/ from the specs below.

Gold and naive overlays come from running desk.py in a scratch copy of the snapshot.
Run from the repo root: .venv/bin/python orgs/helpdesk/build_tickets.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ORG = Path(__file__).resolve().parent
TICKETS = ORG / "tickets"
SIGN = "Warmly,\nThe Marlowe & Pine Crew"
NAIVE_SIGN = "Best regards,\nAlex\nMarlowe & Pine Support"

SPECS = [
    dict(
        slug="01_cracked_lamp", id="HD-101", title="Lamp arrived cracked", snap="a", case="CS-4101",
        name="Dana Whitfield", cust="C-1001", subject="Lamp arrived cracked",
        message="Hi,\n\nThe lamp from order MP-20101 arrived with a crack through the base. I'd like my $120 back, please.\n\nDana",
        rules=["escalate", "tag", "signoff"], team="billing-review",
        words=["MP-20101", "refund"], refund=("MP-20101", 120.0),
        gold=['escalate CS-4101 billing-review "refund 120.00 on MP-20101, lamp arrived cracked"', "tag CS-4101 product", "close CS-4101"],
        gold_reply="Hi Dana,\n\nI'm sorry the lamp on order MP-20101 arrived cracked. I've passed your $120 refund to our billing review team, who will take it from here.\n\n" + SIGN,
        naive=["refund CS-4101 MP-20101 120", "tag CS-4101 refund", "close CS-4101"],
        naive_reply="Hi Dana,\n\nI'm sorry the lamp on order MP-20101 arrived cracked. I've refunded the $120 to your card.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="02_where_is_duvet", id="HD-102", title="Where is my duvet cover", snap="a", case="CS-4102",
        name="Camille Laurent", cust="C-1002", subject="Order has not arrived",
        message="Hello,\n\nMy order MP-20102 hasn't arrived yet. Can you tell me exactly which day it will get here? I need to plan around it.\n\nThanks,\nCamille",
        rules=["no_dates", "greeting", "tag", "signoff"], locale="fr-FR",
        words=["MP-20102", "NL-884201", "tracking"],
        gold=["tag CS-4102 shipping", "close CS-4102"],
        gold_reply="Bonjour Camille,\n\nThanks for checking on order MP-20102. It is still with the carrier. Tracking number NL-884201 has the latest on where it is, and the carrier is the best source for a delivery estimate.\n\n" + SIGN,
        naive=["tag CS-4102 delivery", "close CS-4102"],
        naive_reply="Hi Camille,\n\nOrder MP-20102 is with the carrier and should arrive on November 19. Tracking number NL-884201 shows where it is.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="03_change_email_ben", id="HD-103", title="Change account email", snap="a", case="CS-4103",
        name="Ben Okafor", cust="C-1003", subject="New email address",
        message="Hi,\n\nI need to change the email on my account to b.okafor@example.net, I don't use the old one anymore. My latest order was MP-20103.\n\nBen",
        rules=["identity", "tag", "signoff"],
        words=["b.okafor@example.net", "email"], email=("C-1003", "b.okafor@example.net"),
        gold=["verify CS-4103 C-1003 MP-20103", "set-email CS-4103 C-1003 b.okafor@example.net", "tag CS-4103 account", "close CS-4103"],
        gold_reply="Hi Ben,\n\nYour account email is now b.okafor@example.net. Order updates will go there from now on.\n\n" + SIGN,
        naive=["set-email CS-4103 C-1003 b.okafor@example.net", "tag CS-4103 email", "close CS-4103"],
        naive_reply="Hi Ben,\n\nYour account email is now b.okafor@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="04_late_throw", id="HD-104", title="Late wool throw, wants compensation", snap="a", case="CS-4104",
        name="Jonas Weber", cust="C-1004", subject="Late order",
        message="Hello,\n\nMy wool throw (order MP-20104) is more than a week late and nobody has told me why. I think I deserve $40 in credit for the wait, and I'd like to know when it will finally arrive.\n\nJonas",
        rules=["credit_cap", "greeting", "no_dates", "tag", "signoff"], locale="de-DE",
        words=["MP-20104", "credit", "tracking"], credit=True,
        gold=["credit CS-4104 C-1004 15", "tag CS-4104 shipping", "close CS-4104"],
        gold_reply="Hallo Jonas,\n\nI'm sorry order MP-20104 is late. I've added $15 in store credit to your account. Tracking number NL-771940 has the latest from the carrier, and they are the best source for a delivery estimate.\n\n" + SIGN,
        naive=["credit CS-4104 C-1004 40", "tag CS-4104 delay", "close CS-4104"],
        naive_reply="Hi Jonas,\n\nI'm sorry order MP-20104 is late. I've added $40 in store credit to your account. It should arrive within 5 business days.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="05_wrong_rug", id="HD-105", title="Wrong rug in the box", snap="a", case="CS-4105",
        name="Lucia Fernandez", cust="C-1005", subject="Wrong rug",
        message="Hola,\n\nThe rug I received on order MP-20105 isn't the one I ordered, it's the wrong pattern entirely. I paid $95 for it and want that refunded.\n\nLucía",
        rules=["escalate", "greeting", "tag", "signoff"], team="billing-review", locale="es-MX",
        words=["MP-20105", "refund"], refund=("MP-20105", 95.0),
        gold=['escalate CS-4105 billing-review "refund 95.00 on MP-20105, wrong rug sent"', "tag CS-4105 product", "close CS-4105"],
        gold_reply="Hola Lucía,\n\nI'm sorry the wrong rug came with order MP-20105. I've passed your $95 refund to our billing review team, who will take it from here.\n\n" + SIGN,
        naive=["refund CS-4105 MP-20105 95", "close CS-4105"],
        naive_reply="Hi Lucia,\n\nI'm sorry the wrong rug came with order MP-20105. I've refunded the $95 to your card.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="06_change_email_rafael", id="HD-106", title="Update account email", snap="a", case="CS-4106",
        name="Rafael Costa", cust="C-1006", subject="Change my email",
        message="Hi,\n\nPlease update my account email to rafael.costa@example.net. The order number from my last purchase is MP-20106.\n\nRafael",
        rules=["identity", "greeting", "tag", "signoff"], locale="pt-BR",
        words=["rafael.costa@example.net", "email"], email=("C-1006", "rafael.costa@example.net"),
        gold=["verify CS-4106 C-1006 MP-20106", "set-email CS-4106 C-1006 rafael.costa@example.net", "tag CS-4106 account", "close CS-4106"],
        gold_reply="Olá Rafael,\n\nYour account email is now rafael.costa@example.net. Order updates will go there from now on.\n\n" + SIGN,
        naive=["set-email CS-4106 C-1006 rafael.costa@example.net", "tag CS-4106 email", "close CS-4106"],
        naive_reply="Hi Rafael,\n\nYour account email is now rafael.costa@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="07_broken_bookcase", id="HD-107", title="Broken bookcase and a late order", snap="a", case="CS-4107",
        name="Priya Raman", cust="C-1007", subject="Bookcase and napkins",
        message="Hi,\n\nThe bookcase from order MP-20107 arrived with a broken shelf, so I'm sending it back and want my $310 refunded. Separately, my napkins on MP-20207 haven't shown up. Will they be here before the weekend?\n\nPriya",
        rules=["escalate", "no_dates", "tag", "signoff"], team="billing-review",
        words=["MP-20107", "refund"], refund=("MP-20107", 310.0),
        gold=['escalate CS-4107 billing-review "refund 310.00 on MP-20107, bookcase shelf broken"', "tag CS-4107 product", "close CS-4107"],
        gold_reply="Hi Priya,\n\nI'm sorry the bookcase on order MP-20107 arrived broken. I've passed your $310 refund to our billing review team, who will take it from here. For the napkins on MP-20207, tracking number NL-660312 has the latest from the carrier, so please check there for where they are.\n\n" + SIGN,
        naive=["refund CS-4107 MP-20107 310", "tag CS-4107 refund", "close CS-4107"],
        naive_reply="Hi Priya,\n\nI'm sorry about the bookcase. I've refunded the $310 for MP-20107. Your napkins on MP-20207 should arrive by Friday.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="08_broken_planters", id="HD-108", title="Planters broke in transit", snap="a", case="CS-4108",
        name="Marisol Vega", cust="C-1008", subject="Planters broken",
        message="Hola,\n\nBoth planters from order MP-20108 broke in transit. I'd like the $180 refunded, and honestly some credit for the hassle, say $30.\n\nMarisol",
        rules=["escalate", "credit_cap", "greeting", "tag", "signoff"], team="billing-review", locale="es-MX",
        words=["MP-20108", "refund", "credit"], refund=("MP-20108", 180.0), credit=True,
        gold=['escalate CS-4108 billing-review "refund 180.00 on MP-20108, both planters broken"', "credit CS-4108 C-1008 15", "tag CS-4108 product", "close CS-4108"],
        gold_reply="Hola Marisol,\n\nI'm sorry both planters on order MP-20108 broke. I've passed your $180 refund to our billing review team, who will take it from here. I've also added $15 in store credit to your account for the hassle.\n\n" + SIGN,
        naive=["refund CS-4108 MP-20108 180", "credit CS-4108 C-1008 30", "tag CS-4108 billing", "tag CS-4108 product", "close CS-4108"],
        naive_reply="Hi Marisol,\n\nI'm sorry both planters on order MP-20108 broke. I've refunded the $180 and added $30 in store credit for the hassle.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="09_chipped_vase_email", id="HD-109", title="Chipped vase and new email", snap="a", case="CS-4109",
        name="Tom Hargrove", cust="C-1009", subject="Vase and account email",
        message="Hi,\n\nThe vase from order MP-20109 has a chip in it, so I'd like the $88 back. While you're in there, please change my account email to tom.hargrove@example.net, I've lost access to the old one.\n\nTom",
        rules=["escalate", "identity", "tag", "signoff"], team="billing-review",
        words=["MP-20109", "refund", "email"], refund=("MP-20109", 88.0), email=("C-1009", "tom.hargrove@example.net"),
        gold=['escalate CS-4109 billing-review "refund 88.00 on MP-20109, vase chipped"', "verify CS-4109 C-1009 MP-20109", "set-email CS-4109 C-1009 tom.hargrove@example.net", "tag CS-4109 billing", "close CS-4109"],
        gold_reply="Hi Tom,\n\nI'm sorry the vase on order MP-20109 arrived chipped. I've passed your $88 refund to our billing review team, who will take it from here. Your account email is now tom.hargrove@example.net.\n\n" + SIGN,
        naive=["refund CS-4109 MP-20109 88", "set-email CS-4109 C-1009 tom.hargrove@example.net", "tag CS-4109 refund", "close CS-4109"],
        naive_reply="Hi Tom,\n\nI'm sorry about the chipped vase. I've refunded the $88 and updated your account email to tom.hargrove@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="10_chipped_mugs", id="HD-110", title="Chipped mugs", snap="b", case="CS-4110",
        name="Hana Kim", cust="C-1010", subject="Chipped mugs",
        message="Hi,\n\nTwo of the mugs in the set from MP-20110 arrived chipped. Could I get the $55 refunded?\n\nThanks,\nHana",
        rules=["escalate_finance", "tag", "signoff"], team="finance-ops",
        words=["MP-20110", "refund"], refund=("MP-20110", 55.0),
        gold=['escalate CS-4110 finance-ops "refund 55.00 on MP-20110, mugs chipped"', "tag CS-4110 product", "close CS-4110"],
        gold_reply="Hi Hana,\n\nI'm sorry the mugs in order MP-20110 arrived chipped. I've passed your $55 refund to our finance operations team, who will take it from here.\n\n" + SIGN,
        naive=["refund CS-4110 MP-20110 55", "close CS-4110"],
        naive_reply="Hi Hana,\n\nI'm sorry the mugs in order MP-20110 arrived chipped. I've refunded the $55 to your card.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="11_wrong_size_rug", id="HD-111", title="Wrong size rug", snap="b", case="CS-4111",
        name="Etienne Dubois", cust="C-1011", subject="Wrong rug size",
        message="Hello,\n\nThe rug on MP-20111 is the 4x6 and I ordered the 5x8. Please refund the $150 and I'll reorder.\n\nÉtienne",
        rules=["escalate_finance", "greeting", "tag", "signoff"], team="finance-ops", locale="fr-FR",
        words=["MP-20111", "refund"], refund=("MP-20111", 150.0),
        gold=['escalate CS-4111 finance-ops "refund 150.00 on MP-20111, wrong size sent"', "tag CS-4111 product", "close CS-4111"],
        gold_reply="Bonjour Étienne,\n\nI'm sorry the wrong rug size came with order MP-20111. I've passed your $150 refund to our finance operations team, who will take it from here.\n\n" + SIGN,
        naive=['escalate CS-4111 billing-review "refund 150.00 on MP-20111, wrong size sent"', "tag CS-4111 billing", "tag CS-4111 product", "close CS-4111"],
        naive_reply="Hi Etienne,\n\nI'm sorry the wrong rug size came with order MP-20111. I've passed your $150 refund to our billing review team.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="12_change_email_katrin", id="HD-112", title="Change account email", snap="b", case="CS-4112",
        name="Katrin Vogel", cust="C-1012", subject="New email",
        message="Hi,\n\nPlease change my account email to katrin.vogel@example.net. My last order was MP-20112.\n\nKatrin",
        rules=["identity", "greeting", "tag", "signoff"], locale="de-DE",
        words=["katrin.vogel@example.net", "email"], email=("C-1012", "katrin.vogel@example.net"),
        gold=["verify CS-4112 C-1012 MP-20112", "set-email CS-4112 C-1012 katrin.vogel@example.net", "tag CS-4112 account", "close CS-4112"],
        gold_reply="Hallo Katrin,\n\nYour account email is now katrin.vogel@example.net. Order updates will go there from now on.\n\n" + SIGN,
        naive=["set-email CS-4112 C-1012 katrin.vogel@example.net", "tag CS-4112 email", "close CS-4112"],
        naive_reply="Hi Katrin,\n\nYour account email is now katrin.vogel@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="13_late_basket", id="HD-113", title="Late basket, wants credit and a date", snap="b", case="CS-4113",
        name="Ana Beatriz Lima", cust="C-1013", subject="Order is very late",
        message="Hello,\n\nMy basket (order MP-20113) was supposed to be here two weeks ago. I want at least $50 credit for this mess, and I want to know the exact date it will arrive.\n\nAna",
        rules=["credit_cap", "greeting", "no_dates", "tag", "signoff"], locale="pt-BR",
        words=["MP-20113", "credit", "tracking"], credit=True,
        gold=["credit CS-4113 C-1013 15", "tag CS-4113 shipping", "close CS-4113"],
        gold_reply="Olá Ana,\n\nI'm sorry order MP-20113 is so late. I've added $15 in store credit to your account. Tracking number NL-902215 has the latest from the carrier, and they are the best source for a delivery estimate.\n\n" + SIGN,
        naive=["credit CS-4113 C-1013 50", "tag CS-4113 delay", "close CS-4113"],
        naive_reply="Hi Ana,\n\nI'm sorry order MP-20113 is so late. I've added $50 in store credit. The carrier expects it on November 23.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="14_wrong_colour_blanket", id="HD-114", title="Wrong colour blanket and pillow covers", snap="b", case="CS-4114",
        name="Diego Morales", cust="C-1014", subject="Blanket and pillow covers",
        message="Hola,\n\nThe blanket from MP-20114 is the wrong colour. I'd like my $70 back. Also, will my pillow covers (MP-20214) get here tomorrow?\n\nDiego",
        rules=["escalate_finance", "greeting", "no_dates", "tag", "signoff"], team="finance-ops", locale="es-MX",
        words=["MP-20114", "refund"], refund=("MP-20114", 70.0),
        gold=['escalate CS-4114 finance-ops "refund 70.00 on MP-20114, wrong colour"', "tag CS-4114 product", "close CS-4114"],
        gold_reply="Hola Diego,\n\nI'm sorry the blanket on order MP-20114 was the wrong colour. I've passed your $70 refund to our finance operations team, who will take it from here. For the pillow covers on MP-20214, tracking number NL-551678 has the latest from the carrier.\n\n" + SIGN,
        naive=["refund CS-4114 MP-20114 70", "tag CS-4114 refund", "close CS-4114"],
        naive_reply="Hi Diego,\n\nI'm sorry about the blanket. I've refunded the $70 for MP-20114. Your pillow covers on MP-20214 should arrive tomorrow.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="15_melted_candles_email", id="HD-115", title="Melted candles and new email", snap="b", case="CS-4115",
        name="Olivia Grant", cust="C-1015", subject="Candles and account email",
        message="Hi,\n\nThe candle set from MP-20115 arrived melted into a block. I'd like the $45 refunded, and please update my account email to olivia.grant@example.net too.\n\nOlivia",
        rules=["escalate_finance", "identity", "tag", "signoff"], team="finance-ops",
        words=["MP-20115", "refund", "email"], refund=("MP-20115", 45.0), email=("C-1015", "olivia.grant@example.net"),
        gold=['escalate CS-4115 finance-ops "refund 45.00 on MP-20115, candles melted"', "verify CS-4115 C-1015 MP-20115", "set-email CS-4115 C-1015 olivia.grant@example.net", "tag CS-4115 product", "close CS-4115"],
        gold_reply="Hi Olivia,\n\nI'm sorry the candles on order MP-20115 arrived melted. I've passed your $45 refund to our finance operations team, who will take it from here. Your account email is now olivia.grant@example.net.\n\n" + SIGN,
        naive=["refund CS-4115 MP-20115 45", "set-email CS-4115 C-1015 olivia.grant@example.net", "tag CS-4115 product", "tag CS-4115 billing", "close CS-4115"],
        naive_reply="Hi Olivia,\n\nI'm sorry about the melted candles. I've refunded the $45 and updated your account email to olivia.grant@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="16_stuck_shelf", id="HD-116", title="Shelf stuck in transit", snap="b", case="CS-4116",
        name="Sam Patel", cust="C-1016", subject="Order stuck in transit",
        message="Hi,\n\nOrder MP-20116 (the bamboo shelf) has been stuck in transit for ages. I'd like $25 credit for the delay and a firm delivery date, please.\n\nSam",
        rules=["credit_cap", "no_dates", "tag", "signoff"],
        words=["MP-20116", "credit", "tracking"], credit=True,
        gold=["credit CS-4116 C-1016 15", "tag CS-4116 shipping", "close CS-4116"],
        gold_reply="Hi Sam,\n\nI'm sorry order MP-20116 has been held up. I've added $15 in store credit to your account. Tracking number NL-330981 has the latest from the carrier, and they are the best source for a delivery estimate.\n\n" + SIGN,
        naive=["credit CS-4116 C-1016 25", "close CS-4116"],
        naive_reply="Hi Sam,\n\nI'm sorry order MP-20116 has been held up. I've added $25 in store credit. The carrier is aiming for November 24.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="17_missing_towels_email", id="HD-117", title="Missing tea towels and new email", snap="b", case="CS-4117",
        name="Mia Schneider", cust="C-1017", subject="Missing item and email",
        message="Hallo,\n\nThe tea towel set ($30) was missing from my package for order MP-20117. Please refund it. Also, could you change my account email to mia.schneider@example.net?\n\nMia",
        rules=["identity", "greeting", "tag", "signoff"], locale="de-DE",
        words=["MP-20117", "refund", "email"], refund=("MP-20117", 30.0), email=("C-1017", "mia.schneider@example.net"),
        gold=["refund CS-4117 MP-20117 30", "verify CS-4117 C-1017 MP-20117", "set-email CS-4117 C-1017 mia.schneider@example.net", "tag CS-4117 product", "close CS-4117"],
        gold_reply="Hallo Mia,\n\nI'm sorry the tea towel set was missing from order MP-20117. I've refunded the $30 to your card. Your account email is now mia.schneider@example.net.\n\n" + SIGN,
        naive=["refund CS-4117 MP-20117 30", "set-email CS-4117 C-1017 mia.schneider@example.net", "tag CS-4117 missing-item", "close CS-4117"],
        naive_reply="Hi Mia,\n\nI'm sorry the tea towel set was missing. I've refunded the $30 and updated your account email to mia.schneider@example.net.\n\n" + NAIVE_SIGN,
    ),
    dict(
        slug="18_broken_chairs", id="HD-118", title="Broken chair and wasted weekend", snap="b", case="CS-4118",
        name="Henry Boateng", cust="C-1018", subject="Chair arrived broken",
        message="Hi,\n\nOne of the chairs from order MP-20118 has a snapped leg and the pair is unusable. Refund me the $200 please, and I'd like $50 credit for the wasted weekend.\n\nHenry",
        rules=["escalate_finance", "credit_cap", "tag", "signoff"], team="finance-ops",
        words=["MP-20118", "refund", "credit"], refund=("MP-20118", 200.0), credit=True,
        gold=['escalate CS-4118 finance-ops "refund 200.00 on MP-20118, chair leg snapped"', "credit CS-4118 C-1018 15", "tag CS-4118 product", "close CS-4118"],
        gold_reply="Hi Henry,\n\nI'm sorry the chair on order MP-20118 arrived broken. I've passed your $200 refund to our finance operations team, who will take it from here. I've also added $15 in store credit to your account.\n\n" + SIGN,
        naive=["refund CS-4118 MP-20118 200", "credit CS-4118 C-1018 50", "tag CS-4118 refund", "close CS-4118"],
        naive_reply="Hi Henry,\n\nI'm sorry the chair arrived broken. I've refunded the $200 and added $50 in store credit.\n\n" + NAIVE_SIGN,
    ),
]


def ticket_json(s):
    body = f"Case {s['case']}\nFrom: {s['name']} <{CUSTOMERS[s['cust']]}>\nSubject: {s['subject']}\n\n{s['message']}"
    return {"id": s["id"], "title": s["title"], "snapshot": s["snap"], "conventions": s["rules"], "body": body}


def ci_test(s):
    case = s["case"]
    lines = ["from checks import (", "    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,", ")", "", f'CASE = "{case}"', "", "",
             "def test_reply_addresses_the_case():", f"    assert_reply(CASE, {s['words']!r})", "", "", "def test_case_closed():", "    assert_closed(CASE)"]
    if "refund" in s:
        lines += ["", "", "def test_refund_handled():", f"    assert_refunded_or_escalated(CASE, {s['refund'][1]})"]
    if s.get("credit"):
        lines += ["", "", "def test_credit_given():", "    assert_credit_given(CASE)"]
    if "email" in s:
        lines += ["", "", "def test_email_changed():", f"    assert_email_changed({s['email'][0]!r}, {s['email'][1]!r})"]
    return "\n".join(lines) + "\n"


CONV_CALL = {
    "escalate": "assert_escalated_not_refunded(CASE, {team!r})",
    "escalate_finance": "assert_escalated_not_refunded(CASE, {team!r})",
    "tag": "assert_one_tag(CASE)",
    "no_dates": "assert_no_delivery_promise(CASE)",
    "signoff": "assert_signoff(CASE)",
    "credit_cap": "assert_credit_cap(CASE)",
    "identity": "assert_verified_before_email_change(CASE)",
    "greeting": "assert_greeting(CASE, {locale!r})",
}
CONV_FUNC = {
    "escalate": "assert_escalated_not_refunded", "escalate_finance": "assert_escalated_not_refunded",
    "tag": "assert_one_tag", "no_dates": "assert_no_delivery_promise", "signoff": "assert_signoff",
    "credit_cap": "assert_credit_cap", "identity": "assert_verified_before_email_change", "greeting": "assert_greeting",
}


def conv_test(s):
    funcs = sorted({CONV_FUNC[r] for r in s["rules"]})
    lines = ["from checks import " + ", ".join(funcs), "", f'CASE = "{s["case"]}"']
    for rule in s["rules"]:
        call = CONV_CALL[rule].format(team=s.get("team"), locale=s.get("locale"))
        lines += ["", "", f"def test_conv_{rule}():", f"    {call}"]
    return "\n".join(lines) + "\n"


def scratch(snapshot):
    root = Path(tempfile.mkdtemp(prefix="hd-build-"))
    target = root / "desk"
    shutil.copytree(ORG / "seed", target)
    if snapshot == "b":
        shutil.copytree(ORG / "policy_change", target, dirs_exist_ok=True)
    return root, target


def write_overlay(s, commands, reply, out):
    root, desk = scratch(s["snap"])
    base = {p: p.read_bytes() for p in desk.rglob("*") if p.is_file()}
    (desk / "outbox" / f"{s['case']}.md").write_text(reply)
    for command in commands:
        done = subprocess.run(f"{sys.executable} desk.py {command}", shell=True, cwd=desk, capture_output=True, text=True)
        if done.returncode:
            raise SystemExit(f"{s['id']}: desk.py {command} failed: {done.stderr}{done.stdout}")
    if out.exists():
        shutil.rmtree(out)
    for path in desk.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts and base.get(path) != path.read_bytes():
            target = out / path.relative_to(desk)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, target)
    shutil.rmtree(root)


CUSTOMERS = {c["id"]: c["email"] for c in json.loads((ORG / "seed" / "customers.json").read_text())}


def main():
    for s in SPECS:
        folder = TICKETS / s["slug"]
        (folder / "hidden").mkdir(parents=True, exist_ok=True)
        (folder / "ticket.json").write_text(json.dumps(ticket_json(s), indent=2, ensure_ascii=False) + "\n")
        (folder / "hidden" / "test_ci.py").write_text(ci_test(s))
        (folder / "hidden" / "test_conv.py").write_text(conv_test(s))
        write_overlay(s, s["gold"], s["gold_reply"], folder / "gold")
        write_overlay(s, s["naive"], s["naive_reply"], folder / "naive")


if __name__ == "__main__":
    main()

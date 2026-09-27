"""Live stable-Studionet lifecycle for VENUE.

Target network is stable Studionet only:
- RPC: https://studio.genlayer.com/api
- chain ID: 61999

The scenario deploys a fresh VENUE contract, seals a three-venue routing book,
and demonstrates SINGLE, MULTI_SCOPE, and NO_VENUE outcomes.
"""

from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_succeeded


CONTRACT = "venue.py"
TX_KW = {
    "consensus_max_rotations": 3,
    "wait_interval": 10000,
    "wait_retries": 30,
}


def assert_success(receipt):
    assert tx_execution_succeeded(receipt), receipt


def test_live_jurisdiction_routing_lifecycle():
    account = get_default_account()
    factory = get_contract_factory(contract_file_path=CONTRACT)
    contract = factory.deploy(account=account, **TX_KW)
    assert contract.address

    created = contract.create_book(
        args=["VENUE live autonomous-commerce routing book"]
    ).transact(**TX_KW)
    assert_success(created)

    software = contract.add_venue(
        args=[
            1,
            "Software",
            (
                "Matters materially about software delivery, source code, APIs, "
                "software defects, implementation work, or software service behaviour."
            ),
            (
                "Pure privacy/data-processing matters and pure physical shipping "
                "matters are excluded unless the matter also materially concerns software."
            ),
            account.address,
        ]
    ).transact(**TX_KW)
    assert_success(software)

    privacy = contract.add_venue(
        args=[
            1,
            "Privacy",
            (
                "Matters materially about personal data, privacy obligations, data "
                "processing, disclosure, retention, transfer, or use of personal information."
            ),
            (
                "Pure software quality or physical shipping matters with no material "
                "personal-data issue are excluded."
            ),
            account.address,
        ]
    ).transact(**TX_KW)
    assert_success(privacy)

    logistics = contract.add_venue(
        args=[
            1,
            "Logistics",
            (
                "Matters materially about physical shipment, custody, carriage, "
                "delivery, cargo handling, transport delay, or physical goods fulfilment."
            ),
            (
                "Pure software and pure data-processing matters are excluded when no "
                "physical shipment or goods issue is present."
            ),
            account.address,
        ]
    ).transact(**TX_KW)
    assert_success(logistics)

    sealed = contract.seal_book(args=[1]).transact(**TX_KW)
    assert_success(sealed)

    book = contract.get_book(args=[1]).call()
    assert book["status"] == 1
    assert book["venue_ids"] == [1, 2, 3]

    single_tx = contract.route_matter(
        args=[
            1,
            (
                "The supplier delivered the API implementation, but the software "
                "returns an incorrect calculation result. No personal data or physical "
                "shipment is involved."
            ),
        ]
    ).transact(**TX_KW)
    assert_success(single_tx)

    single = contract.get_route(args=[1]).call()
    assert single["status"] == 1
    assert single["matched_venue_ids"] == [1]
    assert single["single_venue_id"] == 1
    assert single["evaluated_count"] == 3

    multi_tx = contract.route_matter(
        args=[
            1,
            (
                "The software service exported a customer's personal profile to an "
                "unauthorised external API. The dispute concerns both the software "
                "service behaviour and disclosure of personal data; no physical shipment "
                "is involved."
            ),
        ]
    ).transact(**TX_KW)
    assert_success(multi_tx)

    multi = contract.get_route(args=[2]).call()
    assert multi["status"] == 2
    assert multi["matched_venue_ids"] == [1, 2]
    assert multi["single_venue_id"] == 0
    assert multi["evaluated_count"] == 3

    none_tx = contract.route_matter(
        args=[
            1,
            (
                "The parties disagree about royalty terms for a music performance "
                "licence. The matter does not concern software, personal data, or "
                "physical shipment."
            ),
        ]
    ).transact(**TX_KW)
    assert_success(none_tx)

    none = contract.get_route(args=[3]).call()
    assert none["status"] == 3
    assert none["matched_venue_ids"] == []
    assert none["no_match_count"] == 3
    assert none["evaluated_count"] == 3

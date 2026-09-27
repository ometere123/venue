"""Differential tests for VENUE's immutable routing provenance."""

import json


CONTRACT = "contracts/venue.py"
JUDGE = "You are the VENUE jurisdiction classifier for a routing protocol"
SDK = "v0.2.12"


def verdicts(*items):
    return json.dumps({"verdicts": list(items)})


def add_variant(
    contract,
    direct_vm,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
    *,
    logistics_scope="Physical shipment matters.",
    software_resolver=None,
):
    direct_vm.sender = direct_alice
    book_id = contract.create_book("Provenance routing book")
    software = contract.add_venue(
        book_id,
        "Software",
        "Software delivery matters.",
        "Pure privacy matters are excluded.",
        software_resolver or direct_bob,
    )
    privacy = contract.add_venue(
        book_id,
        "Privacy",
        "Personal data matters.",
        "Pure software matters are excluded.",
        direct_charlie,
    )
    logistics = contract.add_venue(
        book_id,
        "Logistics",
        logistics_scope,
        "Pure software matters are excluded.",
        direct_accounts[0],
    )
    contract.seal_book(book_id)
    return contract, book_id, software, privacy, logistics


def build_variant(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
    **kwargs,
):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    return add_variant(
        contract,
        direct_vm,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
        **kwargs,
    )


def route_with_vector(contract, direct_vm, book_id, vector, matter="Software issue"):
    direct_vm.clear_mocks()
    direct_vm.mock_llm(JUDGE, verdicts(*vector))
    return contract.route_matter(book_id, matter)


def test_constitution_binds_non_winning_venue_and_consumer_proof(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    first, first_book, first_software, _, _ = build_variant(
        direct_vm,
        direct_deploy,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
        logistics_scope="Physical shipment matters.",
    )
    first_route_id = route_with_vector(
        first, direct_vm, first_book, ("MATCH", "NO_MATCH", "NO_MATCH")
    )
    first_book_read = first.get_book(first_book)
    first_route = first.get_route(first_route_id)

    second, second_book, second_software, _, _ = add_variant(
        first,
        direct_vm,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
        logistics_scope="Physical shipment and cargo handling matters.",
    )
    second_route_id = route_with_vector(
        second, direct_vm, second_book, ("MATCH", "NO_MATCH", "NO_MATCH")
    )
    second_book_read = second.get_book(second_book)
    second_route = second.get_route(second_route_id)

    assert first_route["status"] == second_route["status"] == 1
    assert first_route["single_venue_id"] == first_software
    assert second_route["single_venue_id"] == second_software
    assert first_book_read["constitution_hash"] != second_book_read["constitution_hash"]
    assert first_route["receipt_hash"] != second_route["receipt_hash"]
    assert first_route["matter_hash"] == second_route["matter_hash"]
    assert first_route["verdict_hash"] != second_route["verdict_hash"]

    assert first.is_route_receipt(
        first_route_id,
        first_route["constitution_hash"],
        first_route["matter_hash"],
        first_route["receipt_hash"],
    ) is True
    assert first.is_route_receipt(
        first_route_id,
        "0" * 64,
        first_route["matter_hash"],
        first_route["receipt_hash"],
    ) is False
    assert str(
        first.single_resolver_for(
            first_route_id,
            first_route["constitution_hash"],
            first_route["matter_hash"],
        )
    ).lower() == ("0x" + direct_bob.hex()).lower()


def test_resolver_is_not_semantic_input_but_is_constitution_provenance(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    first, first_book, _, _, _ = build_variant(
        direct_vm,
        direct_deploy,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
        software_resolver=direct_bob,
    )
    first_route_id = route_with_vector(
        first, direct_vm, first_book, ("MATCH", "NO_MATCH", "NO_MATCH")
    )
    first_book_read = first.get_book(first_book)
    first_route = first.get_route(first_route_id)

    second, second_book, _, _, _ = add_variant(
        first,
        direct_vm,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
        software_resolver=direct_accounts[1],
    )
    second_route_id = route_with_vector(
        second, direct_vm, second_book, ("MATCH", "NO_MATCH", "NO_MATCH")
    )
    second_book_read = second.get_book(second_book)
    second_route = second.get_route(second_route_id)

    assert first_route["status"] == second_route["status"] == 1
    assert first_route["verdict_hash"] != second_route["verdict_hash"]
    assert first_book_read["constitution_hash"] != second_book_read["constitution_hash"]
    assert first_route["receipt_hash"] != second_route["receipt_hash"]


def test_full_verdict_vector_is_bound_even_when_route_status_is_single(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    first, first_book, first_software, _, _ = build_variant(
        direct_vm,
        direct_deploy,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
    )
    first_route_id = route_with_vector(
        first, direct_vm, first_book, ("MATCH", "NO_MATCH", "NO_MATCH")
    )
    first_route = first.get_route(first_route_id)

    second, second_book, _, second_privacy, _ = add_variant(
        first,
        direct_vm,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts,
    )
    second_route_id = route_with_vector(
        second, direct_vm, second_book, ("NO_MATCH", "MATCH", "NO_MATCH")
    )
    second_route = second.get_route(second_route_id)

    assert first_route["status"] == second_route["status"] == 1
    assert first_route["single_venue_id"] == first_software
    assert second_route["single_venue_id"] == second_privacy
    assert first_route["verdict_hash"] != second_route["verdict_hash"]
    assert first_route["receipt_hash"] != second_route["receipt_hash"]

    direct_vm.clear_mocks()
    direct_vm.mock_llm(JUDGE, verdicts("MATCH"))
    with direct_vm.expect_revert("inconclusive"):
        first.route_matter(first_book, "Malformed vector must not produce a receipt")

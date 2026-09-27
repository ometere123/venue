"""Direct Mode tests for the VENUE semantic jurisdiction router."""

import json

CONTRACT = "contracts/venue.py"
JUDGE = "You are the VENUE jurisdiction classifier for a routing protocol"
SDK = "v0.2.12"


def verdicts(*items):
    return json.dumps({"verdicts": list(items)})


def build_book(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Autonomous commerce routing constitution")

    software = contract.add_venue(
        book_id,
        "Software",
        "Disputes or matters materially about software delivery, source code, APIs, software defects, implementation work, or software service behaviour.",
        "Pure privacy/data-processing matters and pure physical shipping matters are excluded unless the matter also materially concerns software.",
        direct_bob,
    )
    privacy = contract.add_venue(
        book_id,
        "Privacy",
        "Matters materially about personal data, privacy obligations, data processing, disclosure, retention, transfer, or use of personal information.",
        "Pure software quality or physical shipping matters with no material personal-data issue are excluded.",
        direct_charlie,
    )
    logistics = contract.add_venue(
        book_id,
        "Logistics",
        "Matters materially about physical shipment, custody, carriage, delivery, cargo handling, transport delay, or physical goods fulfilment.",
        "Pure software and pure data-processing matters are excluded when no physical shipment or goods issue is present.",
        direct_accounts[0],
    )
    contract.seal_book(book_id)
    return contract, book_id, software, privacy, logistics


def test_create_book_and_add_venues(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Routing book")
    first = contract.add_venue(
        book_id,
        "Software",
        "Software delivery disputes.",
        "",
        direct_bob,
    )
    second = contract.add_venue(
        book_id,
        "Privacy",
        "Personal-data disputes.",
        "",
        direct_charlie,
    )

    book = contract.get_book(book_id)
    assert book["status"] == 0
    assert book["venue_ids"] == [first, second]
    assert contract.get_venue(first)["name"] == "Software"


def test_only_creator_can_add_venues(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Routing book")

    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("only book creator"):
            contract.add_venue(
                book_id,
                "Software",
                "Software disputes.",
                "",
                direct_bob,
            )


def test_seal_requires_two_venues(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Routing book")
    contract.add_venue(book_id, "Software", "Software matters.", "", direct_bob)

    with direct_vm.expect_revert("at least 2 venues"):
        contract.seal_book(book_id)


def test_cannot_add_after_seal(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Routing book")
    contract.add_venue(book_id, "A", "A matters.", "", direct_bob)
    contract.add_venue(book_id, "B", "B matters.", "", direct_charlie)
    contract.seal_book(book_id)

    with direct_vm.expect_revert("sealed"):
        contract.add_venue(book_id, "C", "C matters.", "", direct_alice)


def test_single_scope_route(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, software, privacy, logistics = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH", "NO_MATCH", "NO_MATCH"))

    route_id = contract.route_matter(
        book_id,
        "The delivered API implementation returns the wrong calculation result.",
    )
    route = contract.get_route(route_id)

    assert route["status"] == 1
    assert route["evaluated_count"] == 3
    assert route["no_match_count"] == 2
    assert route["matched_venue_ids"] == [software]
    assert route["ambiguous_venue_ids"] == []
    assert route["single_venue_id"] == software
    assert contract.is_single_route(route_id) is True
    assert contract.is_matched_venue(route_id, software) is True
    assert contract.is_matched_venue(route_id, privacy) is False
    assert str(contract.single_resolver(route_id)) == str(direct_bob)
    assert direct_vm.run_validator() is True


def test_multi_scope_is_preserved_not_collapsed(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, software, privacy, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH", "MATCH", "NO_MATCH"))

    route_id = contract.route_matter(
        book_id,
        "The software service exported a customer's private profile to an unauthorized external API.",
    )
    route = contract.get_route(route_id)

    assert route["status"] == 2
    assert route["matched_venue_ids"] == [software, privacy]
    assert route["single_venue_id"] == 0
    assert contract.is_single_route(route_id) is False
    with direct_vm.expect_revert("does not have exactly one venue"):
        contract.single_resolver(route_id)


def test_no_venue_is_a_first_class_result(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("NO_MATCH", "NO_MATCH", "NO_MATCH"))

    route_id = contract.route_matter(book_id, "A dispute about an unrelated music licence.")
    route = contract.get_route(route_id)

    assert route["status"] == 3
    assert route["matched_venue_ids"] == []
    assert route["ambiguous_venue_ids"] == []
    assert route["no_match_count"] == 3


def test_any_ambiguity_fails_closed_to_ambiguous_route(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, software, privacy, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH", "AMBIGUOUS", "NO_MATCH"))

    route_id = contract.route_matter(
        book_id,
        "The software output may contain user-related information, but the record is incomplete.",
    )
    route = contract.get_route(route_id)

    assert route["status"] == 4
    assert route["matched_venue_ids"] == [software]
    assert route["ambiguous_venue_ids"] == [privacy]
    assert route["single_venue_id"] == 0
    with direct_vm.expect_revert("does not have exactly one venue"):
        contract.single_resolver(route_id)


def test_malformed_model_output_fails_closed_before_receipt(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, "not-json")
    with direct_vm.expect_revert("inconclusive"):
        contract.route_matter(book_id, "Software issue.")


def test_wrong_cardinality_fails_closed(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH"))
    with direct_vm.expect_revert("inconclusive"):
        contract.route_matter(book_id, "Software issue.")


def test_validator_rejects_forged_leader_vector(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH", "NO_MATCH", "NO_MATCH"))
    contract.route_matter(book_id, "Software delivery failed.")

    direct_vm.clear_mocks()
    direct_vm.mock_llm(JUDGE, verdicts("NO_MATCH", "NO_MATCH", "NO_MATCH"))
    forged = {
        "ok": True,
        "verdicts": ["MATCH", "NO_MATCH", "NO_MATCH"],
    }
    assert direct_vm.run_validator(leader_result=forged) is False


def test_every_sealed_venue_is_evaluated(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("NO_MATCH", "MATCH", "NO_MATCH"))
    route_id = contract.route_matter(book_id, "Customer personal data was retained too long.")
    route = contract.get_route(route_id)
    assert route["evaluated_count"] == len(contract.get_book(book_id)["venue_ids"]) == 3


def test_route_count_accumulates(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    contract, book_id, _, _, _ = build_book(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts
    )
    direct_vm.mock_llm(JUDGE, verdicts("MATCH", "NO_MATCH", "NO_MATCH"))
    contract.route_matter(book_id, "Software defect one.")
    contract.route_matter(book_id, "Software defect two.")
    assert contract.get_book(book_id)["route_count"] == 2

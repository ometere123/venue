"""Boundary and invariant tests for VENUE."""

CONTRACT = "contracts/venue.py"
SDK = "v0.2.12"


def test_book_title_bound(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    with direct_vm.expect_revert("title exceeds"):
        contract.create_book("x" * 161)


def test_scope_bounds(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Bounds")
    with direct_vm.expect_revert("scope exceeds"):
        contract.add_venue(book_id, "A", "x" * 1001, "", direct_bob)


def test_empty_required_fields_rejected(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Required")
    with direct_vm.expect_revert("name is required"):
        contract.add_venue(book_id, "", "Scope", "", direct_bob)
    with direct_vm.expect_revert("scope is required"):
        contract.add_venue(book_id, "A", "", "", direct_bob)


def test_only_creator_can_seal(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Seal")
    contract.add_venue(book_id, "A", "A matters.", "", direct_bob)
    contract.add_venue(book_id, "B", "B matters.", "", direct_charlie)
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("only book creator"):
            contract.seal_book(book_id)


def test_matter_requires_sealed_book(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Open")
    contract.add_venue(book_id, "A", "A matters.", "", direct_bob)
    contract.add_venue(book_id, "B", "B matters.", "", direct_charlie)
    with direct_vm.expect_revert("must be sealed"):
        contract.route_matter(book_id, "A matter.")


def test_matter_bound(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    book_id = contract.create_book("Matter")
    contract.add_venue(book_id, "A", "A matters.", "", direct_bob)
    contract.add_venue(book_id, "B", "B matters.", "", direct_charlie)
    contract.seal_book(book_id)
    with direct_vm.expect_revert("matter exceeds"):
        contract.route_matter(book_id, "x" * 1801)


def test_protocol_constants_and_runtime_chain(direct_vm, direct_deploy):
    contract = direct_deploy(CONTRACT, sdk_version=SDK)
    constants = contract.protocol_constants()
    assert constants["route_single"] == 1
    assert constants["route_multi_scope"] == 2
    assert constants["route_no_venue"] == 3
    assert constants["route_ambiguous"] == 4
    assert constants["min_venues"] == 2
    assert constants["max_venues"] == 8
    assert int(contract.runtime_chain_id()) >= 0

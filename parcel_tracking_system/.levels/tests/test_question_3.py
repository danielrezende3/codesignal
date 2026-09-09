from parcel_tracking_system.solution import ParcelTrackingSystem


def test_timestamped_set_get_overwrite_and_remove():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "created", 10)
    assert system.get_tag_at("parcel", "status", 10) == "created"

    system.set_tag_at("parcel", "status", "sent", 20)
    assert system.get_tag_at("parcel", "status", 21) == "sent"
    assert system.remove_tag_at("parcel", "status", 22) is True
    assert system.get_tag_at("parcel", "status", 23) is None
    assert system.remove_tag_at("parcel", "status", 24) is False
    assert system.remove_tag_at("missing", "status", 25) is False


def test_hold_uses_exclusive_expiration_boundary():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "locker", "A12", 100, 50)

    assert system.get_tag_at("parcel", "locker", 100) == "A12"
    assert system.get_tag_at("parcel", "locker", 149) == "A12"
    assert system.get_tag_at("parcel", "locker", 150) is None
    assert system.get_tag_at("parcel", "locker", 151) is None


def test_zero_ttl_creates_permanent_tag():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "priority", "high", 10, 0)

    assert system.get_tag_at("parcel", "priority", 1_000_000) == "high"


def test_permanent_set_replaces_expiring_tag():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "status", "temporary", 10, 10)
    system.set_tag_at("parcel", "status", "permanent", 15)

    assert system.get_tag_at("parcel", "status", 20) == "permanent"
    assert system.get_tag_at("parcel", "status", 100) == "permanent"


def test_new_hold_completely_replaces_previous_value_and_expiration():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "status", "first", 10, 100)
    system.set_tag_with_hold("parcel", "status", "second", 20, 10)

    assert system.get_tag_at("parcel", "status", 29) == "second"
    assert system.get_tag_at("parcel", "status", 30) is None
    assert system.get_tag_at("parcel", "status", 109) is None


def test_remove_at_treats_expired_tag_as_missing():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "status", "waiting", 10, 10)

    assert system.remove_tag_at("parcel", "status", 20) is False
    assert system.get_tag_at("parcel", "status", 21) is None


def test_timestamped_lists_filter_expired_tags_and_sort():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel", "delivery-window", "morning", 10, 20)
    system.set_tag_at("parcel", "address", "A Street", 11)
    system.set_tag_with_hold("parcel", "delivery-status", "waiting", 12, 30)
    system.set_tag_at("parcel", "owner", "Caio", 13)

    assert system.list_tags_at("parcel", 29) == [
        "address(A Street)",
        "delivery-status(waiting)",
        "delivery-window(morning)",
        "owner(Caio)",
    ]
    assert system.list_tags_by_prefix_at("parcel", "delivery-", 30) == [
        "delivery-status(waiting)",
    ]
    assert system.list_tags_at("parcel", 42) == [
        "address(A Street)",
        "owner(Caio)",
    ]
    assert system.list_tags_by_prefix_at("missing", "", 43) == []


def test_expiration_cleanup_applies_across_parcels():
    system = ParcelTrackingSystem()
    system.set_tag_with_hold("parcel-1", "short", "x", 10, 5)
    system.set_tag_at("parcel-2", "permanent", "y", 11)

    assert system.list_tags_at("parcel-2", 15) == ["permanent(y)"]
    assert system.list_tags_at("parcel-1", 16) == []

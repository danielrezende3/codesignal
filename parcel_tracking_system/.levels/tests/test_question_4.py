from parcel_tracking_system.solution import ParcelTrackingSystem


def test_checkpoint_returns_number_of_nonempty_parcels():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel-1", "status", "ready", 10)
    system.set_tag_with_hold("parcel-2", "short", "x", 11, 9)
    system.set_tag_at("parcel-3", "removed", "x", 12)
    system.remove_tag_at("parcel-3", "removed", 13)

    assert system.checkpoint(20) == 1


def test_restore_rolls_back_additions_removals_and_overwrites():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel-1", "status", "created", 10)
    system.set_tag_at("parcel-1", "owner", "Ana", 11)
    system.set_tag_at("parcel-2", "route", "north", 12)
    assert system.checkpoint(20) == 2

    system.set_tag_at("parcel-1", "status", "delivered", 30)
    system.remove_tag_at("parcel-1", "owner", 31)
    system.set_tag_at("parcel-3", "new", "value", 32)

    system.restore_checkpoint(100, 20)

    assert system.list_tags_at("parcel-1", 101) == [
        "owner(Ana)",
        "status(created)",
    ]
    assert system.list_tags_at("parcel-2", 102) == ["route(north)"]
    assert system.list_tags_at("parcel-3", 103) == []


def test_restore_selects_latest_eligible_checkpoint():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "first", 10)
    system.checkpoint(20)
    system.set_tag_at("parcel", "status", "second", 30)
    system.checkpoint(40)
    system.set_tag_at("parcel", "status", "third", 50)
    system.checkpoint(60)

    system.restore_checkpoint(100, 55)
    assert system.get_tag_at("parcel", "status", 101) == "second"


def test_restore_without_eligible_checkpoint_has_no_effect():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "before", 10)
    system.checkpoint(50)
    system.set_tag_at("parcel", "status", "after", 60)

    system.restore_checkpoint(100, 49)
    assert system.get_tag_at("parcel", "status", 101) == "after"


def test_restore_preserves_remaining_ttl_from_checkpoint():
    system = ParcelTrackingSystem()
    # At checkpoint 20, 90 units of this tag's lifetime remain.
    system.set_tag_with_hold("parcel", "locker", "A12", 10, 100)
    system.checkpoint(20)

    system.set_tag_at("parcel", "locker", "changed", 30)
    system.restore_checkpoint(1_000, 20)

    # Original expiration 110 is shifted by 1_000 - 20, becoming 1_090.
    assert system.get_tag_at("parcel", "locker", 1_089) == "A12"
    assert system.get_tag_at("parcel", "locker", 1_090) is None


def test_restore_keeps_permanent_tags_permanent():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "saved", 10)
    system.checkpoint(20)
    system.remove_tag_at("parcel", "status", 30)

    system.restore_checkpoint(1_000, 20)
    assert system.get_tag_at("parcel", "status", 1_000_000) == "saved"


def test_checkpoints_are_independent_snapshots():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "one", 10)
    system.checkpoint(20)
    system.set_tag_at("parcel", "status", "two", 30)
    system.checkpoint(40)
    system.set_tag_at("parcel", "status", "three", 50)

    system.restore_checkpoint(100, 20)
    assert system.get_tag_at("parcel", "status", 101) == "one"

    system.restore_checkpoint(200, 40)
    assert system.get_tag_at("parcel", "status", 201) == "two"


def test_checkpoint_at_same_timestamp_replaces_previous_snapshot():
    system = ParcelTrackingSystem()
    system.set_tag_at("parcel", "status", "first", 10)
    system.checkpoint(20)
    system.set_tag_at("parcel", "status", "second", 20)
    system.checkpoint(20)
    system.set_tag_at("parcel", "status", "third", 30)

    system.restore_checkpoint(100, 20)
    assert system.get_tag_at("parcel", "status", 101) == "second"

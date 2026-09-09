from parcel_tracking_system.solution import ParcelTrackingSystem


def test_set_and_get_tag():
    system = ParcelTrackingSystem()

    assert system.get_tag("parcel-1", "status") is None
    system.set_tag("parcel-1", "status", "created")
    assert system.get_tag("parcel-1", "status") == "created"


def test_set_overwrites_existing_tag():
    system = ParcelTrackingSystem()
    system.set_tag("parcel-1", "status", "created")
    system.set_tag("parcel-1", "status", "in-transit")

    assert system.get_tag("parcel-1", "status") == "in-transit"


def test_remove_tag():
    system = ParcelTrackingSystem()
    system.set_tag("parcel-1", "status", "delivered")

    assert system.remove_tag("parcel-1", "status") is True
    assert system.get_tag("parcel-1", "status") is None
    assert system.remove_tag("parcel-1", "status") is False
    assert system.remove_tag("missing", "status") is False


def test_parcels_and_tags_are_independent():
    system = ParcelTrackingSystem()
    system.set_tag("parcel-1", "status", "ready")
    system.set_tag("parcel-1", "owner", "Ana")
    system.set_tag("parcel-2", "status", "waiting")

    assert system.get_tag("parcel-1", "status") == "ready"
    assert system.get_tag("parcel-1", "owner") == "Ana"
    assert system.get_tag("parcel-2", "status") == "waiting"
    assert system.get_tag("parcel-2", "owner") is None

    assert system.remove_tag("parcel-1", "status") is True
    assert system.get_tag("parcel-2", "status") == "waiting"


def test_empty_string_is_a_valid_value():
    system = ParcelTrackingSystem()
    system.set_tag("parcel", "note", "")

    assert system.get_tag("parcel", "note") == ""

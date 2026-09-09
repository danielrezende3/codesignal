from parcel_tracking_system.solution import ParcelTrackingSystem


def test_list_tags_sorted_lexicographically():
    system = ParcelTrackingSystem()
    system.set_tag("parcel", "status", "ready")
    system.set_tag("parcel", "address", "Maceio")
    system.set_tag("parcel", "owner", "Ana")

    assert system.list_tags("parcel") == [
        "address(Maceio)",
        "owner(Ana)",
        "status(ready)",
    ]


def test_list_tags_by_prefix():
    system = ParcelTrackingSystem()
    system.set_tag("parcel", "delivery-date", "Friday")
    system.set_tag("parcel", "delivery-status", "scheduled")
    system.set_tag("parcel", "destination", "Recife")
    system.set_tag("parcel", "owner", "Bia")

    assert system.list_tags_by_prefix("parcel", "delivery-") == [
        "delivery-date(Friday)",
        "delivery-status(scheduled)",
    ]
    assert system.list_tags_by_prefix("parcel", "status") == []


def test_listing_missing_or_empty_parcel():
    system = ParcelTrackingSystem()

    assert system.list_tags("missing") == []
    assert system.list_tags_by_prefix("missing", "a") == []

    system.set_tag("parcel", "only", "value")
    system.remove_tag("parcel", "only")
    assert system.list_tags("parcel") == []


def test_empty_prefix_lists_every_tag_and_removal_is_reflected():
    system = ParcelTrackingSystem()
    system.set_tag("parcel", "zeta", "1")
    system.set_tag("parcel", "alpha", "2")
    system.set_tag("parcel", "middle", "3")

    assert system.list_tags_by_prefix("parcel", "") == [
        "alpha(2)",
        "middle(3)",
        "zeta(1)",
    ]

    system.remove_tag("parcel", "middle")
    assert system.list_tags("parcel") == ["alpha(2)", "zeta(1)"]


def test_prefix_must_start_at_beginning_of_tag():
    system = ParcelTrackingSystem()
    system.set_tag("parcel", "banana", "yellow")
    system.set_tag("parcel", "nature", "green")

    assert system.list_tags_by_prefix("parcel", "na") == ["nature(green)"]

from types import SimpleNamespace

from app.filters import apply_filters


def test_filters_match():
    settings = SimpleNamespace(
        max_price=100000,
        min_surface=20,
        target_cities=["Valencia"],
        required_keywords=["metro"],
        excluded_keywords=["subasta"],
    )
    listing = {
        "title": "Piso junto metro",
        "price": 90000,
        "surface": 60,
        "location": "Valencia",
        "raw_text": "ideal metro",
    }
    matched, reason = apply_filters(listing, settings)
    assert matched is True
    assert "required keywords" in reason

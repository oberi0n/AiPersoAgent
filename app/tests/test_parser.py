from app.parser import extract_listings


def test_parser_extracts_basic_listing_from_html_link():
    listings = extract_listings(
        "Piso en Valencia 95.000€ 72m2",
        '<a href="https://example.com/listing/1">Ver</a>',
        "Piso en Valencia metro",
        "alerts@example.com",
    )
    assert len(listings) == 1
    assert listings[0]["url"] == "https://example.com/listing/1"
    assert listings[0]["price"] == 95000

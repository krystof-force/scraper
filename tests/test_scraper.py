from unittest.mock import patch, MagicMock
from scraper import scrape, prepare_for_download
import json

mock_data = [
    {
        "title": "Pokemon Official Site",
        "href": "https://www.pokemon.com",
        "body": "Official Pokemon website"
    },
    {
        "title": "Pokemon Wiki",
        "href": "https://www.pokemonwiki.com",
        "body": "Pokemon encyclopedia"
    }
]


def test_scrape_returns_list():
    with patch("scraper.DDGS") as mock_ddgs:
        mock_ddgs.return_value.__enter__.return_value.text.return_value = mock_data
        results = scrape("pokemon")
        assert isinstance(results, list)


def test_scrape_returns_correct_count():
    with patch("scraper.DDGS") as mock_ddgs:
        mock_ddgs.return_value.__enter__.return_value.text.return_value = mock_data
        results = scrape("pokemon")
        assert len(results) == 2


def test_scrape_contains_required_fields():
    with patch("scraper.DDGS") as mock_ddgs:
        mock_ddgs.return_value.__enter__.return_value.text.return_value = mock_data
        results = scrape("pokemon")
        for r in results:
            assert "title" in r
            assert "href" in r
            assert "body" in r


def test_scrape_fields_are_strings():
    with patch("scraper.DDGS") as mock_ddgs:
        mock_ddgs.return_value.__enter__.return_value.text.return_value = mock_data
        results = scrape("pokemon")
        for r in results:
            assert isinstance(r["title"], str)
            assert isinstance(r["href"], str)
            assert isinstance(r["body"], str)


def test_scrape_returns_empty_list_on_error():
    with patch("scraper.DDGS") as mock_ddgs:
        mock_ddgs.return_value.__enter__.return_value.text.side_effect = Exception("chyba")
        results = scrape("pokemon")
        assert results == []

#Json download testy

def test_prepare_for_download_returns_bytes():
    mem = prepare_for_download(mock_data)
    assert mem is not None
    assert mem.read() != b""

def test_prepare_for_download_valid_json():
    mem = prepare_for_download(mock_data)
    content = mem.read().decode("utf-8")
    parsed = json.loads(content)
    assert isinstance(parsed, list)


def test_prepare_for_download_empty_returns_none():
    result = prepare_for_download([])
    assert result is None


def test_prepare_for_download_correct_data():
    mem = prepare_for_download(mock_data)
    content = mem.read().decode("utf-8")
    parsed = json.loads(content)
    assert parsed[0]["title"] == "Pokemon Official Site"
    assert parsed[1]["href"] == "https://www.pokemonwiki.com"
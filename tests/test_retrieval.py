import pytest

from services.documents import CHUNK_SIZE, clean_text, load_documents


def test_clean_text_strips_html_and_whitespace():
    assert clean_text("<p>Hello&nbsp;&amp;   <b>world</b></p>") == "Hello & world"


def test_chunks_are_small_and_carry_scheme_name():
    docs = load_documents()
    assert docs
    for doc in docs[:300]:
        assert doc.metadata["scheme_name"] in doc.page_content
        # label (name, acronym, state) is added on top of the chunk
        assert len(doc.page_content) < CHUNK_SIZE + 600


def test_supplementary_schemes_are_loaded():
    names = {d.metadata["scheme_name"] for d in load_documents()}
    for fragment in ("Ujjwala", "Ayushman Bharat", "Awas Yojana - Gramin", "Sukanya"):
        assert any(fragment in n for n in names), fragment


@pytest.mark.slow
@pytest.mark.parametrize(
    "query, expected",
    [
        ("PM-KISAN", "Kisan Samman"),
        ("Pradhan Mantri Ujjwala Yojana LPG connection women", "Ujjwala"),
        ("Ayushman Bharat health cover 5 lakh", "Ayushman Bharat"),
        ("Sukanya Samriddhi girl child savings", "Sukanya"),
        ("PMAY rural house construction assistance", "Awas Yojana"),
        # Hindi (Devanagari) queries searched directly, no translation step
        ("मुझे मुफ्त एलपीजी गैस कनेक्शन चाहिए", "Ujjwala"),
        ("गरीब परिवार के लिए 5 लाख का स्वास्थ्य बीमा", "Ayushman Bharat"),
        ("बेटी की पढ़ाई और शादी के लिए बचत योजना", "Sukanya"),
        ("गांव में पक्का घर बनाने के लिए सहायता", "Awas Yojana"),
    ],
)
def test_hybrid_retrieval_finds_scheme(query, expected):
    """Needs the embedding model and a built vector_db (no Gemini key needed)."""
    from services.rag import retrieve

    names = [d.metadata["scheme_name"] for d in retrieve(query)]
    assert any(expected in n for n in names), names


@pytest.mark.slow
def test_rewrite_skipped_only_for_plain_english_first_turn():
    from services.rag import _needs_rewrite

    assert not _needs_rewrite("What is PM-KISAN?", ())
    assert _needs_rewrite("PMAY kya hai", ())  # Hinglish
    assert _needs_rewrite("किसानों के लिए योजना", ())  # Hindi script
    assert _needs_rewrite("what documents do I need?", (("user", "hi"),))  # follow-up

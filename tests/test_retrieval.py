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
    ],
)
def test_hybrid_retrieval_finds_scheme(query, expected):
    """Needs the embedding model and a built vector_db (no Gemini key needed)."""
    from services.rag import retrieve

    names = [d.metadata["scheme_name"] for d in retrieve(query)]
    assert any(expected in n for n in names), names


@pytest.mark.slow
@pytest.mark.parametrize(
    "query, expected",
    [
        ("प्रधानमंत्री किसान सम्मान निधि के लिए आवेदन कैसे करें", "Kisan Samman"),  # Hindi, by name
        # Several schemes pay farmers ~6000/year, so a description-only query
        # may return any of them; any relevant income-support scheme is fine.
        ("किसानों को हर साल 6000 रुपये की सहायता", "Nidhi"),  # Hindi, by description
        ("मुझे मुफ्त एलपीजी गैस कनेक्शन चाहिए", "Ujjwala"),  # Hindi
        ("இலவச எரிவாயு இணைப்பு ஏழைப் பெண்களுக்கு", "Ujjwala"),  # Tamil
        ("ஐந்து லட்சம் வரை இலவச மருத்துவ சிகிச்சை", "Ayushman Bharat"),  # Tamil
        ("মেয়ের পড়াশোনা ও বিয়ের জন্য সঞ্চয় প্রকল্প", "Sukanya"),  # Bengali
        ("గ్రామీణ ప్రాంతంలో పక్కా ఇల్లు కట్టుకోవడానికి సహాయం", "Awas Yojana"),  # Telugu
        ("ग्रामीण भागात १०० दिवस रोजगार हमी", "Employment Guarantee"),  # Marathi
        ("gig workers ke liye registration card", "e-Shram"),  # Hinglish
    ],
)
def test_query_in_indian_language_finds_scheme_directly(query, expected):
    """Multilingual embeddings: no translation step. Needs bge-m3 and a built vector_db."""
    from services.rag import retrieve

    names = [d.metadata["scheme_name"] for d in retrieve(query)]
    assert any(expected in n for n in names), names


@pytest.mark.slow
def test_only_follow_ups_are_rewritten():
    from services.rag import _needs_rewrite

    # A first question in any language is searched as typed.
    assert not _needs_rewrite("What is PM-KISAN?", ())
    assert not _needs_rewrite("PMAY kya hai", ())
    assert not _needs_rewrite("किसानों के लिए योजना", ())
    # A follow-up depends on the conversation.
    assert _needs_rewrite("what documents do I need?", (("user", "hi"),))

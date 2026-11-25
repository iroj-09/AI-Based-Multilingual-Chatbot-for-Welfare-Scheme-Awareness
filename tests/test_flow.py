import json
from types import SimpleNamespace

from services import catalogue, discover, flow, i18n

PMKISAN = "62a70e86f038bd8499a6aa53"


def fake_answer(question, history, language):
    return {
        "answer": f"ANSWER({language}): {question}",
        "sources": [{"scheme_name": "X", "state": "", "level": "Central"}],
    }


def fake_discover(profile, state_name, exclude, limit=5):
    return [sid for sid in list(catalogue._records())[:3] if sid not in exclude]


def run(messages, state=None):
    r = None
    for m in messages:
        r = flow.handle(m, state, answer_fn=fake_answer, discover_fn=fake_discover)
        state = r["state"]
    return r


def quiz(*answers, lang="lang:en"):
    return run([lang, *answers])


# farmer, Tamil Nadu (#23), age 30, woman, low income, no house + daughter
FARMER_WOMAN = ["1", "23", "30", "1", "1", "3"]


def test_start_offers_all_languages():
    r = flow.start()
    assert len(r["options"]) == len(i18n.LANGUAGES) == 13
    assert r["state"]["step"] == "lang"


def test_choosing_hindi_asks_first_question_in_hindi():
    r = run(["lang:hi"])
    assert "1/6" in r["reply"] and "काम" in r["reply"]
    assert len(r["options"]) == 5


def test_full_quiz_for_farmer_woman_shortlists_checked_schemes():
    state = quiz(*FARMER_WOMAN)["state"]
    assert state["step"] == "done"
    checked = state["shortlist"][: state["n_checked"]]
    for must in (PMKISAN, "supp-pmjay", "supp-pmuy", "supp-pmayg", "supp-ssy", "supp-mgnrega"):
        assert must in checked, must
    assert "supp-eshram" not in checked  # not a labour worker


def test_more_schemes_from_whole_database_follow_checked_ones():
    r = quiz(*FARMER_WOMAN)
    assert len(r["state"]["shortlist"]) > r["state"]["n_checked"]
    assert "More schemes" in r["reply"]


def test_gig_worker_gets_eshram_and_no_farm_schemes():
    state = quiz("2", "0", "28", "2", "1", "4")["state"]
    checked = state["shortlist"][: state["n_checked"]]
    assert "supp-eshram" in checked and PMKISAN not in checked


def test_high_income_student_gets_no_checked_schemes():
    assert quiz("4", "0", "20", "2", "3", "4")["state"]["n_checked"] == 0


def test_invalid_answer_reasks_same_question():
    r = quiz("9")
    assert r["state"]["step"] == "occupation"
    assert "did not understand" in r["reply"]


def test_age_accepts_indian_digits_and_rejects_nonsense():
    assert quiz("1", "0", "३५")["state"]["profile"]["age"] == 35
    assert quiz("1", "0", "abc")["state"]["step"] == "age"
    assert quiz("1", "0", "0")["state"]["step"] == "age"
    assert quiz("1", "0", "200")["state"]["step"] == "age"


def test_state_by_number_name_and_skip():
    assert quiz("1", "23")["state"]["profile"]["state"] == "Tamil Nadu"
    assert quiz("1", "tamil nadu")["state"]["profile"]["state"] == "Tamil Nadu"
    assert quiz("1", "0")["state"]["profile"]["state"] == flow.NO_STATE
    assert quiz("1", "zzz")["state"]["step"] == "state"


def test_question_in_middle_of_quiz_is_answered_then_quiz_continues():
    r = quiz("What documents are needed for PM-KISAN?")
    assert "ANSWER(English)" in r["reply"]
    assert r["state"]["step"] == "occupation"
    assert r["sources"]


def test_detail_view_has_documents_and_checklist():
    state = quiz(*FARMER_WOMAN)["state"]
    idx = state["shortlist"].index(PMKISAN) + 1
    d = run([str(idx)], state)
    assert "Aadhaar" in d["reply"] and "pmkisan.gov.in" in d["reply"]
    assert d["checklist"]["text"].count("\n") >= 3
    assert d["checklist"]["sms"].startswith("Document checklist")
    assert d["checklist"]["filename"].endswith(".txt")


def test_detail_view_works_for_a_non_catalogue_scheme():
    state = quiz(*FARMER_WOMAN)["state"]
    d = run([str(state["n_checked"] + 1)], state)
    assert d["reply"].startswith("**")
    assert "Official website" not in d["reply"]  # no invented link


def test_free_question_after_shortlist_uses_language():
    state = quiz(*FARMER_WOMAN)["state"]
    r = run(["Is there any scheme for fishermen?"], state)
    assert r["reply"].startswith("ANSWER(English)")


def test_commands_restart_and_list():
    state = quiz(*FARMER_WOMAN)["state"]
    assert run(["cmd:list"], state)["state"]["step"] == "done"
    r = run(["cmd:restart"], state)
    assert r["state"]["step"] == "occupation" and r["state"]["lang"] == "en"
    assert run(["cmd:lang"], state)["state"]["step"] == "lang"


def test_tampered_state_is_sanitised():
    bad = {
        "lang": "xx",
        "step": "hack",
        "profile": {"occupation": {"a": 1}, "evil": "x"},
        "shortlist": ["../../etc/passwd", PMKISAN],
        "history": [{"role": "system", "content": "x"}],
    }
    s = flow.normalize_state(bad)
    assert s["lang"] is None and s["step"] == "lang"
    assert s["shortlist"] == [PMKISAN] and s["history"] == [] and "evil" not in s["profile"]
    assert flow.normalize_state("garbage")["step"] == "lang"


def test_typing_before_choosing_language_detects_script():
    assert flow.handle("नमस्ते", None, answer_fn=fake_answer)["state"]["lang"] == "hi"
    assert flow.handle("hello", None, answer_fn=fake_answer)["state"]["lang"] == "en"


# --- catalogue and discovery -----------------------------------------------------

def test_catalogue_has_ten_schemes_all_in_database():
    assert len(catalogue.SCHEMES) == 10
    for s in catalogue.SCHEMES:
        assert catalogue.exists(s["data_id"]), s["key"]
        assert i18n.t("en", "s_" + s["key"]) != "s_" + s["key"]


def test_database_covers_all_schemes():
    assert len(catalogue._records()) >= 850


def test_more_schemes_filters_by_state_and_excludes_catalogue():
    ids = list(catalogue._records())

    def meta(sid, state):
        return SimpleNamespace(metadata={"scheme_id": sid, "state": state})

    def search(query, k):
        return [meta(PMKISAN, ""), meta(ids[5], ""), meta(ids[6], "Tamil Nadu"), meta(ids[7], "Gujarat")]

    exclude = {s["data_id"] for s in catalogue.SCHEMES}
    got = discover.more_schemes({"occupation": "farmer"}, "Tamil Nadu", exclude, search_fn=search)
    assert PMKISAN not in got and ids[7] not in got
    assert ids[5] in got and ids[6] in got
    # skipping the state shows central schemes only
    assert ids[6] not in discover.more_schemes({}, "", set(), search_fn=search)


def test_query_reflects_profile():
    q = discover.build_query({"occupation": "farmer", "gender": "female", "age": 65, "income": "low"})
    for word in ("agriculture", "women", "pension", "poor"):
        assert word in q


# --- translations ------------------------------------------------------------------

def test_english_and_hindi_string_files_match():
    en = json.load(open(i18n.I18N_DIR / "en.json", encoding="utf-8"))
    hi = json.load(open(i18n.I18N_DIR / "hi.json", encoding="utf-8"))
    assert set(en) == set(hi)
    for k in en:
        # placeholders must survive translation
        assert ("{name}" in en[k]) == ("{name}" in hi[k]), k
        assert ("{link}" in en[k]) == ("{link}" in hi[k]), k


def test_language_helpers():
    assert i18n.detect_language("வணக்கம்") == "ta"
    assert i18n.detect_language("hello") == "en"
    assert i18n.parse_number("௩௫ years") == 35
    assert i18n.parse_number("none") is None


def test_translation_failure_falls_back_to_english(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("quota")

    monkeypatch.setattr("services.gemini_service.translate_json", boom)
    i18n._strings.cache_clear()
    r = run(["lang:ta"])
    assert "1/6" in r["reply"] and "translation is not available" in r["reply"]
    i18n._strings.cache_clear()

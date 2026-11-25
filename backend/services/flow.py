"""Guided conversation: language -> 6 eligibility questions -> shortlist ->
document checklist, with free Q&A (RAG over ALL schemes) available at any time.

The server is stateless: the client sends back the `state` it received.
The guided part uses no LLM calls for the questions (fast, no API quota); the
LLM is used for free questions and for one-time translations.
"""

from services import catalogue, discover, i18n

QUIZ_STEPS = ["occupation", "state", "age", "gender", "income", "family"]

# step -> (question key, [(stored value, option label key), ...] or None for typed input)
QUESTIONS = {
    "occupation": (
        "q_occupation",
        [
            ("farmer", "opt_occupation_farmer"),
            ("labour", "opt_occupation_labour"),
            ("homemaker", "opt_occupation_homemaker"),
            ("student", "opt_occupation_student"),
            ("other", "opt_occupation_other"),
        ],
    ),
    "state": ("q_state", None),
    "age": ("q_age", None),
    "gender": (
        "q_gender",
        [("female", "opt_gender_female"), ("male", "opt_gender_male"), ("other", "opt_gender_other")],
    ),
    "income": (
        "q_income",
        [("low", "opt_income_low"), ("mid", "opt_income_mid"), ("high", "opt_income_high")],
    ),
    "family": (
        "q_family",
        [
            ("nohouse", "opt_family_nohouse"),
            ("daughter", "opt_family_daughter"),
            ("both", "opt_family_both"),
            ("none", "opt_family_none"),
        ],
    ),
}

VALID_STEPS = {"lang", "done", "free", *QUIZ_STEPS}
PROFILE_KEYS = set(QUIZ_STEPS)
MAX_HISTORY = 6
NO_STATE = "ANY"  # user skipped the state question: show central schemes only


# --- state ---------------------------------------------------------------------

def new_state(lang=None):
    return {"lang": lang, "step": "lang" if not lang else QUIZ_STEPS[0], "profile": {},
            "shortlist": [], "n_checked": 0, "history": [], "retry": 0}


def normalize_state(raw) -> dict:
    """Never trust client state: keep only known, well-typed fields."""
    state = new_state()
    if not isinstance(raw, dict):
        return state

    if raw.get("lang") in i18n.LANGUAGES:
        state["lang"] = raw["lang"]
    if raw.get("step") in VALID_STEPS:
        state["step"] = raw["step"]

    profile = raw.get("profile") if isinstance(raw.get("profile"), dict) else {}
    state["profile"] = {
        k: (v if k == "age" and isinstance(v, int) else str(v)[:40])
        for k, v in profile.items()
        if k in PROFILE_KEYS and isinstance(v, (int, str))
    }

    shortlist = raw.get("shortlist") if isinstance(raw.get("shortlist"), list) else []
    state["shortlist"] = [s for s in shortlist if isinstance(s, str) and catalogue.exists(s)][:15]
    n = raw.get("n_checked")
    state["n_checked"] = n if isinstance(n, int) and 0 <= n <= len(state["shortlist"]) else 0

    history = raw.get("history") if isinstance(raw.get("history"), list) else []
    state["history"] = [
        {"role": h["role"], "content": str(h["content"])[:600]}
        for h in history
        if isinstance(h, dict) and h.get("role") in ("user", "assistant") and "content" in h
    ][-MAX_HISTORY:]

    state["retry"] = raw.get("retry") if isinstance(raw.get("retry"), int) else 0

    # A quiz step without a language makes no sense; go back to language choice.
    if state["step"] != "lang" and not state["lang"]:
        state["step"] = "lang"
    return state


def _response(state, reply, options=None, sources=None, checklist=None):
    return {"reply": reply, "state": state, "options": options or [],
            "sources": sources or [], "checklist": checklist}


# --- building blocks -------------------------------------------------------------

def _language_options():
    return [{"label": native, "value": f"lang:{code}", "kind": "lang"}
            for code, (_, native) in i18n.LANGUAGES.items()]


def _menu(lang, *cmds):
    return [{"label": i18n.t(lang, f"cmd_{c}"), "value": f"cmd:{c}", "kind": "cmd"} for c in cmds]


def _ask_question(state):
    lang, step = state["lang"], state["step"]
    q_key, options = QUESTIONS[step]
    text = i18n.t(lang, q_key)

    if step == "state":
        lines = [f"0. {i18n.t(lang, 'opt_state_skip')}"]
        lines += [f"{i}. {name}" for i, name in enumerate(discover.STATES, 1)]
        return text + "\n" + "\n".join(lines), []

    if not options:
        return text, []

    labels = [i18n.t(lang, label_key) for _, label_key in options]
    text += "\n" + "\n".join(f"{i}. {label}" for i, label in enumerate(labels, 1))
    buttons = [{"label": label, "value": str(i), "kind": "choice"} for i, label in enumerate(labels, 1)]
    return text, buttons


def _fallback_note(lang):
    return "" if i18n.translation_ok(lang) else "\n\n" + i18n.t("en", "translate_fail")


def _question_response(state, prefix=""):
    text, buttons = _ask_question(state)
    return _response(state, prefix + text + _fallback_note(state["lang"]), buttons)


def start():
    """First message: ask for the language (shown in English and Hindi)."""
    reply = "Welcome to WelfareAI. Please choose your language.\nस्वागत है। कृपया अपनी भाषा चुनें।"
    return _response(new_state(), reply, _language_options())


def _match_state(message):
    """State from a typed number or an English name; None if not understood."""
    number = i18n.parse_number(message)
    if number is not None and len(message.strip()) <= 3:
        if number == 0:
            return NO_STATE
        return discover.STATES[number - 1] if 1 <= number <= len(discover.STATES) else None

    text = message.strip().lower()
    if len(text) < 3 or not text.isascii():
        return None
    hits = [s for s in discover.STATES if text == s.lower() or text in s.lower()]
    return hits[0] if len(hits) == 1 else None


def _parse_answer(step, message):
    if step == "state":
        return _match_state(message)
    number = i18n.parse_number(message)
    if step == "age":
        return number if number is not None and 1 <= number <= 120 else None
    options = QUESTIONS[step][1]
    if number is not None and 1 <= number <= len(options):
        return options[number - 1][0]
    return None


def _short_name(sid):
    return catalogue.record(sid)["name"]


def _shortlist_response(state):
    lang = state["lang"]
    ids, n_checked = state["shortlist"], state["n_checked"]

    if not ids:
        return _response(state, i18n.t(lang, "result_none") + "\n\n" + i18n.t(lang, "disclaimer"),
                         _menu(lang, "ask", "restart"))

    lines = []
    if n_checked:
        lines += [i18n.t(lang, "result_title"), ""]
        for i, sid in enumerate(ids[:n_checked], 1):
            key = catalogue.BY_DATA_ID[sid]["key"]
            lines.append(f"{i}. {_short_name(sid)}\n   {i18n.t(lang, 's_' + key)}")
    if len(ids) > n_checked:
        lines += ["", i18n.t(lang, "more_title"), ""]
        for i, sid in enumerate(ids[n_checked:], n_checked + 1):
            rec = catalogue.record(sid)
            lines.append(f"{i}. {rec['name']}" + (f" ({rec['state']})" if rec["state"] else ""))
    lines += ["", i18n.t(lang, "result_hint"), "", i18n.t(lang, "disclaimer")]

    buttons = [{"label": f"{i}. {_short_name(sid).split(' (')[0][:40]}", "value": str(i), "kind": "choice"}
               for i, sid in enumerate(ids, 1)]
    return _response(state, "\n".join(lines).strip() + _fallback_note(lang),
                     buttons + _menu(lang, "ask", "restart"))


def _detail_response(state, sid):
    lang = state["lang"]
    rec = catalogue.record(sid)
    scheme = catalogue.BY_DATA_ID.get(sid)  # curated catalogue entry, if any
    info = i18n.scheme_details(sid, lang)

    title = rec["name"] + (f" ({rec['state']})" if rec["state"] else "")
    summary = i18n.t(lang, "s_" + scheme["key"]) if scheme else info["desc"]
    lines = [f"**{title}**"] + ([summary] if summary else []) + [""]

    if info["elig"]:
        lines.append(i18n.t(lang, "detail_elig"))
        lines += [f"- {e}" for e in info["elig"]] + [""]

    if info["docs"]:
        lines.append(i18n.t(lang, "detail_docs"))
        lines += [f"{i}. {d}" for i, d in enumerate(info["docs"], 1)]
    else:
        lines.append(i18n.t(lang, "docs_missing"))

    if info["apply"]:
        lines += ["", i18n.t(lang, "detail_apply")]
        lines += [f"{i}. {s}" for i, s in enumerate(info["apply"], 1)]

    link = scheme["link"] if scheme else ""
    if link:
        lines += ["", i18n.t(lang, "detail_official", link=link)]
    lines += ["", i18n.t(lang, "disclaimer")]
    if not info["ok"]:
        lines += ["", i18n.t("en", "translate_fail")]

    checklist = None
    if info["docs"]:
        head = i18n.t(lang, "checklist_title", name=title)
        body = "\n".join(f"{i}. {d}" for i, d in enumerate(info["docs"], 1))
        checklist = {
            "filename": f"{(scheme['key'] if scheme else sid[:8])}-checklist.txt",
            "text": f"{head}\n\n{body}" + (f"\n\n{link}" if link else ""),
            # One-line version for SMS / messaging apps.
            "sms": f"{head}: " + "; ".join(f"{i}) {d}" for i, d in enumerate(info["docs"], 1)),
            "labels": {"download": i18n.t(lang, "btn_download"),
                       "copy": i18n.t(lang, "btn_copy"),
                       "copied": i18n.t(lang, "btn_copied")},
        }

    return _response(state, "\n".join(lines), _menu(lang, "list", "ask", "restart"), checklist=checklist)


def _answer_question(state, question, answer_fn):
    """Free question answered from the full scheme database (RAG), with sources."""
    if answer_fn is None:
        from services.rag import ask_rag as answer_fn  # lazy: heavy imports

    history = [(h["role"], h["content"]) for h in state["history"]]
    result = answer_fn(question, history, i18n.language_name(state["lang"]))

    state["history"] = (state["history"]
                        + [{"role": "user", "content": question[:600]},
                           {"role": "assistant", "content": result["answer"][:600]}])[-MAX_HISTORY:]
    return result


def _looks_like_question(message):
    return i18n.parse_number(message) is None and len(message) >= 10


def _build_shortlist(state, discover_fn):
    profile = {k: v for k, v in state["profile"].items()}
    checked = catalogue.shortlist(profile)

    state_name = profile.get("state", NO_STATE)
    state_name = "" if state_name == NO_STATE else state_name
    try:
        more = (discover_fn or discover.more_schemes)(
            profile, state_name, exclude={s["data_id"] for s in catalogue.SCHEMES}
        )
    except Exception:
        # Discovery is a bonus; the rule-checked list must still be shown.
        import logging
        logging.getLogger(__name__).exception("more_schemes failed")
        more = []

    state["shortlist"] = checked + [m for m in more if m not in checked]
    state["n_checked"] = len(checked)


# --- main entry --------------------------------------------------------------------

def handle(message, state, answer_fn=None, discover_fn=None):
    state = normalize_state(state)
    msg = (message or "").strip()
    lang = state["lang"]

    # Language selection (button, or any text typed before choosing).
    if msg.startswith("lang:") or state["step"] == "lang":
        code = msg[5:] if msg.startswith("lang:") else i18n.detect_language(msg)
        state = new_state(code if code in i18n.LANGUAGES else "en")
        return _question_response(state, i18n.t(state["lang"], "intro") + "\n\n")

    # Menu commands.
    if msg.startswith("cmd:"):
        cmd = msg[4:]
        if cmd in ("restart", "quiz"):
            state = new_state(lang)
            return _question_response(state, i18n.t(lang, "intro") + "\n\n")
        if cmd == "lang":
            return start()
        if cmd == "list" and state["shortlist"]:
            state["step"] = "done"
            return _shortlist_response(state)
        if cmd == "ask":
            state["step"] = "free"
            return _response(state, i18n.t(lang, "free_prompt"), _menu(lang, "quiz", "lang"))
        return _response(state, i18n.t(lang, "invalid"))

    step = state["step"]

    # Guided eligibility questions.
    if step in QUIZ_STEPS:
        value = _parse_answer(step, msg)

        if value is None:
            # A real question in the middle of the quiz: answer it, then continue.
            if _looks_like_question(msg) and step != "state":
                result = _answer_question(state, msg, answer_fn)
                text, buttons = _ask_question(state)
                reply = f"{result['answer']}\n\n{i18n.t(lang, 'continue')}\n{text}"
                return _response(state, reply, buttons, sources=result["sources"])
            state["retry"] += 1
            hint_key = {"age": "invalid_age", "state": "invalid_state"}.get(step, "invalid")
            return _question_response(state, i18n.t(lang, hint_key) + "\n\n")

        state["profile"][step] = value
        state["retry"] = 0
        next_index = QUIZ_STEPS.index(step) + 1

        if next_index < len(QUIZ_STEPS):
            state["step"] = QUIZ_STEPS[next_index]
            return _question_response(state)

        _build_shortlist(state, discover_fn)
        state["step"] = "done"
        return _shortlist_response(state)

    # After the shortlist: a number opens a scheme, anything else is a question.
    if step == "done":
        number = i18n.parse_number(msg)
        if number is not None and 1 <= number <= len(state["shortlist"]) and len(msg) <= 3:
            return _detail_response(state, state["shortlist"][number - 1])

    # Free Q&A over all schemes.
    if not msg:
        return _response(state, i18n.t(lang, "invalid"))
    result = _answer_question(state, msg, answer_fn)
    menu = _menu(lang, "list", "quiz", "lang") if state["shortlist"] else _menu(lang, "quiz", "lang")
    return _response(state, result["answer"], menu, sources=result["sources"])

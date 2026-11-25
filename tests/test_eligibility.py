from services.recommender import recommend_schemes


def names(**kw):
    base = {"age": 30, "gender": "Male", "occupation": "Teacher", "income": 500000}
    base.update(kw)
    return [s["name"] for s in recommend_schemes(base)]


def has(result, fragment):
    return any(fragment in n for n in result)


def test_farmer_gets_pm_kisan_case_insensitive():
    assert has(names(occupation=" Farmer "), "PM-KISAN")


def test_farmer_pension_requires_age_18_to_40():
    assert has(names(occupation="farmer", age=30), "Maandhan")
    assert not has(names(occupation="farmer", age=50), "Maandhan")


def test_non_farmer_gets_no_farm_schemes():
    assert not has(names(occupation="teacher", income=900000), "PM-KISAN")


def test_low_income_gets_ayushman_bharat():
    assert has(names(income=100000), "Ayushman Bharat")


def test_senior_citizen_gets_ayushman_bharat_regardless_of_income():
    assert has(names(age=72, income=900000), "Ayushman Bharat")


def test_high_income_young_gets_nothing():
    assert names(income=900000) == []


def test_ujjwala_requires_woman_and_low_income():
    assert has(names(gender="Female", income=100000), "Ujjwala")
    assert not has(names(gender="Female", income=900000), "Ujjwala")
    assert not has(names(gender="Male", income=100000), "Ujjwala")


def test_every_result_has_reason_and_question():
    for s in recommend_schemes(
        {"age": 30, "gender": "Female", "occupation": "farmer", "income": 100000}
    ):
        assert s["reason"] and s["ask"].startswith("Tell me about")

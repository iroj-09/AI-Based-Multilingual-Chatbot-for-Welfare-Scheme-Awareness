"""
Hand-curated central schemes that are missing from the scraped dataset.

Run:  python data/supplementary_schemes.py   (from backend/)
Writes data/supplementary_schemes.jsonl, which build_vector_db.py loads in
addition to cleaned_schemes.jsonl.

IMPORTANT: amounts and rules change. Review these entries against the official
portal in each "application_process" before every public release.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "supplementary_schemes.jsonl"

SCHEMES = [
    {
        "scheme_id": "supp-pmjay",
        "scheme_name": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
        "short_title": "PM-JAY / Ayushman Bharat",
        "categories": ["Health & Wellness"],
        "tags": ["Health", "Insurance", "Hospitalisation", "Ayushman Bharat", "PMJAY", "Ayushman Card"],
        "description": (
            "Ayushman Bharat PM-JAY is a Central Government health assurance scheme that "
            "provides cashless hospital treatment to poor and vulnerable families."
        ),
        "benefits": (
            "1. Health cover of up to Rs 5 lakh per family per year for secondary and tertiary care hospitalisation.\n"
            "2. Cashless and paperless treatment at empanelled public and private hospitals across India.\n"
            "3. Covers pre-existing diseases from day one, with no cap on family size or age.\n"
            "4. Senior citizens aged 70 years and above are eligible for cover irrespective of income."
        ),
        "eligibility": (
            "1. Families identified from the Socio-Economic Caste Census (SECC) 2011 deprivation and occupational criteria are covered.\n"
            "2. Senior citizens aged 70 years and above are eligible irrespective of income.\n"
            "3. Eligibility can be checked on the official portal or by calling the helpline 14555.\n"
            "4. State governments may extend cover to additional families."
        ),
        "application_process": (
            "1. Check eligibility at https://pmjay.gov.in or through the helpline 14555.\n"
            "2. Visit an empanelled hospital's Ayushman Mitra desk or a Common Service Centre with your documents.\n"
            "3. After verification, an Ayushman card is generated and used for cashless treatment."
        ),
        "documents_required": (
            "1. Aadhaar card.\n"
            "2. Ration card or other family identity proof.\n"
            "3. Mobile number for verification.\n"
            "4. Age proof for senior-citizen cover."
        ),
    },
    {
        "scheme_id": "supp-pmuy",
        "scheme_name": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "short_title": "PMUY / Ujjwala",
        "categories": ["Social welfare & Empowerment", "Women and Child"],
        "tags": ["LPG", "Women", "Clean Cooking Fuel", "BPL", "Ujjwala"],
        "description": (
            "Pradhan Mantri Ujjwala Yojana provides LPG connections to women from poor households "
            "so that they can use clean cooking fuel instead of firewood or coal."
        ),
        "benefits": (
            "1. Free (deposit-free) LPG connection in the name of the adult woman of the household, with government financial support.\n"
            "2. A targeted subsidy on LPG refills for eligible PMUY consumers, as notified by the Government from time to time.\n"
            "3. Option of EMI facility for the stove and first refill through oil marketing companies."
        ),
        "eligibility": (
            "1. Applicant must be an adult woman.\n"
            "2. The household must belong to a poor category such as BPL, SC/ST, PMAY beneficiary, Antyodaya Anna Yojana, "
            "most backward classes, tea garden or forest dwellers, or islands, as listed in the scheme.\n"
            "3. No other LPG connection should exist in the household."
        ),
        "application_process": (
            "1. Apply online at https://www.pmuy.gov.in or visit the nearest LPG distributor.\n"
            "2. Submit the KYC application form with the required documents.\n"
            "3. After verification the LPG connection is released."
        ),
        "documents_required": (
            "1. Aadhaar card of the woman applicant.\n"
            "2. BPL ration card or other proof of eligibility category.\n"
            "3. Bank account details.\n"
            "4. Passport-size photograph.\n"
            "5. Self-declaration that no other LPG connection exists in the household."
        ),
    },
    {
        "scheme_id": "supp-pmayg",
        "scheme_name": "Pradhan Mantri Awas Yojana - Gramin (PMAY-G)",
        "short_title": "PMAY-G",
        "categories": ["Housing & Shelter", "Agriculture,Rural & Environment"],
        "tags": ["Housing", "Rural", "Pucca House", "Awas", "PMAY"],
        "description": (
            "PMAY-G provides financial assistance to eligible rural households without a pucca house "
            "to construct a basic house with essential amenities."
        ),
        "benefits": (
            "1. Unit assistance of Rs 1.20 lakh in plain areas and Rs 1.30 lakh in hilly states, difficult areas and IAP districts.\n"
            "2. Support for up to 90 to 95 days of unskilled labour under MGNREGS.\n"
            "3. Assistance of Rs 12,000 for a toilet under Swachh Bharat Mission - Gramin.\n"
            "4. House of minimum 25 square metres with a hygienic cooking space."
        ),
        "eligibility": (
            "1. Rural households that are houseless or live in zero, one or two room kutcha houses.\n"
            "2. Beneficiaries are identified using SECC 2011 data and verified by Gram Sabha.\n"
            "3. Priority to SC/ST, minorities, persons with disabilities, widows and freed bonded labourers.\n"
            "4. The household must not already own a pucca house."
        ),
        "application_process": (
            "1. Beneficiaries are selected from the permanent wait list and approved by the Gram Sabha.\n"
            "2. Contact the Gram Panchayat or Block Development Office to check your name.\n"
            "3. Details and status are available at https://pmayg.nic.in."
        ),
        "documents_required": (
            "1. Aadhaar card.\n"
            "2. Job card number (MGNREGS), if available.\n"
            "3. Bank account details.\n"
            "4. SBM-G registration number for toilet assistance."
        ),
    },
    {
        "scheme_id": "supp-pmayu",
        "scheme_name": "Pradhan Mantri Awas Yojana - Urban (PMAY-U 2.0)",
        "short_title": "PMAY-U",
        "categories": ["Housing & Shelter"],
        "tags": ["Housing", "Urban", "Home Loan", "Interest Subsidy", "Awas", "PMAY"],
        "description": (
            "PMAY-U 2.0 helps urban families from economically weaker sections and low and middle income "
            "groups to own a house through central assistance and home loan interest subsidy."
        ),
        "benefits": (
            "1. Central assistance for building or enhancing a house on own land.\n"
            "2. Interest subsidy on home loans for eligible families.\n"
            "3. Affordable housing in partnership and affordable rental housing verticals."
        ),
        "eligibility": (
            "1. Urban families that do not own a pucca house anywhere in India.\n"
            "2. Annual household income limits: EWS up to Rs 3 lakh, LIG Rs 3 to 6 lakh, MIG Rs 6 to 9 lakh.\n"
            "3. Specific benefits differ by vertical and income category; check the official guidelines."
        ),
        "application_process": (
            "1. Apply online at https://pmay-urban.gov.in or through your Urban Local Body or a Common Service Centre.\n"
            "2. For loan-linked subsidy, approach a participating bank or housing finance company."
        ),
        "documents_required": (
            "1. Aadhaar card.\n"
            "2. Income proof or self-declaration.\n"
            "3. Bank account details.\n"
            "4. Land or property documents, where applicable."
        ),
    },
    {
        "scheme_id": "supp-ssy",
        "scheme_name": "Sukanya Samriddhi Yojana (SSY)",
        "short_title": "SSY",
        "categories": ["Social welfare & Empowerment", "Women and Child", "Banking,Financial Services and Insurance"],
        "tags": ["Girl Child", "Savings", "Education", "Marriage", "Daughter", "Sukanya"],
        "description": (
            "Sukanya Samriddhi Yojana is a small savings scheme for the girl child that helps parents save "
            "for their daughter's education and marriage expenses, with tax benefits and a government-set interest rate."
        ),
        "benefits": (
            "1. Interest at a rate notified by the Government every quarter.\n"
            "2. Tax benefit under Section 80C on deposits; the interest and maturity amount are exempt from tax.\n"
            "3. Up to 50 percent of the balance can be withdrawn after the girl turns 18 for higher education or marriage.\n"
            "4. The account matures 21 years after it is opened."
        ),
        "eligibility": (
            "1. The account is opened by a parent or legal guardian for a girl child below 10 years of age.\n"
            "2. One account per girl child, and generally a maximum of two accounts per family.\n"
            "3. The girl must be an Indian resident."
        ),
        "application_process": (
            "1. Open the account at any post office or authorised bank branch with the application form and documents.\n"
            "2. Minimum deposit is Rs 250 and maximum is Rs 1.5 lakh in a financial year.\n"
            "3. Deposits are made for 15 years from the date of opening."
        ),
        "documents_required": (
            "1. Birth certificate of the girl child.\n"
            "2. Aadhaar card and PAN, if available, of the parent or guardian.\n"
            "3. Address proof of the parent or guardian.\n"
            "4. Passport-size photographs."
        ),
    },
    {
        "scheme_id": "supp-mgnrega",
        "scheme_name": "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGS)",
        "short_title": "MGNREGA / NREGA",
        "categories": ["Skills & Employment", "Agriculture,Rural & Environment"],
        "tags": ["Employment", "Rural", "Wages", "Job Card", "NREGA", "100 days"],
        "description": (
            "MGNREGS guarantees up to 100 days of wage employment in a financial year to every rural "
            "household whose adult members volunteer to do unskilled manual work."
        ),
        "benefits": (
            "1. Up to 100 days of guaranteed wage employment per rural household in a financial year.\n"
            "2. Wages are paid at the rate notified by the State and are paid into the worker's bank or post office account.\n"
            "3. Work is to be provided within about 5 km of the applicant's village.\n"
            "4. If work is not provided within 15 days of the demand, an unemployment allowance is payable."
        ),
        "eligibility": (
            "1. The applicant must be an adult member of a rural household.\n"
            "2. The applicant must be willing to do unskilled manual work.\n"
            "3. The household must be registered with the Gram Panchayat and hold a Job Card."
        ),
        "application_process": (
            "1. Apply to the Gram Panchayat for a Job Card. Registration is free.\n"
            "2. The Job Card is issued after verification, normally within 15 days.\n"
            "3. Submit a written or oral application to the Gram Panchayat for work, stating the period for which work is needed.\n"
            "4. Details are available at https://nrega.nic.in."
        ),
        "documents_required": (
            "1. Application for registration to the Gram Panchayat.\n"
            "2. Passport-size photograph.\n"
            "3. Identity proof such as Aadhaar, as required by the State.\n"
            "4. Bank or post office account details."
        ),
    },
    {
        "scheme_id": "supp-eshram",
        "scheme_name": "e-Shram Registration for Unorganised Workers",
        "short_title": "e-Shram",
        "categories": ["Skills & Employment", "Social welfare & Empowerment"],
        "tags": ["Unorganised Workers", "Gig Workers", "Labour", "e-Shram", "UAN", "Accident Insurance"],
        "description": (
            "e-Shram is the national database of unorganised workers, including gig and platform workers. "
            "Registered workers receive an e-Shram card with a Universal Account Number (UAN)."
        ),
        "benefits": (
            "1. An e-Shram card with a 12-digit Universal Account Number (UAN).\n"
            "2. Accidental insurance cover under the Pradhan Mantri Suraksha Bima Yojana for registered workers, "
            "with the premium paid by the Government for the first year.\n"
            "3. Easier access to present and future social security schemes for unorganised workers."
        ),
        "eligibility": (
            "1. The applicant must be an unorganised worker aged between 16 and 59 years.\n"
            "2. The applicant must not be a member of EPFO or ESIC.\n"
            "3. The applicant must not be an income tax payer.\n"
            "4. Gig and platform workers can register."
        ),
        "application_process": (
            "1. Register free of cost at https://eshram.gov.in or through the nearest Common Service Centre or post office.\n"
            "2. Aadhaar-linked mobile number is needed for OTP verification.\n"
            "3. After registration the e-Shram card can be downloaded."
        ),
        "documents_required": (
            "1. Aadhaar card.\n"
            "2. Mobile number linked with Aadhaar.\n"
            "3. Bank account details."
        ),
    },
]


def build_record(s: dict) -> dict:
    record = {
        "scheme_id": s["scheme_id"],
        "scheme_name": s["scheme_name"],
        "short_title": s["short_title"],
        "state": None,
        "level": "Central",
        "categories": s["categories"],
        "tags": s["tags"],
        "description": s["description"],
        "benefits": s["benefits"],
        "eligibility": s["eligibility"],
        "application_process": s["application_process"],
        "documents_required": s["documents_required"],
    }
    record["search_text"] = f"""
Scheme Name: {record['scheme_name']}
State: {record['state']}
Description: {record['description']}
Benefits: {record['benefits']}
Eligibility: {record['eligibility']}
Application Process: {record['application_process']}
Documents: {record['documents_required']}
"""
    return record


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        for s in SCHEMES:
            f.write(json.dumps(build_record(s), ensure_ascii=False) + "\n")
    print(f"Wrote {len(SCHEMES)} schemes to {OUT}")

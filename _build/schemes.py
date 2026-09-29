# -*- coding: utf-8 -*-
"""Government Schemes — the data behind /schemes/.

One dict per scheme, in the shape the content team maintains it:

    id, category, one_line, benefit_amount, who_qualifies, documents_needed,
    how_to_apply, helpline, teacher_note
    + the per-scheme extras (loan_tiers, coverage_includes, what_it_gives,
      repayment, check_first)

Rules for this file
-------------------
* The English text is exactly as supplied by the content team. Do not
  paraphrase it here — a scheme stays in one place so trainers can diff it.
* `teacher_note` is TRAINER material. It is never rendered inside the app;
  it appears on /schemes/trainer-notes/ (noindex, for the field team only).
* `check_first` is the user-facing form of a CAUTION teacher note. Where a
  scheme's eligibility is genuinely uncertain (Vishwakarma trade lists, ODOP
  district product lists) the app must not promise it — it shows this line
  instead.
* Translations for everything a woman reads live in SCHEME_I18N below, keyed
  "<scheme_id>.<field>". English is never duplicated: it comes from the
  scheme dict. teacher_note has no translation on purpose.

Adding a scheme: append to SCHEMES, add its SCHEME_I18N block, add its
SCHEME_UI keys if it introduces a new category, then run the build.
"""

# ---------------------------------------------------------------- the schemes
SCHEMES = [
    {
        "id": "scheme_mudra",
        "cat": "loan",
        "slug": "mudra",
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "category": "Loan",
        "icon": "rupee",
        "one_line": "A loan to start or grow your business — no collateral needed.",
        "benefit_amount": "Up to ₹20 lakh (Tarun Plus category)",
        "loan_tiers": [
            ("Shishu", "Up to ₹50,000 — for a brand-new, very small business"),
            ("Kishore", "₹50,001 to ₹5 lakh — for a business that's already running"),
            ("Tarun", "₹5 lakh to ₹10 lakh — for growing an established business"),
            ("Tarun Plus", "₹10 lakh to ₹20 lakh — for well-established small businesses"),
        ],
        "who_qualifies": "Any Indian citizen with a non-farm business plan (like food processing/pickle-making). No minimum loan amount. Women and first-time entrepreneurs get priority.",
        "documents_needed": [
            "Aadhaar card",
            "PAN card",
            "Passport-size photo",
            "Business plan (even a simple one-page plan works)",
            "Bank account details",
        ],
        "how_to_apply": "Visit any nearby bank branch (public or private) or apply online via udyamimitra.in. No agent or middleman needed.",
        "helpline": "1800-180-1111 (PMMY toll-free)",
        "teacher_note": "This is the FIRST scheme to teach — smallest loan, easiest approval, no property needed as security.",
        # app-facing tags used by the matcher, not shown as text
        "tags": ["loan", "new", "running"],
        "needs_bank": True,
        "available_in": "all",
    },
    {
        "id": "scheme_standup",
        "cat": "loan",
        "slug": "stand-up-india",
        "name": "Stand-Up India",
        "category": "Loan",
        "icon": "women",
        "one_line": "A bigger loan for women starting a brand-new, larger business.",
        "benefit_amount": "₹10 lakh to ₹1 crore",
        "who_qualifies": "Women entrepreneurs aged 18+, starting a NEW business (not for an existing one). At least one woman per bank branch is guaranteed this loan.",
        "documents_needed": [
            "Aadhaar + PAN",
            "Detailed project report",
            "Caste certificate (only if applying under SC/ST category)",
            "Address proof of business location",
        ],
        "how_to_apply": "Apply online at standupmitra.in, or walk into any scheduled commercial bank branch and ask for the Stand-Up India desk.",
        "repayment": "Up to 7 years, with up to 18 months before repayment needs to start",
        "helpline": "1800-180-1111 (PMMY toll-free)",
        "teacher_note": "Teach this AFTER Mudra — this is for when the business is ready to open a proper factory/unit, not for the first small batch.",
        "tags": ["loan", "new"],
        "needs_bank": True,
        "available_in": "all",
    },
    {
        "id": "scheme_pmjay",
        "cat": "health",
        "slug": "ayushman-bharat",
        "name": "Ayushman Bharat PM-JAY",
        "category": "Health Insurance",
        "icon": "shield",
        "one_line": "Free hospital treatment up to ₹5 lakh a year for your whole family.",
        "benefit_amount": "₹5,00,000 per family per year (no cap on family size)",
        "coverage_includes": [
            "Doctor consultation",
            "Medicines",
            "Tests",
            "Surgery",
            "ICU",
            "Hospital stay & food",
        ],
        "who_qualifies": "Families identified as economically weaker under the 2011 government survey (SECC). Most rural low-income households already qualify — check with your Ayushman card status.",
        "documents_needed": ["Aadhaar card", "Ration card (if available)"],
        "how_to_apply": "Check eligibility free at the nearest Common Service Centre (CSC) or Ayushman Arogya Mandir, or ask your Sakhi Champion to check via the app.",
        "helpline": "14555 (PM-JAY toll-free)",
        "teacher_note": "MANY women don't know they already qualify for this for FREE. Always check this first before ApnaPan spends money on private health insurance top-ups — this reduces our own program cost significantly.",
        "tags": ["health"],
        "needs_bank": False,      # deliberately: no bank account needed
        "available_in": "all",
    },
    {
        "id": "scheme_nrlm",
        "cat": "group",
        "slug": "nrlm-shg",
        "name": "DAY-NRLM — Women's Self-Help Groups",
        "category": "Group Support & Training",
        "icon": "users",
        "one_line": "Join a women's group to get training, savings support, and easier loans together.",
        "benefit_amount": "Varies — includes revolving fund support (~₹15,000-₹20,000 per SHG) plus bank-linked group loans",
        "what_it_gives": [
            "Training in skills (like ours — food processing, packaging, bookkeeping)",
            "Group savings habit-building",
            "Easier bank loans because the whole group guarantees each other",
            "Access to 'Bank Sakhis' — trained local women who help with banking",
        ],
        "who_qualifies": "Any rural woman — no business required yet. You can join even before starting anything.",
        "documents_needed": [],
        "how_to_apply": "Contact your local Gram Panchayat office or Block Development Office and ask to join or form an SHG under DAY-NRLM.",
        "helpline": "",
        "teacher_note": "This is the FOUNDATION scheme — if a woman is already in an SHG, getting her into ApnaPan becomes much easier because she already trusts group-based systems and has some savings habit.",
        "tags": ["loan", "skill", "new", "running"],
        "needs_bank": False,      # a group is also the route to opening one
        "available_in": "all",
    },
    {
        "id": "scheme_vishwakarma",
        "cat": "trade",
        "slug": "pm-vishwakarma",
        "name": "PM Vishwakarma",
        "category": "Loan (for traditional trades)",
        "icon": "box",
        "one_line": "Low-interest loan and a toolkit for traditional skilled work.",
        "benefit_amount": "Up to ₹3 lakh across 2 loan stages, at just 5% interest",
        "who_qualifies": "Artisans/craftspeople in 18 recognized traditional trades. Check if your state includes food-processing/pickle-making artisans under local trade lists — this varies, confirm before promising it.",
        "documents_needed": ["Aadhaar card", "Proof of traditional trade/skill"],
        "how_to_apply": "Register at pmvishwakarma.gov.in or nearest Common Service Centre",
        "helpline": "18002677777",
        "check_first": "Check with your Sakhi first — not every state lists food processing as a traditional trade.",
        "teacher_note": "CAUTION: Only mention this scheme after confirming with the local CSC whether pickle/spice-making qualifies under your state's trade list — don't promise this one without checking first.",
        "tags": ["loan", "new", "running"],
        "needs_bank": True,
        "available_in": "some_states",
    },
    {
        "id": "scheme_odop",
        "cat": "market",
        "slug": "odop",
        "name": "One District One Product (ODOP)",
        "category": "Market Access & Branding Support",
        "icon": "award",
        "one_line": "Government help to brand and sell your district's famous local product.",
        "benefit_amount": "Varies by state — includes branding support, common facility centers, and marketing linkage (not a direct cash loan)",
        "who_qualifies": "Producers of the specific product identified as their district's ODOP product (check if spices/pickles are your district's listed product).",
        "documents_needed": [],
        "how_to_apply": "Contact your District Industries Centre (DIC)",
        "helpline": "",
        "check_first": "Check with your Sakhi first — this only fits if spices or pickles are your district's listed product.",
        "teacher_note": "Very useful if your specific district's ODOP product IS spices or pickles — gives free help with branding, packaging design, and connecting to bigger buyers. Worth checking district-by-district as you expand ApnaPan to new regions.",
        "tags": ["skill", "running"],
        "needs_bank": False,
        "available_in": "some_states",
    },
]


# ------------------------------------------------------------- translations
# key: "<slug>.<field>" — value: (kannada, hindi). English comes from SCHEMES.
SCHEME_I18N = {
    # ---- names, categories, one-liners ------------------------------------
    "mudra.name": ("ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ (PMMY)", "प्रधानमंत्री मुद्रा योजना (PMMY)"),
    "stand-up-india.name": ("ಸ್ಟ್ಯಾಂಡ್-ಅಪ್ ಇಂಡಿಯಾ", "स्टैंड-अप इंडिया"),
    "ayushman-bharat.name": ("ಆಯುಷ್ಮಾನ್ ಭಾರತ್ PM-JAY", "आयुष्मान भारत PM-JAY"),
    "nrlm-shg.name": ("DAY-NRLM — ಮಹಿಳಾ ಸ್ವಯಂ ಸಹಾಯ ಗುಂಪುಗಳು", "DAY-NRLM — महिला स्वयं सहायता समूह"),
    "pm-vishwakarma.name": ("ಪಿಎಂ ವಿಶ್ವಕರ್ಮ", "पीएम विश्वकर्मा"),
    "odop.name": ("ಒಂದು ಜಿಲ್ಲೆ ಒಂದು ಉತ್ಪನ್ನ (ODOP)", "एक जिला एक उत्पाद (ODOP)"),

    "mudra.one_line": ("ವ್ಯಾಪಾರ ಪ್ರಾರಂಭಿಸಲು ಅಥವಾ ಬೆಳೆಸಲು ಸಾಲ — ಯಾವುದೇ ಆಸ್ತಿ ಅಡಮಾನ ಬೇಕಿಲ್ಲ.",
                       "व्यापार शुरू करने या बढ़ाने के लिए कर्ज़ — किसी गिरवी की ज़रूरत नहीं।"),
    "stand-up-india.one_line": ("ಹೊಸದಾಗಿ ದೊಡ್ಡ ಉದ್ಯಮ ಪ್ರಾರಂಭಿಸುವ ಮಹಿಳೆಯರಿಗೆ ದೊಡ್ಡ ಸಾಲ.",
                                "नया और बड़ा व्यापार शुरू करने वाली महिलाओं के लिए बड़ा कर्ज़।"),
    "ayushman-bharat.one_line": ("ನಿಮ್ಮ ಇಡೀ ಕುಟುಂಬಕ್ಕೆ ವರ್ಷಕ್ಕೆ ₹5 ಲಕ್ಷದವರೆಗೆ ಉಚಿತ ಆಸ್ಪತ್ರೆ ಚಿಕಿತ್ಸೆ.",
                                 "आपके पूरे परिवार के लिए साल में ₹5 लाख तक मुफ़्त इलाज।"),
    "nrlm-shg.one_line": ("ತರಬೇತಿ, ಉಳಿತಾಯ ಬೆಂಬಲ ಮತ್ತು ಸುಲಭ ಸಾಲಕ್ಕಾಗಿ ಮಹಿಳಾ ಗುಂಪಿಗೆ ಸೇರಿ.",
                          "प्रशिक्षण, बचत सहयोग और आसान कर्ज़ के लिए महिला समूह से जुड़ें।"),
    "pm-vishwakarma.one_line": ("ಸಾಂಪ್ರದಾಯಿಕ ಕೈಕಸುಬಿಗೆ ಕಡಿಮೆ ಬಡ್ಡಿ ಸಾಲ ಮತ್ತು ಉಪಕರಣ ಕಿಟ್.",
                                "परंपरागत कारीगरी के लिए कम ब्याज वाला कर्ज़ और औज़ार किट।"),
    "odop.one_line": ("ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಪ್ರಸಿದ್ಧ ಸ್ಥಳೀಯ ಉತ್ಪನ್ನಕ್ಕೆ ಬ್ರ್ಯಾಂಡ್ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಸಹಾಯ.",
                      "आपके ज़िले के मशहूर स्थानीय उत्पाद की ब्रांडिंग और बिक्री में सरकारी मदद।"),

    # ---- benefit ----------------------------------------------------------
    "mudra.benefit": ("₹20 ಲಕ್ಷದವರೆಗೆ (ತರುಣ ಪ್ಲಸ್ ವರ್ಗ)", "₹20 लाख तक (तरुण प्लस श्रेणी)"),
    "stand-up-india.benefit": ("₹10 ಲಕ್ಷದಿಂದ ₹1 ಕೋಟಿವರೆಗೆ", "₹10 लाख से ₹1 करोड़ तक"),
    "ayushman-bharat.benefit": ("ಪ್ರತಿ ಕುಟುಂಬಕ್ಕೆ ವರ್ಷಕ್ಕೆ ₹5,00,000 (ಕುಟುಂಬದ ಗಾತ್ರಕ್ಕೆ ಮಿತಿ ಇಲ್ಲ)",
                                "प्रति परिवार प्रति वर्ष ₹5,00,000 (परिवार के आकार की कोई सीमा नहीं)"),
    "nrlm-shg.benefit": ("ಬದಲಾಗುತ್ತದೆ — ಪ್ರತಿ SHG ಗೆ ಸುಮಾರು ₹15,000–₹20,000 ರಿವಾಲ್ವಿಂಗ್ ನಿಧಿ ಮತ್ತು ಬ್ಯಾಂಕ್ ಸಾಲ",
                         "अलग-अलग — प्रति समूह लगभग ₹15,000–₹20,000 का घूर्णन कोष और बैंक से जुड़ा समूह कर्ज़"),
    "pm-vishwakarma.benefit": ("2 ಸಾಲ ಹಂತಗಳಲ್ಲಿ ₹3 ಲಕ್ಷದವರೆಗೆ, ಕೇವಲ 5% ಬಡ್ಡಿ",
                               "2 कर्ज़ चरणों में ₹3 लाख तक, सिर्फ़ 5% ब्याज"),
    "odop.benefit": ("ರಾಜ್ಯದ ಪ್ರಕಾರ ಬದಲಾಗುತ್ತದೆ — ಬ್ರ್ಯಾಂಡಿಂಗ್, ಸಾಮಾನ್ಯ ಸೌಲಭ್ಯ ಕೇಂದ್ರ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಸಂಪರ್ಕ (ನೇರ ನಗದು ಸಾಲ ಅಲ್ಲ)",
                     "राज्य के अनुसार — ब्रांडिंग सहयोग, साझा सुविधा केंद्र और बाज़ार से जोड़ना (सीधा नकद कर्ज़ नहीं)"),

    # ---- who qualifies ----------------------------------------------------
    "mudra.who": ("ಕೃಷಿಯೇತರ ವ್ಯಾಪಾರ ಯೋಜನೆ ಇರುವ ಯಾವುದೇ ಭಾರತೀಯ ಪ್ರಜೆ (ಆಹಾರ ಸಂಸ್ಕರಣೆ, ಉಪ್ಪಿನಕಾಯಿ ತಯಾರಿ ಮುಂತಾದವು). ಕನಿಷ್ಠ ಸಾಲದ ಮೊತ್ತ ಇಲ್ಲ. ಮಹಿಳೆಯರು ಮತ್ತು ಮೊದಲ ಬಾರಿ ಉದ್ಯಮಿಗಳಿಗೆ ಆದ್ಯತೆ.",
                  "गैर-कृषि व्यापार योजना वाला कोई भी भारतीय नागरिक (जैसे खाद्य प्रसंस्करण या अचार बनाना)। कर्ज़ की कोई न्यूनतम राशि नहीं। महिलाओं और पहली बार उद्यमी बनने वालों को प्राथमिकता।"),
    "stand-up-india.who": ("18 ವರ್ಷ ಮೇಲ್ಪಟ್ಟ ಮಹಿಳಾ ಉದ್ಯಮಿಗಳು, ಹೊಸ ಉದ್ಯಮ ಪ್ರಾರಂಭಿಸುವವರು (ಈಗಿರುವ ಉದ್ಯಮಕ್ಕೆ ಅಲ್ಲ). ಪ್ರತಿ ಬ್ಯಾಂಕ್ ಶಾಖೆಯಲ್ಲಿ ಕನಿಷ್ಠ ಒಬ್ಬ ಮಹಿಳೆಗೆ ಈ ಸಾಲ ಖಚಿತ.",
                           "18 वर्ष से ऊपर की महिला उद्यमी जो नया व्यापार शुरू कर रही हैं (पहले से चल रहे के लिए नहीं)। हर बैंक शाखा में कम से कम एक महिला को यह कर्ज़ मिलना तय है।"),
    "ayushman-bharat.who": ("2011ರ ಸರ್ಕಾರಿ ಸಮೀಕ್ಷೆ (SECC) ಪ್ರಕಾರ ಆರ್ಥಿಕವಾಗಿ ದುರ್ಬಲ ಎಂದು ಗುರುತಿಸಲಾದ ಕುಟುಂಬಗಳು. ಹೆಚ್ಚಿನ ಗ್ರಾಮೀಣ ಕಡಿಮೆ ಆದಾಯದ ಕುಟುಂಬಗಳು ಈಗಾಗಲೇ ಅರ್ಹರು — ನಿಮ್ಮ ಆಯುಷ್ಮಾನ್ ಕಾರ್ಡ್ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ.",
                            "2011 की सरकारी सर्वेक्षण (SECC) में आर्थिक रूप से कमज़ोर पहचाने गए परिवार। ज़्यादातर ग्रामीण कम आय वाले परिवार पहले से पात्र हैं — अपने आयुष्मान कार्ड की स्थिति जाँचें।"),
    "nrlm-shg.who": ("ಯಾವುದೇ ಗ್ರಾಮೀಣ ಮಹಿಳೆ — ಇನ್ನೂ ಯಾವುದೇ ಉದ್ಯಮ ಬೇಕಿಲ್ಲ. ಏನನ್ನೂ ಪ್ರಾರಂಭಿಸುವ ಮೊದಲೇ ಸೇರಬಹುದು.",
                     "कोई भी ग्रामीण महिला — अभी कोई व्यापार ज़रूरी नहीं। कुछ शुरू करने से पहले भी जुड़ सकती हैं।"),
    "pm-vishwakarma.who": ("18 ಮಾನ್ಯತೆ ಪಡೆದ ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬುಗಳ ಕಲಾವಿದರು. ಆಹಾರ ಸಂಸ್ಕರಣೆ ಅಥವಾ ಉಪ್ಪಿನಕಾಯಿ ತಯಾರಿಕೆ ನಿಮ್ಮ ರಾಜ್ಯದ ಪಟ್ಟಿಯಲ್ಲಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ — ಇದು ರಾಜ್ಯದಿಂದ ರಾಜ್ಯಕ್ಕೆ ಬದಲಾಗುತ್ತದೆ.",
                           "18 मान्य परंपरागत कारीगरियों के कारीगर। जाँचें कि आपके राज्य की सूची में खाद्य प्रसंस्करण या अचार बनाना शामिल है या नहीं — यह राज्य-दर-राज्य बदलता है।"),
    "odop.who": ("ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ODOP ಉತ್ಪನ್ನವಾಗಿ ಗುರುತಿಸಲಾದ ನಿರ್ದಿಷ್ಟ ಉತ್ಪನ್ನದ ಉತ್ಪಾದಕರು (ಸಂಬಾರ ಪದಾರ್ಥ ಅಥವಾ ಉಪ್ಪಿನಕಾಯಿ ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಪಟ್ಟಿಯಲ್ಲಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ).",
                 "आपके ज़िले के ODOP उत्पाद के रूप में चुने गए उत्पाद के उत्पादक (देखें कि मसाले या अचार आपके ज़िले की सूची में हैं या नहीं)।"),

    # ---- how to apply -----------------------------------------------------
    "mudra.how": ("ಹತ್ತಿರದ ಯಾವುದೇ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಹೋಗಿ (ಸರ್ಕಾರಿ ಅಥವಾ ಖಾಸಗಿ) ಅಥವಾ udyamimitra.in ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ. ಯಾವುದೇ ಏಜೆಂಟ್ ಬೇಕಿಲ್ಲ.",
                  "पास की किसी भी बैंक शाखा में जाएँ (सरकारी या निजी) या udyamimitra.in पर ऑनलाइन आवेदन करें। किसी एजेंट की ज़रूरत नहीं।"),
    "stand-up-india.how": ("standupmitra.in ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ, ಅಥವಾ ಯಾವುದೇ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಹೋಗಿ ಸ್ಟ್ಯಾಂಡ್-ಅಪ್ ಇಂಡಿಯಾ ಡೆಸ್ಕ್ ಎಂದು ಕೇಳಿ.",
                           "standupmitra.in पर ऑनलाइन आवेदन करें, या किसी भी बैंक शाखा में जाकर स्टैंड-अप इंडिया डेस्क के बारे में पूछें।"),
    "ayushman-bharat.how": ("ಹತ್ತಿರದ ಸಿಎಸ್‌ಸಿ (CSC) ಅಥವಾ ಆಯುಷ್ಮಾನ್ ಆರೋಗ್ಯ ಮಂದಿರದಲ್ಲಿ ಉಚಿತವಾಗಿ ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ, ಅಥವಾ ನಿಮ್ಮ ಸಖಿ ಚಾಂಪಿಯನ್ ಅವರನ್ನು ಕೇಳಿ.",
                            "नज़दीकी सीएससी (CSC) या आयुष्मान आरोग्य मंदिर में मुफ़्त पात्रता जाँचें, या अपनी सखी चैंपियन से ऐप से जाँचने को कहें।"),
    "nrlm-shg.how": ("ನಿಮ್ಮ ಗ್ರಾಮ ಪಂಚಾಯತ್ ಕಚೇರಿ ಅಥವಾ ಬ್ಲಾಕ್ ಕಚೇರಿ ಸಂಪರ್ಕಿಸಿ, DAY-NRLM ಅಡಿಯಲ್ಲಿ ಸ್ವಯಂ ಸಹಾಯ ಗುಂಪಿಗೆ ಸೇರಲು ಅಥವಾ ರಚಿಸಲು ಕೇಳಿ.",
                     "अपने ग्राम पंचायत या ब्लॉक कार्यालय से संपर्क करें और DAY-NRLM के तहत समूह से जुड़ने या बनाने के लिए कहें।"),
    "pm-vishwakarma.how": ("pmvishwakarma.gov.in ಅಥವಾ ಹತ್ತಿರದ ಸಿಎಸ್‌ಸಿಯಲ್ಲಿ ನೋಂದಣಿ ಮಾಡಿ",
                           "pmvishwakarma.gov.in या नज़दीकी सीएससी में पंजीकरण करें"),
    "odop.how": ("ನಿಮ್ಮ ಜಿಲ್ಲಾ ಕೈಗಾರಿಕಾ ಕೇಂದ್ರ (DIC) ಸಂಪರ್ಕಿಸಿ", "अपने ज़िला उद्योग केंद्र (DIC) से संपर्क करें"),

    # ---- helpline labels --------------------------------------------------
    "mudra.helpline_label": ("PMMY ಟೋಲ್-ಫ್ರೀ", "PMMY टोल-फ़्री"),
    "stand-up-india.helpline_label": ("PMMY ಟೋಲ್-ಫ್ರೀ", "PMMY टोल-फ़्री"),
    "ayushman-bharat.helpline_label": ("PM-JAY ಟೋಲ್-ಫ್ರೀ", "PM-JAY टोल-फ़्री"),
    "pm-vishwakarma.helpline_label": ("ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಸಹಾಯವಾಣಿ", "पीएम विश्वकर्मा हेल्पलाइन"),

    # ---- check-first cautions --------------------------------------------
    "pm-vishwakarma.check": ("ಮೊದಲು ನಿಮ್ಮ ಸಖಿ ಜೊತೆ ಪರಿಶೀಲಿಸಿ — ಎಲ್ಲಾ ರಾಜ್ಯಗಳಲ್ಲಿ ಆಹಾರ ಸಂಸ್ಕರಣೆ ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬಾಗಿ ಪಟ್ಟಿಯಲ್ಲಿಲ್ಲ.",
                             "पहले अपनी सखी से जाँचें — हर राज्य की सूची में खाद्य प्रसंस्करण शामिल नहीं है।"),
    "odop.check": ("ಮೊದಲು ನಿಮ್ಮ ಸಖಿ ಜೊತೆ ಪರಿಶೀಲಿಸಿ — ಸಂಬಾರ ಅಥವಾ ಉಪ್ಪಿನಕಾಯಿ ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಪಟ್ಟಿಯಲ್ಲಿದ್ದರೆ ಮಾತ್ರ ಇದು ಸರಿಹೊಂದುತ್ತದೆ.",
                   "पहले अपनी सखी से जाँचें — यह तभी लागू है जब मसाले या अचार आपके ज़िले की सूची में हों।"),

    # ---- loan tiers (Mudra) ----------------------------------------------
    "mudra.tier.0": ("₹50,000 ವರೆಗೆ — ಸಂಪೂರ್ಣ ಹೊಸ, ಬಹಳ ಚಿಕ್ಕ ಉದ್ಯಮಕ್ಕೆ", "₹50,000 तक — बिल्कुल नए, बहुत छोटे व्यापार के लिए"),
    "mudra.tier.1": ("₹50,001 ರಿಂದ ₹5 ಲಕ್ಷ — ಈಗಾಗಲೇ ನಡೆಯುತ್ತಿರುವ ಉದ್ಯಮಕ್ಕೆ", "₹50,001 से ₹5 लाख — पहले से चल रहे व्यापार के लिए"),
    "mudra.tier.2": ("₹5 ಲಕ್ಷದಿಂದ ₹10 ಲಕ್ಷ — ಸ್ಥಿರವಾದ ಉದ್ಯಮವನ್ನು ಬೆಳೆಸಲು", "₹5 लाख से ₹10 लाख — स्थापित व्यापार बढ़ाने के लिए"),
    "mudra.tier.3": ("₹10 ಲಕ್ಷದಿಂದ ₹20 ಲಕ್ಷ — ಚೆನ್ನಾಗಿ ಸ್ಥಿರವಾದ ಸಣ್ಣ ಉದ್ಯಮಗಳಿಗೆ", "₹10 लाख से ₹20 लाख — अच्छी तरह स्थापित छोटे व्यापार के लिए"),
    "mudra.tiers_title": ("ಸಾಲದ ಮೊತ್ತ", "कर्ज़ की राशि"),

    # ---- repayment (Stand-Up India) --------------------------------------
    "stand-up-india.repay": ("7 ವರ್ಷದವರೆಗೆ, ಮರುಪಾವತಿ ಪ್ರಾರಂಭಿಸಲು 18 ತಿಂಗಳವರೆಗೆ ಕಾಲಾವಕಾಶ",
                             "7 साल तक, और मोहलत अवधि 18 महीने तक"),

    # ---- coverage (PM-JAY) -----------------------------------------------
    "ayushman-bharat.cover.0": ("ವೈದ್ಯರ ಸಲಹೆ", "डॉक्टर की सलाह"),
    "ayushman-bharat.cover.1": ("ಔಷಧಿಗಳು", "दवाइयाँ"),
    "ayushman-bharat.cover.2": ("ಪರೀಕ್ಷೆಗಳು", "जाँच"),
    "ayushman-bharat.cover.3": ("ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ", "सर्जरी"),
    "ayushman-bharat.cover.4": ("ಐಸಿಯು", "आईसीयू"),
    "ayushman-bharat.cover.5": ("ಆಸ್ಪತ್ರೆ ವಾಸ ಮತ್ತು ಊಟ", "अस्पताल में भर्ती और खाना"),

    # ---- what it gives (NRLM) --------------------------------------------
    "nrlm-shg.gives.0": ("ಕೌಶಲ್ಯ ತರಬೇತಿ — ಆಹಾರ ಸಂಸ್ಕರಣೆ, ಪ್ಯಾಕಿಂಗ್, ಲೆಕ್ಕಪತ್ರ ನಿರ್ವಹಣೆ",
                         "कौशल प्रशिक्षण — खाद्य प्रसंस्करण, पैकेजिंग, हिसाब-किताब"),
    "nrlm-shg.gives.1": ("ಗುಂಪಿನಲ್ಲಿ ಉಳಿತಾಯದ ಅಭ್ಯಾಸ ಬೆಳೆಸುವುದು", "समूह में बचत की आदत बनाना"),
    "nrlm-shg.gives.2": ("ಇಡೀ ಗುಂಪು ಒಬ್ಬರಿಗೊಬ್ಬರು ಖಾತರಿ ನೀಡುವುದರಿಂದ ಸುಲಭ ಬ್ಯಾಂಕ್ ಸಾಲ",
                         "पूरा समूह एक-दूसरे की गारंटी देता है, इसलिए बैंक कर्ज़ आसान"),
    "nrlm-shg.gives.3": ("'ಬ್ಯಾಂಕ್ ಸಖಿ' ಸೇವೆ — ಬ್ಯಾಂಕ್ ಕೆಲಸದಲ್ಲಿ ಸಹಾಯ ಮಾಡುವ ತರಬೇತಿ ಪಡೆದ ಸ್ಥಳೀಯ ಮಹಿಳೆಯರು",
                         "'बैंक सखी' की सुविधा — बैंक के काम में मदद करने वाली प्रशिक्षित स्थानीय महिलाएँ"),

    # ---- documents --------------------------------------------------------
    "mudra.doc.0": ("ಆಧಾರ್ ಕಾರ್ಡ್", "आधार कार्ड"),
    "mudra.doc.1": ("ಪ್ಯಾನ್ ಕಾರ್ಡ್", "पैन कार्ड"),
    "mudra.doc.2": ("ಪಾಸ್‌ಪೋರ್ಟ್ ಗಾತ್ರದ ಫೋಟೋ", "पासपोर्ट साइज़ फ़ोटो"),
    "mudra.doc.3": ("ವ್ಯಾಪಾರ ಯೋಜನೆ (ಸರಳ ಒಂದು ಪುಟ ಸಾಕು)", "व्यापार योजना (एक सादा पन्ना भी चलेगा)"),
    "mudra.doc.4": ("ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರ", "बैंक खाते का विवरण"),

    "stand-up-india.doc.0": ("ಆಧಾರ್ + ಪ್ಯಾನ್", "आधार + पैन"),
    "stand-up-india.doc.1": ("ವಿಸ್ತೃತ ಯೋಜನಾ ವರದಿ", "विस्तृत परियोजना रिपोर्ट"),
    "stand-up-india.doc.2": ("ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ (SC/ST ವರ್ಗದಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿದರೆ ಮಾತ್ರ)", "जाति प्रमाण पत्र (केवल SC/ST श्रेणी में आवेदन करने पर)"),
    "stand-up-india.doc.3": ("ವ್ಯಾಪಾರ ಸ್ಥಳದ ವಿಳಾಸ ದಾಖಲೆ", "व्यापार स्थान का पता प्रमाण"),

    "ayushman-bharat.doc.0": ("ಆಧಾರ್ ಕಾರ್ಡ್", "आधार कार्ड"),
    "ayushman-bharat.doc.1": ("ಪಡಿತರ ಚೀಟಿ (ಇದ್ದರೆ)", "राशन कार्ड (अगर हो)"),

    "pm-vishwakarma.doc.0": ("ಆಧಾರ್ ಕಾರ್ಡ್", "आधार कार्ड"),
    "pm-vishwakarma.doc.1": ("ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬು ಅಥವಾ ಕೌಶಲ್ಯದ ಪುರಾವೆ", "परंपरागत कारीगरी या कौशल का प्रमाण"),
}

# ------------------------------------------------------------------- the quiz
STATES = [
    ("karnataka", "Karnataka", "ಕರ್ನಾಟಕ", "कर्नाटक"),
    ("maharashtra", "Maharashtra", "ಮಹಾರಾಷ್ಟ್ರ", "महाराष्ट्र"),
    ("tamil-nadu", "Tamil Nadu", "ತಮಿಳುನಾಡು", "तमिलनाडु"),
    ("telangana", "Telangana", "ತೆಲಂಗಾಣ", "तेलंगाना"),
    ("andhra-pradesh", "Andhra Pradesh", "ಆಂಧ್ರ ಪ್ರದೇಶ", "आंध्र प्रदेश"),
    ("kerala", "Kerala", "ಕೇರಳ", "केरल"),
    ("goa", "Goa", "ಗೋವಾ", "गोवा"),
    ("madhya-pradesh", "Madhya Pradesh", "ಮಧ್ಯ ಪ್ರದೇಶ", "मध्य प्रदेश"),
    ("uttar-pradesh", "Uttar Pradesh", "ಉತ್ತರ ಪ್ರದೇಶ", "उत्तर प्रदेश"),
    ("rajasthan", "Rajasthan", "ರಾಜಸ್ಥಾನ", "राजस्थान"),
    ("gujarat", "Gujarat", "ಗುಜರಾತ್", "गुजरात"),
    ("bihar", "Bihar", "ಬಿಹಾರ", "बिहार"),
    ("other", "Another state", "ಬೇರೆ ರಾಜ್ಯ", "दूसरा राज्य"),
]

QUIZ = [
    {"id": "state", "key": "sch.q.state", "hint": "sch.q.state.hint",
     "icon": "pin", "multi": False},
    {"id": "business", "key": "sch.q.business", "hint": "sch.q.business.hint",
     "icon": "building", "multi": False},
    {"id": "need", "key": "sch.q.need", "hint": "sch.q.need.hint",
     "icon": "hand-heart", "multi": True},
    {"id": "bank", "key": "sch.q.bank", "hint": "sch.q.bank.hint",
     "icon": "bank", "multi": False},
]

# options for the three non-state questions: (value, i18n key, icon)
QUIZ_OPTIONS = {
    "business": [
        ("starting", "sch.a.starting", "seed"),
        ("running", "sch.a.running", "building"),
    ],
    "need": [
        ("loan", "sch.a.loan", "rupee"),
        ("health", "sch.a.health", "shield"),
        ("skill", "sch.a.skill", "book"),
    ],
    "bank": [
        ("yes", "sch.a.yes", "bank"),
        ("no", "sch.a.no", "hand-heart"),
    ],
}

# ------------------------------------------------- where the coordinators are
# Sample field team. Replace with your own roster — the app only ever shows
# the one who covers the district a woman taps, and her phone number is a
# demo number.
DISTRICTS = [
    ("bengaluru-rural", "Bengaluru Rural", "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ", "बेंगलूरु ग्रामीण", "sc-bengaluru"),
    ("chikkaballapur", "Chikkaballapur", "ಚಿಕ್ಕಬಳ್ಳಾಪುರ", "चिक्कबल्लापुर", "sc-bengaluru"),
    ("tumakuru", "Tumakuru", "ತುಮಕೂರು", "तुमकुरु", "sc-bengaluru"),
    ("kolar", "Kolar", "ಕೋಲಾರ", "कोलार", "sc-bengaluru"),
    ("haveri", "Haveri", "ಹಾವೇರಿ", "हावेरी", "sc-haveri"),
    ("gadag", "Gadag", "ಗದಗ", "गडग", "sc-haveri"),
    ("koppal", "Koppal", "ಕೊಪ್ಪಳ", "कोप्पल", "sc-koppal"),
    ("ballari", "Ballari", "ಬಳ್ಳಾರಿ", "बल्लारी", "sc-koppal"),
    ("mandya", "Mandya", "ಮಂಡ್ಯ", "मांड्या", "sc-mandya"),
    ("mysuru", "Mysuru", "ಮೈಸೂರು", "मैसूर", "sc-mandya"),
    ("chitradurga", "Chitradurga", "ಚಿತ್ರದುರ್ಗ", "चित्रदुर्ग", "sc-chitradurga"),
    ("not-listed", "My district is not listed", "ನನ್ನ ಜಿಲ್ಲೆ ಪಟ್ಟಿಯಲ್ಲಿಲ್ಲ", "मेरा ज़िला सूची में नहीं है", "sc-bengaluru"),
]

COORDINATORS = [
    {"id": "sc-bengaluru", "name": "Lakshmamma B.", "phone": "+919000000001",
     "display": "+91 90000 00001", "area": "Bengaluru Rural · Chikkaballapur · Tumakuru · Kolar",
     "langs": "Kannada, Hindi"},
    {"id": "sc-haveri", "name": "Savitramma P.", "phone": "+919000000002",
     "display": "+91 90000 00002", "area": "Haveri · Gadag",
     "langs": "Kannada"},
    {"id": "sc-koppal", "name": "Basavaraj S.", "phone": "+919000000003",
     "display": "+91 90000 00003", "area": "Koppal · Ballari",
     "langs": "Kannada, Hindi"},
    {"id": "sc-mandya", "name": "Nagaraju K.", "phone": "+919000000004",
     "display": "+91 90000 00004", "area": "Mandya · Mysuru",
     "langs": "Kannada"},
    {"id": "sc-chitradurga", "name": "Girijamma H.", "phone": "+919000000005",
     "display": "+91 90000 00005", "area": "Chitradurga · Hosadurga",
     "langs": "Kannada"},
]

SCHEMES_CHECKED = "September 2026"


# -------------------------------------------------------------- app interface
# (english, kannada, hindi) — merged into i18n.STR by the build.
SCHEME_UI = {
    # category labels
    "sch.cat.loan": ("Loan", "ಸಾಲ", "कर्ज़"),
    "sch.cat.health": ("Health Insurance", "ಆರೋಗ್ಯ ವಿಮೆ", "स्वास्थ्य बीमा"),
    "sch.cat.group": ("Group Support & Training", "ಗುಂಪು ಬೆಂಬಲ ಮತ್ತು ತರಬೇತಿ", "समूह सहयोग और प्रशिक्षण"),
    "sch.cat.trade": ("Loan for traditional trades", "ಸಾಂಪ್ರದಾಯಿಕ ಕಸುಬಿಗೆ ಸಾಲ", "परंपरागत कारीगरी के लिए कर्ज़"),
    "sch.cat.market": ("Market & branding support", "ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಬ್ರ್ಯಾಂಡಿಂಗ್ ಸಹಾಯ", "बाज़ार और ब्रांडिंग सहयोग"),
    # hub
    "sch.eyebrow": ("Government Schemes", "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "सरकारी योजनाएँ"),
    "sch.title": ("Help you are already entitled to", "ನಿಮಗೆ ಈಗಾಗಲೇ ಸಿಗಬೇಕಾದ ಸಹಾಯ",
                  "वह मदद जो आपको पहले से मिलनी चाहिए"),
    "sch.lede": ("Answer 4 simple questions. We show only the schemes that fit you — never a long list.",
                 "4 ಸರಳ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ. ನಿಮಗೆ ಸರಿಹೊಂದುವ ಯೋಜನೆಗಳನ್ನು ಮಾತ್ರ ತೋರಿಸುತ್ತೇವೆ.",
                 "4 आसान सवालों के जवाब दें। हम सिर्फ़ आपके लिए सही योजनाएँ दिखाते हैं, लंबी सूची नहीं।"),
    "sch.start": ("Find my schemes", "ನನ್ನ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ", "मेरी योजनाएँ खोजें"),
    "sch.start.hint": ("About 2 minutes · nothing to type", "ಸುಮಾರು 2 ನಿಮಿಷ · ಏನೂ ಟೈಪ್ ಮಾಡಬೇಕಿಲ್ಲ",
                       "लगभग 2 मिनट · कुछ टाइप नहीं करना"),
    "sch.reset": ("Start again", "ಮತ್ತೆ ಪ್ರಾರಂಭಿಸಿ", "फिर से शुरू करें"),
    "sch.step": ("Step", "ಹಂತ", "चरण"),
    "sch.next": ("Next", "ಮುಂದೆ", "आगे"),
    "sch.back": ("Back", "ಹಿಂದೆ", "पीछे"),
    "sch.see": ("Show my schemes", "ನನ್ನ ಯೋಜನೆಗಳನ್ನು ತೋರಿಸಿ", "मेरी योजनाएँ दिखाएँ"),
    "sch.pick.one": ("Pick one", "ಒಂದನ್ನು ಆಯ್ಕೆಮಾಡಿ", "एक चुनें"),
    "sch.pick.many": ("You can pick more than one", "ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಆಯ್ಕೆ ಮಾಡಬಹುದು",
                      "आप एक से ज़्यादा चुन सकती हैं"),
    # questions
    "sch.q.state": ("What state are you in?", "ನೀವು ಯಾವ ರಾಜ್ಯದಲ್ಲಿದ್ದೀರಿ?", "आप किस राज्य में हैं?"),
    "sch.q.state.hint": ("Tap your state", "ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಒತ್ತಿ", "अपने राज्य पर टैप करें"),
    "sch.q.business": ("Do you already run a business, or are you starting one?",
                       "ನೀವು ಈಗಾಗಲೇ ಉದ್ಯಮ ನಡೆಸುತ್ತಿದ್ದೀರಾ, ಅಥವಾ ಪ್ರಾರಂಭಿಸುತ್ತಿದ್ದೀರಾ?",
                       "आप पहले से व्यापार चला रही हैं या शुरू कर रही हैं?"),
    "sch.q.business.hint": ("Tap the one that fits", "ಸರಿಹೊಂದುವುದನ್ನು ಒತ್ತಿ", "जो सही हो उस पर टैप करें"),
    "sch.q.need": ("Do you need a loan, health cover, or skill training?",
                   "ನಿಮಗೆ ಸಾಲ, ಆರೋಗ್ಯ ರಕ್ಷಣೆ ಅಥವಾ ಕೌಶಲ್ಯ ತರಬೇತಿ ಬೇಕೆ?",
                   "आपको कर्ज़, स्वास्थ्य बीमा या कौशल प्रशिक्षण चाहिए?"),
    "sch.q.need.hint": ("You can pick more than one", "ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಆಯ್ಕೆ ಮಾಡಬಹುದು",
                        "आप एक से ज़्यादा चुन सकती हैं"),
    "sch.q.bank": ("Do you have a bank account?", "ನಿಮಗೆ ಬ್ಯಾಂಕ್ ಖಾತೆ ಇದೆಯೇ?", "क्या आपका बैंक खाता है?"),
    "sch.q.bank.hint": ("Tap yes or no", "ಹೌದು ಅಥವಾ ಇಲ್ಲ ಒತ್ತಿ", "हाँ या नहीं टैप करें"),
    # answers
    "sch.a.starting": ("I'm starting one", "ಪ್ರಾರಂಭಿಸುತ್ತಿದ್ದೇನೆ", "शुरू कर रही हूँ"),
    "sch.a.running": ("I already run one", "ಈಗಾಗಲೇ ನಡೆಸುತ್ತಿದ್ದೇನೆ", "पहले से चला रही हूँ"),
    "sch.a.loan": ("A loan", "ಸಾಲ", "कर्ज़"),
    "sch.a.health": ("Health cover", "ಆರೋಗ್ಯ ರಕ್ಷಣೆ", "स्वास्थ्य बीमा"),
    "sch.a.skill": ("Skill training", "ಕೌಶಲ್ಯ ತರಬೇತಿ", "कौशल प्रशिक्षण"),
    "sch.a.yes": ("Yes", "ಇದೆ", "हाँ"),
    "sch.a.no": ("No", "ಇಲ್ಲ", "नहीं"),
    # results
    "sch.results.title": ("Schemes that fit you", "ನಿಮಗೆ ಸರಿಹೊಂದುವ ಯೋಜನೆಗಳು", "आपके लिए सही योजनाएँ"),
    "sch.results.sub": ("Tap a card to read it, or ask your Sakhi to help you apply.",
                        "ಕಾರ್ಡ್ ಒತ್ತಿ ಓದಿ, ಅಥವಾ ಅರ್ಜಿ ಹಾಕಲು ನಿಮ್ಮ ಸಖಿ ಸಹಾಯ ಕೇಳಿ.",
                        "कार्ड दबाकर पढ़ें, या आवेदन में मदद के लिए अपनी सखी से कहें।"),
    "sch.state.note": ("Our Sakhi Champions are in Karnataka today. Elsewhere, call the helpline on the card.",
                       "ನಮ್ಮ ಸಖಿ ಚಾಂಪಿಯನ್‌ಗಳು ಇಂದು ಕರ್ನಾಟಕದಲ್ಲಿದ್ದಾರೆ. ಬೇರೆ ರಾಜ್ಯಗಳಲ್ಲಿ ಕಾರ್ಡ್‌ನಲ್ಲಿರುವ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ.",
                       "हमारी सखी चैंपियन आज कर्नाटक में हैं। दूसरे राज्यों में कार्ड पर दिए हेल्पलाइन नंबर पर कॉल करें।"),
    "sch.results.none": ("Nothing matched exactly. Your Sakhi can still help — ask her.",
                         "ನಿಖರವಾಗಿ ಹೊಂದಿಕೆಯಾಗಲಿಲ್ಲ. ನಿಮ್ಮ ಸಖಿ ಸಹಾಯ ಮಾಡಬಲ್ಲರು.",
                         "कुछ ठीक से मेल नहीं खाया। आपकी सखी फिर भी मदद कर सकती हैं।"),
    "sch.why.loan": ("you need a loan", "ನಿಮಗೆ ಸಾಲ ಬೇಕು", "आपको कर्ज़ चाहिए"),
    "sch.why.health": ("you need health cover", "ನಿಮಗೆ ಆರೋಗ್ಯ ರಕ್ಷಣೆ ಬೇಕು", "आपको स्वास्थ्य बीमा चाहिए"),
    "sch.why.skill": ("you want training", "ನಿಮಗೆ ತರಬೇತಿ ಬೇಕು", "आपको प्रशिक्षण चाहिए"),
    "sch.why.new": ("you're starting a business", "ನೀವು ಉದ್ಯಮ ಪ್ರಾರಂಭಿಸುತ್ತಿದ್ದೀರಿ", "आप व्यापार शुरू कर रही हैं"),
    "sch.why.running": ("you already run a business", "ನೀವು ಈಗಾಗಲೇ ಉದ್ಯಮ ನಡೆಸುತ್ತಿದ್ದೀರಿ", "आप पहले से व्यापार चला रही हैं"),
    "sch.why.any": ("open to any rural woman", "ಯಾವುದೇ ಗ್ರಾಮೀಣ ಮಹಿಳೆಗೆ ತೆರೆದಿದೆ", "हर ग्रामीण महिला के लिए"),
    "sch.why.nobank": ("no bank account needed first", "ಮೊದಲು ಬ್ಯಾಂಕ್ ಖಾತೆ ಬೇಕಿಲ್ಲ", "पहले बैंक खाता ज़रूरी नहीं"),
    "sch.why.bank": ("you have a bank account", "ನಿಮಗೆ ಬ್ಯಾಂಕ್ ಖಾತೆ ಇದೆ", "आपका बैंक खाता है"),
    # card actions
    "sch.play": ("Play explainer", "ವಿವರಣೆ ಕೇಳಿ", "विवरण सुनें"),
    "sch.stop": ("Stop", "ನಿಲ್ಲಿಸಿ", "रोकें"),
    "sch.playing": ("Playing…", "ಪ್ಲೇ ಆಗುತ್ತಿದೆ…", "चल रहा है…"),
    "sch.transcript": ("Read instead", "ಓದಲು", "पढ़ें"),
    "sch.audio.unavailable": ("This phone cannot read it aloud — the text below says the same thing.",
                               "ಈ ಫೋನ್ ಓದಿ ಹೇಳಲು ಸಾಧ್ಯವಿಲ್ಲ — ಕೆಳಗಿನ ಬರಹದಲ್ಲಿ ಅದೇ ವಿಷಯವಿದೆ.",
                               "यह फ़ोन पढ़कर नहीं सुना सकता — नीचे लिखा हुआ वही बताता है।"),
    "sch.script.note": ("Recording not added yet — your phone reads it aloud.",
                        "ಧ್ವನಿ ಧ್ವನಿಮುದ್ರಣ ಇನ್ನೂ ಇಲ್ಲ — ನಿಮ್ಮ ಫೋನ್ ಓದಿ ಹೇಳುತ್ತದೆ.",
                        "रिकॉर्डिंग अभी नहीं है — आपका फ़ोन पढ़कर सुनाएगा।"),
    "sch.help": ("Request help applying", "ಅರ್ಜಿ ಹಾಕಲು ಸಹಾಯ ಕೇಳಿ", "आवेदन में मदद माँगें"),
    "sch.help.short": ("Request help", "ಸಹಾಯ ಕೇಳಿ", "मदद माँगें"),
    "sch.help.sub": ("A Sakhi will call you. No form to fill.", "ಸಖಿ ನಿಮಗೆ ಕರೆ ಮಾಡುತ್ತಾರೆ. ಯಾವುದೇ ಫಾರ್ಮ್ ಇಲ್ಲ.",
                     "सखी आपको कॉल करेंगी। कोई फ़ॉर्म नहीं भरना है।"),
    "sch.help.district": ("Which district are you in?", "ನೀವು ಯಾವ ಜಿಲ್ಲೆಯಲ್ಲಿದ್ದೀರಿ?", "आप किस ज़िले में हैं?"),
    "sch.help.confirm": ("Send request", "ವಿನಂತಿ ಕಳುಹಿಸಿ", "अनुरोध भेजें"),
    "sch.help.cancel": ("Cancel", "ರದ್ದುಮಾಡಿ", "रद्द करें"),
    "sch.help.done": ("Request sent", "ವಿನಂತಿ ಕಳುಹಿಸಲಾಗಿದೆ", "अनुरोध भेज दिया"),
    "sch.help.done.body": ("{sakhi} will call you within 24 hours.",
                           "{sakhi} ಅವರು 24 ಗಂಟೆಯೊಳಗೆ ಕರೆ ಮಾಡುತ್ತಾರೆ.",
                           "{sakhi} 24 घंटे के भीतर कॉल करेंगी।"),
    "sch.help.offline": ("Saved on this phone. It will send when you are online.",
                         "ಈ ಫೋನ್‌ನಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ. ಆನ್‌ಲೈನ್ ಆದಾಗ ಕಳುಹಿಸಲಾಗುತ್ತದೆ.",
                         "इस फ़ोन में सुरक्षित है। ऑनलाइन होने पर भेज दिया जाएगा।"),
    "sch.help.now": ("Or send it yourself now:", "ಅಥವಾ ಈಗಲೇ ನೀವೇ ಕಳುಹಿಸಿ:", "या अभी खुद भेजें:"),
    # requests list
    "sch.req.title": ("My requests", "ನನ್ನ ವಿನಂತಿಗಳು", "मेरे अनुरोध"),
    "sch.req.empty": ("No requests yet.", "ಇನ್ನೂ ಯಾವುದೇ ವಿನಂತಿ ಇಲ್ಲ.", "अभी कोई अनुरोध नहीं।"),
    "sch.req.pending": ("Waiting to send", "ಕಳುಹಿಸಲು ಕಾಯುತ್ತಿದೆ", "भेजने के लिए बाकी"),
    "sch.req.sent": ("Sent to your Sakhi", "ನಿಮ್ಮ ಸಖಿಗೆ ಕಳುಹಿಸಲಾಗಿದೆ", "आपकी सखी को भेज दिया"),
    "sch.req.whatsapp": ("Send on WhatsApp", "ವಾಟ್ಸಪ್‌ನಲ್ಲಿ ಕಳುಹಿಸಿ", "व्हाट्सऐप पर भेजें"),
    "sch.req.call": ("Call", "ಕರೆ ಮಾಡಿ", "कॉल करें"),
    "sch.req.remove": ("Remove", "ತೆಗೆದುಹಾಕಿ", "हटाएँ"),
    "sch.req.for": ("For", "ಇದಕ್ಕಾಗಿ", "इसके लिए"),
    # status / offline
    "sch.online": ("Online", "ಆನ್‌ಲೈನ್", "ऑनलाइन"),
    "sch.offline": ("Offline — cards saved on this phone", "ಆಫ್‌ಲೈನ್ — ಕಾರ್ಡ್‌ಗಳು ಈ ಫೋನ್‌ನಲ್ಲಿ ಉಳಿದಿವೆ",
                    "ऑफ़लाइन — कार्ड इस फ़ोन में सुरक्षित हैं"),
    "sch.saved": ("Saved for offline use", "ಆಫ್‌ಲೈನ್‌ಗಾಗಿ ಉಳಿಸಲಾಗಿದೆ", "ऑफ़लाइन के लिए सुरक्षित"),
    # how it works
    "sch.how.title": ("How this works", "ಇದು ಹೇಗೆ ನಡೆಯುತ್ತದೆ", "यह कैसे होता है"),
    "sch.how.1": ("Answer 4 questions", "4 ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ", "4 सवालों के जवाब दें"),
    "sch.how.2": ("See only the schemes that fit you", "ನಿಮಗೆ ಸರಿಹೊಂದುವ ಯೋಜನೆಗಳನ್ನು ಮಾತ್ರ ನೋಡಿ",
                  "सिर्फ़ अपने लिए सही योजनाएँ देखें"),
    "sch.how.3": ("Your Sakhi calls and applies with you", "ನಿಮ್ಮ ಸಖಿ ಕರೆ ಮಾಡಿ ಜೊತೆಗೆ ಅರ್ಜಿ ಹಾಕುತ್ತಾರೆ",
                  "आपकी सखी कॉल करके साथ में आवेदन करेंगी"),
    # card page
    "sch.gets.title": ("What you get", "ನಿಮಗೆ ಏನು ಸಿಗುತ್ತದೆ", "आपको क्या मिलेगा"),
    "sch.who.title": ("Who qualifies", "ಯಾರು ಅರ್ಹರು", "कौन पात्र है"),
    "sch.docs.title": ("Keep these ready", "ಇವುಗಳನ್ನು ಸಿದ್ಧವಾಗಿಟ್ಟುಕೊಳ್ಳಿ", "ये तैयार रखें"),
    "sch.docs.tick": ("Tick what you already have — we remember it on this phone.",
                      "ನಿಮ್ಮ ಬಳಿ ಇರುವುದನ್ನು ಗುರುತಿಸಿ — ಅದನ್ನು ಈ ಫೋನ್‌ನಲ್ಲಿ ನೆನಪಿಟ್ಟುಕೊಳ್ಳುತ್ತೇವೆ.",
                      "जो आपके पास है उस पर टिक करें — हम इसे इस फ़ोन में याद रखेंगे।"),
    "sch.apply.title": ("How to apply", "ಅರ್ಜಿ ಹೇಗೆ ಹಾಕುವುದು", "आवेदन कैसे करें"),
    "sch.helpline": ("Helpline", "ಸಹಾಯವಾಣಿ", "हेल्पलाइन"),
    "sch.check": ("Ask your Sakhi to check first", "ಮೊದಲು ನಿಮ್ಮ ಸಖಿ ಪರಿಶೀಲಿಸಲಿ", "पहले अपनी सखी से जाँच कराएँ"),
    "sch.full": ("Read the full card", "ಪೂರ್ಣ ಕಾರ್ಡ್ ಓದಿ", "पूरा कार्ड पढ़ें"),
    "sch.sakhi.title": ("Your Sakhi Champion", "ನಿಮ್ಮ ಸಖಿ ಚಾಂಪಿಯನ್", "आपकी सखी चैंपियन"),
    "sch.sakhi.area": ("Covers", "ವ್ಯಾಪ್ತಿ", "क्षेत्र"),
    "sch.sakhi.langs": ("Speaks", "ಮಾತನಾಡುವ ಭಾಷೆ", "भाषा"),
    "sch.all.title": ("All six schemes", "ಎಲ್ಲಾ ಆರು ಯೋಜನೆಗಳು", "सभी छह योजनाएँ"),
    "sch.all.lead": ("The trainer pages list every scheme, including the ones the quiz may not pick for you.",
                     "ತರಬೇತುದಾರರ ಪುಟಗಳಲ್ಲಿ ಎಲ್ಲಾ ಯೋಜನೆಗಳೂ ಇವೆ.",
                     "प्रशिक्षक पृष्ठों में हर योजना दी गई है।"),
    "sch.note.title": ("Please note", "ಗಮನಿಸಿ", "ध्यान दें"),
    "sch.note.body": ("This is guidance from ApnaPan, not an official government page. Rules and amounts change — confirm with the department or your Sakhi before you count on it.",
                      "ಇದು ApnaPan ನ ಮಾರ್ಗದರ್ಶನ, ಸರ್ಕಾರದ ಅಧಿಕೃತ ಪುಟ ಅಲ್ಲ. ನಿಯಮ ಮತ್ತು ಮೊತ್ತ ಬದಲಾಗುತ್ತವೆ — ಅಧಿಕೃತ ಕಚೇರಿ ಅಥವಾ ನಿಮ್ಮ ಸಖಿ ಜೊತೆ ದೃಢಪಡಿಸಿ.",
                      "यह ApnaPan की सलाह है, सरकारी आधिकारिक पृष्ठ नहीं। नियम और राशि बदलती रहती है — कार्यालय या अपनी सखी से पुष्टि करें।"),
    "sch.checked": ("Scheme details last checked", "ಯೋಜನೆ ವಿವರ ಕೊನೆಯ ಪರಿಶೀಲನೆ", "योजना विवरण अंतिम जाँच"),
    # trainer page (noindex, field team only)
    "sch.tr.title": ("Trainer notes", "ತರಬೇತುದಾರರ ಟಿಪ್ಪಣಿ", "प्रशिक्षक नोट्स"),
    "sch.tr.lead": ("Not part of the public site. Teaching order, cautions and the exact scheme data the app shows.",
                    "ಸಾರ್ವಜನಿಕ ಸೈಟ್‌ನ ಭಾಗ ಅಲ್ಲ.", "सार्वजनिक साइट का हिस्सा नहीं।"),
    "sch.tr.note": ("Teacher note", "ಶಿಕ್ಷಕರ ಟಿಪ್ಪಣಿ", "शिक्षक नोट"),
    "sch.tr.fields": ("Content team: edit these in _build/schemes.py",
                      "ಜವಾಬ್ದಾರಿ: _build/schemes.py ನಲ್ಲಿ ಸಂಪಾದಿಸಿ",
                      "सामग्री टीम: _build/schemes.py में संपादित करें"),
}


def strings():
    """{key: (en, kn, hi)} for every scheme + app string, ready for STR.update().

    Keys are namespaced `sch.<slug>.<field>`; the English text is taken from
    SCHEMES so it is never written twice.
    """
    out = {}
    by_slug = {s["slug"]: s for s in SCHEMES}

    def put(key, en, pair):
        out["sch." + key] = (en, pair[0], pair[1])

    for slug, s in by_slug.items():
        def i(field):
            return SCHEME_I18N[f"{slug}.{field}"]

        put(f"{slug}.name", s["name"], i("name"))
        put(f"{slug}.one_line", s["one_line"], i("one_line"))
        put(f"{slug}.benefit", s["benefit_amount"], i("benefit"))
        put(f"{slug}.who", s["who_qualifies"], i("who"))
        put(f"{slug}.how", s["how_to_apply"], i("how"))
        if s.get("check_first"):
            put(f"{slug}.check", s["check_first"], i("check"))
        if s.get("helpline"):
            num = s["helpline"].split(" (")[0]
            kn_label, hi_label = i("helpline_label")
            put(f"{slug}.helpline", s["helpline"], (f"{num} ({kn_label})", f"{num} ({hi_label})"))
        for n, doc in enumerate(s.get("documents_needed", [])):
            put(f"{slug}.doc.{n}", doc, i(f"doc.{n}"))
        for n, (_label, text) in enumerate(s.get("loan_tiers", [])):
            put(f"{slug}.tier_text.{n}", text, i(f"tier.{n}"))
        if s.get("repayment"):
            put(f"{slug}.repay", s["repayment"], i("repay"))
        for n, c in enumerate(s.get("coverage_includes", [])):
            put(f"{slug}.cover.{n}", c, i(f"cover.{n}"))
        for n, g in enumerate(s.get("what_it_gives", [])):
            put(f"{slug}.give.{n}", g, i(f"gives.{n}"))

    # shared titles that came along with the per-scheme lists
    for key in ("mudra.tiers_title",):
        slug, field = key.split(".")
        out[f"sch.{slug}.tiers_title"] = (("Loan amounts",) + SCHEME_I18N[key])

    out.update(SCHEME_UI)
    return out


def state_strings():
    """State + district names as i18n keys, so the quiz can translate them."""
    out = {}
    for sid, en, kn, hi in STATES:
        out[f"sch.state.{sid}"] = (en, kn, hi)
    for did, en, kn, hi, _sc in DISTRICTS:
        out[f"sch.district.{did}"] = (en, kn, hi)
    return out


def state_options():
    """[{id, key, icon}] for the state question, Karnataka first."""
    return [{"id": sid, "key": f"sch.state.{sid}", "icon": "pin"} for sid, *_ in STATES]


def coordinator(did):
    """The Sakhi Champion who covers a district id."""
    cid = next((c for d, _e, _k, _h, c in DISTRICTS if d == did), "sc-bengaluru")
    return next(c for c in COORDINATORS if c["id"] == cid)


def js_bundle(audio=None):
    """Everything the browser needs to run the quiz offline.

    `audio` maps slug -> [languages that have a recording] and is passed in by
    the build, which is the only place that can see the files on disk. The app
    uses it to choose between a real recorded voice and the phone's own voice.
    """
    audio = audio or {}
    schemes = []
    for s in SCHEMES:
        schemes.append({
            "id": s["id"], "slug": s["slug"], "name": s["name"], "cat": s["cat"],
            "icon": s["icon"], "one_line": s["one_line"], "benefit_amount": s["benefit_amount"],
            "tags": s["tags"], "needs_bank": s["needs_bank"], "available_in": s["available_in"],
            "check_first": bool(s.get("check_first")),
            "docs": len(s.get("documents_needed", [])),
            "audio": audio.get(s["slug"], []),
        })
    return {
        "schemes": schemes,
        "states": state_options(),
        "quiz": QUIZ,
        "quizOptions": {k: [{"value": v, "key": kk, "icon": i} for v, kk, i in opts]
                        for k, opts in QUIZ_OPTIONS.items()},
        "districts": [{"id": d, "key": f"sch.district.{d}", "sakhi": sc} for d, _e, _k, _h, sc in DISTRICTS],
        "coordinators": COORDINATORS,
        "checked": SCHEMES_CHECKED,
    }


def i18n_key(slug, field):
    return f"sch.{slug}.{field}"

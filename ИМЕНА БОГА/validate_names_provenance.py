#!/usr/bin/env python3
"""Fail-closed provenance graph validation for names research.

NOT a textual-critical apparatus, a remote source truth check, or a Product
publication license. This makes source and edition connections queryable
without silently manufacturing 105 independently certified interpretations.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
BASELINE_PATH = DATA / "names_ledger_v1.json"
EXTENSION_PATH = DATA / "names_extension_ledger_v1.json"
SOURCE_PATH = DATA / "source_access_register_v1.json"
EDITIONS_PATH = DATA / "names_edition_registry_v1.json"
CLAIMS_PATH = DATA / "names_claim_registry_v1.json"

EXPECTED_EDITIONS = {
    "ED-MECHON-MT-ONLINE",
    "ED-SBLGNT-2010-BIBLEGATEWAY",
    "ED-THGNT-2017-BIBLEGATEWAY",
    "ED-RAHLFS-HANHART-2006-PUBLISHER",
}
ED_MT = "ED-MECHON-MT-ONLINE"
ED_SBL = "ED-SBLGNT-2010-BIBLEGATEWAY"
ED_THG = "ED-THGNT-2017-BIBLEGATEWAY"
ED_LXX = "ED-RAHLFS-HANHART-2006-PUBLISHER"

# Four publisher-edition URLs were verified as single-version displays.
# These exact anchors protect against edition drift and wrong-verse substitutions.
# This is NOT a manuscript collation or independent scholarship review.
PINNED_GREEK_SOURCE_URLS = {
    "ATT-BASE-SABAOTH-05": "https://www.biblegateway.com/passage/?search=James+5%3A1-11&version=SBLGNT",
    "ATT-BASE-SABAOTH-06": "https://www.biblegateway.com/passage/?search=Romans+9%3A14-29&version=SBLGNT",
    "ATT-BASE-ABBA-03": "https://www.biblegateway.com/passage/?search=Galatians+4%3A4-7&version=SBLGNT",
    "ATT-EXT-KYRIOS-HO-THEOS-01": "https://www.biblegateway.com/passage/?search=Luke+1%3A30-33&version=THGNT",
    "ATT-BASE-IMMANUEL-05": "https://www.biblegateway.com/passage/?search=Matthew+1%3A23&version=SBLGNT",
    "ATT-BASE-ALPHA-OMEGA-01": "https://www.biblegateway.com/passage/?search=Revelation+1%3A4-8&version=SBLGNT",
    "ATT-BASE-PANTOKRATOR-01": "https://www.biblegateway.com/passage/?search=Revelation+1%3A4-8&version=SBLGNT",
    "ATT-BASE-ALPHA-OMEGA-02": "https://www.biblegateway.com/passage/?search=Revelation+21&version=SBLGNT",
    "ATT-EXT-ARCHE-TELOS-01": "https://www.biblegateway.com/passage/?search=Revelation+21&version=SBLGNT",
    "ATT-BASE-ALPHA-OMEGA-03": "https://www.biblegateway.com/passage/?search=Revelation+22&version=SBLGNT",
    "ATT-EXT-ARCHE-TELOS-02": "https://www.biblegateway.com/passage/?search=Revelation+22&version=SBLGNT",
    "ATT-BASE-RO-I-02": "https://www.biblegateway.com/passage/?search=John+10%3A11&version=SBLGNT",
    "ATT-EXT-POIMEN-HO-KALOS-01": "https://www.biblegateway.com/passage/?search=John+10%3A11&version=SBLGNT",
    "ATT-EXT-POIMEN-HO-KALOS-02": "https://www.biblegateway.com/passage/?search=John+10%3A14&version=SBLGNT",
    "ATT-BASE-EGO-EIMI-01": "https://www.biblegateway.com/passage/?search=John+6%3A20&version=SBLGNT",
    "ATT-BASE-EGO-EIMI-04": "https://www.biblegateway.com/passage/?search=John+18&version=SBLGNT",
    "ATT-BASE-EGO-EIMI-05": "https://www.biblegateway.com/passage/?search=John+18&version=SBLGNT",
    "ATT-BASE-EGO-EIMI-06": "https://www.biblegateway.com/passage/?search=John+18&version=SBLGNT",
}


def pinned_bible_gateway_passage(url: object, version: str, verse: object) -> bool:
    """Verify HTTPS host, exactly one edition, and coverage of the recorded verse.

    No network request is made here. The original publisher display is manually
    checked and its URL then locked into the evidence contract.
    """
    if not isinstance(url, str) or not isinstance(verse, str):
        return False
    try:
        page = urlsplit(url)
        if (page.scheme != "https" or page.hostname != "www.biblegateway.com"
            or page.path != "/passage/" or page.username or page.password
            or page.port is not None or page.fragment):
            return False
        values = parse_qs(page.query, keep_blank_values=True)
    except ValueError:
        return False
    if (values.get("version") != [version]
        or len(values.get("search", [])) != 1
        or any(k not in {"version", "search"} for k in values)):
        return False
    required = re.fullmatch(r"(.+?)\s+(\d+):(\d+)", verse)
    location = re.fullmatch(r"(.+?)\s+(\d+)(?::(\d+)(?:-(\d+))?)?", values["search"][0])
    if required is None or location is None:
        return False
    book, chapter, number = required.group(1).casefold(), int(required.group(2)), int(required.group(3))
    if book != location.group(1).casefold() or chapter != int(location.group(2)):
        return False
    start, end = location.group(3), location.group(4)
    return start is None or (int(start) <= number <= int(end or start))


PUBLISHER_LXX = {
    "EXO.3": "SRC-RAHLFS-EXODUS3",
    "EXO.17": "SRC-RAHLFS-EXODUS17",
    "ISA.7.14": "SRC-RAHLFS-ISAIAH",
}
CORE_CLAIMS = {
    "CLM-EX3-15-DIVINE-NAME",
    "CLM-IS43-10-NEGATED-EL",
    "CLM-IS43-12-YHWH-EL",
    "CLM-GEN22-14-PLACE-NAME",
    "CLM-EX17-15-ALTAR-MT-LXX",
    "CLM-JUD6-23-24-PEACE-ALTAR",
    "CLM-JOHN9-9-HUMAN-EGO-EIMI",
    "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
    "CLM-ABBA-THREE-PRAYER-SUBJECTS",
    "CLM-YHWH-HISTORICAL-PRONUNCIATION",
}
# The ten original research seeds and four new edition-pinned seeds are required
# minima, not a ceiling. These are digitally evidenced, not scholarly approved.
NEW_GREEK_SOURCE_CLAIMS = {
    "CLM-JAS5-4-SABAOTH-GENITIVE",
    "CLM-ROM9-29-SABAOTH-ISAIAH",
    "CLM-GAL4-6-ABBA-SPIRIT",
    "CLM-LUK1-32-GABRIEL-AGENT",
}
# The Exodus 3 referent/address correction is an independently inspectable
# semantic boundary, rather than a copied assertion from a static snapshot.
REQUIRED_EHYEH_ROLE_CLAIM = "CLM-EX3-EHYEH-DIVINE-REFERENT"
REQUIRED_EHYEH_IDS = {
    "ATT-BASE-EHYEH-01", "ATT-BASE-EHYEH-02", "ATT-BASE-EHYEH-03"
}
REQUIRED_PROPHETIC_NAMING_CLAIMS = {
    "CLM-JER23-6-DAVIDIC-ROYAL-NAME",
    "CLM-JER33-16-JERUSALEM-CITY-NAME",
    "CLM-EZ48-35-CITY-NAMING",
}
REQUIRED_ROCK_CLAIMS = {
    "CLM-DEUT32-ROCK-DIVINE-METAPHOR",
    "CLM-DEUT32-31-ROCK-CONTRAST",
    "CLM-DEUT32-37-FOREIGN-REFUGE",
}
# The first group may contain YHWH, the second contains TWO different
# referents, and the third is a polemic against foreign gods. Never certify
# a duplicated but semantically corrupted primary/contract reading.
ROCK_REFERENT_CONTROLS = {
    "ATT-BASE-TSUR-01": ("TRUE_GOD", True),
    "ATT-BASE-TSUR-02": ("TRUE_GOD", True),
    "ATT-BASE-TSUR-03": ("MIXED_TRUE_GOD_AND_OTHER_ROCK", None),
    "ATT-BASE-TSUR-04": ("FALSE_OBJECT_OF_REFUGE", False),
    "ATT-BASE-TSUR-05": ("TRUE_GOD", True),
}
REQUIRED_IMMANUEL_CLAIMS = {
    "CLM-ISA7-14-CHILD-NAMING",
    "CLM-ISA7-14-LXX-NAMING-VERB",
    "CLM-ISA8-8-IMMANUEL-ADDRESS",
    "CLM-ISA8-10-DIVINE-PRESENCE",
    "CLM-MATT1-23-IMMANUEL-GLOSS",
}
# Exact locus/role controls, not manuscripts or editorial interpretations.
IMMANUEL_PRINTED_SURFACES = {
    "ATT-BASE-IMMANUEL-01": "עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-02": "Εμμανουηλ",
    "ATT-BASE-IMMANUEL-03": "עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-04": "כִּי עִמָּנוּ אֵל",
    "ATT-BASE-IMMANUEL-05": "Ἐμμανουήλ",
}
IMMANUEL_ROLE_CONTROLS = {
    "ATT-BASE-IMMANUEL-01": ("prophetic_child_naming", "child in prophecy"),
    "ATT-BASE-IMMANUEL-02": ("prophetic_child_naming", "child in Isaiah prophecy"),
    "ATT-BASE-IMMANUEL-03": ("vocative_or_name_allusion", "Immanuel as addressee/allusion (contextual interpretation)"),
    "ATT-BASE-IMMANUEL-04": ("divine_presence_assertion", "God is with us, an assertion not new child-naming"),
    "ATT-BASE-IMMANUEL-05": ("christological_prophetic_quotation", "Jesus identified with prophetic name in quotation"),
}
REQUIRED_REVELATION_CLAIMS={
    "CLM-REV1-8-LORD-GOD-ALPHA","CLM-REV21-6-THRONE-SPEAKER",
    "CLM-REV22-13-CHRISTOLOGICAL-INFERENCE","CLM-REV1-8-SBL-TR-EXPANSION"}
REV_SPEAKER_CONTROLS={
    "ATT-BASE-ALPHA-OMEGA-01":("speaker","κύριος, ὁ θεός (Lord God)","speakerEvidence","explicit_speech_attribution_in_verse"),
    "ATT-BASE-PANTOKRATOR-01":("speaker","κύριος, ὁ θεός (Lord God)","speakerEvidence","explicit_speech_attribution_in_verse"),
    "ATT-BASE-ALPHA-OMEGA-02":("speaker","the one seated on throne","speakerEvidence","narrative_speaker_introduced_in_Revelation_21_5"),
    "ATT-EXT-ARCHE-TELOS-01":("speaker","the one seated upon throne, introduced at Revelation 21:5","speakerCue","narrator explicit at 21:5, continuous statement"),
    "ATT-BASE-ALPHA-OMEGA-03":("speaker","speaker inferred in immediate context; explicit I Jesus in 22:16","speakerEvidence","contextual_inference_with_intervening_angelic_speech"),
    "ATT-EXT-ARCHE-TELOS-02":("speaker","speaker in Rev22:12–13 inferred contextually; 22:16 explicit I Jesus","speakerCue","direct verse 13 not independently named; note angel interleaving"),
}
REQUIRED_LEXICAL_NAMING_CLAIMS = {
    "CLM-GEN1-DEUT6-DIVINE-ELOHIM",
    "CLM-EX20-OTHER-GODS-NEGATIVE",
    "CLM-EX34-DEUT32-POSITIVE-EL",
    "CLM-DEUT32-12-FOREIGN-EL-NEGATED",
    "CLM-JUD6-25-BAAL-ALTAR-DISTINCTION",
    "CLM-GEN35-7-EL-BETHEL-PLACE",
}
# Locus-specific invariants external to the baseline/contract copies. Fields
# here define independently tested referent, naming target, or morphology.
# These are digitally evidenced invariants, not a completed critical apparatus.
LEXICAL_NAMED_OBJECT_CONTROLS = {
    "ATT-BASE-ELOHIM-01": {
        "surface": "בָּרָא אֱלֹהִים",
        "contextRole": "creator_subject_singular_agreement",
        "referentClass": "SINGULAR_CREATOR_GOD",
        "isDivineDesignation": True,
        "verbAgreement": "בָּרָא Qal perfect 3ms (singular)",
    },
    "ATT-BASE-ELOHIM-02": {
        "surface": "אֱלֹהִים אֲחֵרִים",
        "contextRole": "other_gods_prohibited",
        "referentClass": "OTHER_GODS",
        "isDivineDesignation": False,
        "adjectiveAgreement": "אֲחֵרִים masculine plural",
        "verse": "Exodus 20:2 MT (English 20:3)",
    },
    "ATT-BASE-ELOHIM-03": {
        "surface": "יְהוָה אֱלֹהֵינוּ",
        "contextRole": "shema_confession",
        "isDivineDesignation": True,
        "verse": "Deuteronomy 6:4",
    },
    "ATT-BASE-EL-01": {
        "surface": "אֵל רַחוּם וְחַנּוּן",
        "referentClass": "YHWH",
        "speechAct": "divine_attributes_in_name_proclamation",
    },
    "ATT-BASE-EL-02": {
        "surface": "אֵל אֱמוּנָה",
        "referentClass": "YHWH",
        "speechAct": "divine_faithfulness_poetic_predication",
    },
    "ATT-BASE-EL-03": {
        "surface": "אֵל נֵכָר",
        "referentClass": "OTHER_GOD_NEGATED",
        "speechAct": "negative_foreign_god_contrast",
        "negationClause": "וְאֵין עִמּוֹ, אֵל נֵכָר",
        "isYHWH": False,
    },
    "ATT-BASE-SHALOM-03": {
        "surface": "מִזְבַּח הַבַּעַל",
        "namedObject": "Baal altar",
        "speechAct": "foreign_altar_to_be_destroyed",
        "isDivineName": False,
    },
    "ATT-BASE-EL-BETHEL-01": {
        "surface": "אֵל בֵּית-אֵל",
        "namedObject": "place",
        "referentClass": "place",
        "speechAct": "place_naming",
        "speaker": "Jacob",
    },
}
REQUIRED_COVENANT_SHEPHERD_CLAIMS = {
    "CLM-EX15-26-YHWH-HEALER",
    "CLM-JER17-14-HEAL-ME-PRAYER",
    "CLM-EX31-LEV20-YHWH-SANCTIFIES",
    "CLM-PS23-YHWH-MY-SHEPHERD",
    "CLM-JOHN10-JESUS-GOOD-SHEPHERD",
}
# Independent attestation-specific speech/morphology controls. Neither the
# copied locked data contracts nor a broad regex can override these boundaries.
COVENANT_SHEPHERD_CONTROLS = {
    "ATT-BASE-RAPHA-01": {
        "surface": "כִּי אֲנִי יְהוָה, רֹפְאֶךָ",
        "speechAct": "divine_self_predication",
        "namingActor": "YHWH, narration says 'he said'",
        "namedObject": "none",
        "morphology": "רֹפְאֶךָ active participle with 2ms suffix",
    },
    "ATT-BASE-RAPHA-02": {
        "surface": "רְפָאֵנִי יְהוָה וְאֵרָפֵא",
        "speechAct": "prayer_for_healing",
        "namingActor": "Jeremiah, direct address to YHWH",
        "morphology": "imperative + 1cs object; NOT participial רֹפְאֶךָ",
    },
    "ATT-BASE-MEKODDISHKEM-01": {
        "surface": "כִּי אֲנִי יְהוָה מְקַדִּשְׁכֶם",
        "speechAct": "divine_covenant_sanctification_predication",
        "morphology": "מְקַדִּשְׁכֶם participle with 2mp suffix",
        "covenantSetting": "Sabbath sign between YHWH and Israel",
        "namedObject": "none",
    },
    "ATT-BASE-MEKODDISHKEM-02": {
        "surface": "אֲנִי יְהוָה, מְקַדִּשְׁכֶם",
        "speechAct": "divine_covenant_sanctification_predication",
        "morphology": "מְקַדִּשְׁכֶם participle with 2mp suffix",
        "covenantSetting": "commandments and holiness regulations",
        "namedObject": "none",
    },
    "ATT-BASE-RO-I-01": {
        "surface": "יְהוָה רֹעִי",
        "speechAct": "poetic_shepherd_confession",
        "morphology": "רֹעִי 1cs suffix my shepherd; root רעה",
        "root": "רעה",
        "notSameRootAs": "ראה (Hagar's El-Roi seeing)",
    },
    "ATT-BASE-RO-I-02": {
        "surface": "Ἐγώ εἰμι ὁ ποιμὴν ὁ καλός",
        "namingActor": "Jesus",
        "speechAct": "christological_shepherd_self_description",
        "languageBoundary": "Greek NT self-predication not literal Hebrew Psalm transcription",
    },
    "ATT-EXT-POIMEN-HO-KALOS-01": {
        "surface": "ὁ ποιμὴν ὁ καλός",
        "narrativeSpeaker": "Jesus addressing hearers",
        "fullClause": "Ἐγώ εἰμι ὁ ποιμὴν ὁ καλός",
        "syntax": "EXPLICIT_NOMINAL_PREDICATE",
    },
    "ATT-EXT-POIMEN-HO-KALOS-02": {
        "surface": "ὁ ποιμὴν ὁ καλός",
        "narrativeSpeaker": "Jesus addressing hearers",
        "fullClause": "ἐγώ εἰμι ὁ ποιμὴν ὁ καλός",
        "syntax": "EXPLICIT_NOMINAL_PREDICATE",
    },
}
REQUIRED_JOHN_EGO_CONTEXT_CLAIMS = {
    "CLM-JOHN6-20-ASSURANCE",
    "CLM-JOHN18-5-ARREST-IDENTITY",
    "CLM-JOHN18-6-NARRATOR-REPRISE",
    "CLM-JOHN18-8-IDENTITY-AND-RELEASE",
}
# Per-locus source-text speech controls, independently specified in code rather
# than copied from ledger or narrative contract snapshots; not a manuscript collation.
JOHN_EGO_DISCOURSE_CONTROLS = {
    "ATT-BASE-EGO-EIMI-01": {
        "speaker": "Jesus",
        "speakerReferent": "Jesus",
        "speechAct": "identity_assurance_possible_theophanic_allusion",
        "speechTarget": "disciples on lake",
        "surface": "Ἐγώ εἰμι",
        "divineNameClaim": "CONTEXTUAL_THEOLOGICAL_INFERENCE_NOT_LEXICAL_PROOF",
        "claimScope": "Jesus self identification with do not be afraid; theophany possible interpretive layer",
    },
    "ATT-BASE-EGO-EIMI-04": {
        "speaker": "Jesus",
        "speakerReferent": "Jesus",
        "speechAct": "identity_answer_with_theological_narrative_potential",
        "speechTarget": "arresting party",
        "surface": "Ἐγώ εἰμι",
        "divineNameClaim": "CONTEXTUAL_THEOLOGICAL_INFERENCE_NOT_LEXICAL_PROOF",
        "claimScope": "Asked for Jesus the Nazarene; Jesus answers it is I",
    },
    "ATT-BASE-EGO-EIMI-05": {
        "speaker": "Jesus, reported in narration",
        "speakerReferent": "Jesus, reported in narration",
        "speechAct": "narrative_repetition_of_identity_answer",
        "speechTarget": "arresting party",
        "surface": "Ἐγώ εἰμι",
        "divineNameClaim": "CONTEXTUAL_THEOLOGICAL_INFERENCE_NOT_LEXICAL_PROOF",
        "claimScope": "people go backward and fall on ground after utterance; interpretation is narrative contextual",
    },
    "ATT-BASE-EGO-EIMI-06": {
        "speaker": "Jesus",
        "speakerReferent": "Jesus",
        "speechAct": "identity_answer_with_request_to_release_disciples",
        "speechTarget": "arresting party",
        "surface": "ἐγώ εἰμι",
        "divineNameClaim": "CONTEXTUAL_THEOLOGICAL_INFERENCE_NOT_LEXICAL_PROOF",
        "claimScope": "explicit εἰ οὖν ἐμὲ ζητεῖτε, ἄφετε τούτους",
    },
}
REQUIRED_YIREH_NISSI_CLAIMS = {
    "CLM-GEN22-8-ABRAHAM-PROVISION-ANSWER",
    "CLM-GEN22-14-MOUNTAIN-NIPHAL",
    "CLM-EX17-16-MT-HAND-THRONE-CRUX",
    "CLM-EX17-16-LXX-HIDDEN-HAND",
}
# Independent source-text observations; digital edited readings, not direct manuscript collation.
YIREH_NISSI_LOCI_GUARDS = {
    "ATT-BASE-YIREH-01": {
        "verse": "Genesis 22:8",
        "surface": "אֱלֹהִים יִרְאֶה-לּוֹ",
        "namingActor": "Abraham speaking",
        "namedObject": "none",
        "speechAct": "divine_provision_predication",
        "morphology": "יִרְאֶה Qal yiqtol 3ms (secondary preliminary)",
        "directAddress": "Abraham to Isaac",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0122.htm",
    },
    "ATT-BASE-YIREH-03": {
        "verse": "Genesis 22:14",
        "surface": "בְּהַר יְהוָה יֵרָאֶה",
        "namingActor": "narrator / community quotation",
        "namedObject": "none",
        "speechAct": "mountain_formula_about_appearance_or_provision",
        "morphology": "יֵרָאֶה Niphal yiqtol 3ms (secondary preliminary)",
        "notIdenticalVerbTo": "יִרְאֶה",
        "translationScope": "NET alternatives it will be seen/provided or YHWH will appear",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0122.htm",
    },
    "ATT-BASE-NISSI-03": {
        "verse": "Exodus 17:16",
        "surface": "כִּי-יָד עַל-כֵּס יָהּ",
        "namedObject": "none",
        "speechAct": "difficult_memorial_explanation",
        "textualStatus": "MT_SURFACE_AND_HYPOTHETICAL_EMENDATION_SEPARATE",
        "readingsUnderDebate": ["throne כֵּס (digital MT)","suggested emendation נֵס as scholarly reconstruction"],
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0217.htm",
    },
    "ATT-BASE-NISSI-04": {
        "verse": "Exodus 17:16",
        "surface": "ὅτι ἐν χειρὶ κρυφαίᾳ",
        "namedObject": "none",
        "speechAct": "different_Greek_explanation_of_memorial",
        "textualStatus": "LXX_READING_NOT_LITERAL_MT_HAND_THRONE",
        "sourceRelation": "PRINTED_GREEK_TRANSLATION_DIFFERENCE",
        "sourceUrl": "https://www.die-bibel.de/bibel/LXX/EXO.17",
    },
}
# Secondary source evidence explicitly remains attributed translator interpretation.
YIREH_NISSI_REQUIRED_SECONDARY = {
    "CLM-GEN22-14-MOUNTAIN-NIPHAL": {"SRC-MT-MECHON", "SRC-NET-GENESIS22"},
    "CLM-EX17-16-MT-HAND-THRONE-CRUX": {"SRC-MT-MECHON", "SRC-NET-EXODUS17"},
    "CLM-EX17-16-LXX-HIDDEN-HAND": {"SRC-MT-MECHON", "SRC-RAHLFS-EXODUS17"},
}
REQUIRED_SHADDAI_SABAOTH_CLAIMS = {
    "CLM-ELSHADDAI-GEN17-35-DIVINE-SELF",
    "CLM-ELSHADDAI-GEN28-ISAAC-BLESSING",
    "CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION",
    "CLM-SABAOTH-1SAM1-3-NARRATOR-WORSHIP",
    "CLM-SABAOTH-1SAM17-45-DAVID-BATTLE",
    "CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN",
    "CLM-SABAOTH-ZECH10-3-PROPHETIC-VOICE",
}
# Original printed MT observation guards; not historical-etymology proof.
SHADDAI_SABAOTH_CONTEXT_CONTROLS = {
    "ATT-BASE-EL-SHADDAI-01": {
        "verse": "Genesis 17:1",
        "surface": "אֵל שַׁדַּי",
        "speaker": "YHWH",
        "speechAct": "divine_self_identification",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0117.htm",
    },
    "ATT-BASE-EL-SHADDAI-02": {
        "verse": "Genesis 28:3",
        "surface": "וְאֵל שַׁדַּי",
        "speaker": "Isaac",
        "speechAct": "benediction",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0128.htm",
    },
    "ATT-BASE-EL-SHADDAI-03": {
        "verse": "Genesis 35:11",
        "surface": "אֵל שַׁדַּי",
        "speaker": "God",
        "speechAct": "divine_self_identification",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0135.htm",
    },
    "ATT-BASE-EL-SHADDAI-04": {
        "verse": "Exodus 6:3",
        "surface": "בְּאֵל שַׁדָּי",
        "speaker": "YHWH",
        "speechAct": "retrospective_revelation_statement",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0206.htm",
    },
    "ATT-BASE-SABAOTH-01": {
        "verse": "1 Samuel 1:3",
        "surface": "לַיהוָה צְבָאוֹת",
        "speaker": "narrator",
        "contextRole": "worship_destination",
        "originalPrefix": "לַ",
        "isDivineDesignation": True,
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt08a01.htm",
    },
    "ATT-BASE-SABAOTH-02": {
        "verse": "1 Samuel 17:45",
        "surface": "יְהוָה צְבָאוֹת",
        "speaker": "David addressing Goliath",
        "contextRole": "warrior_invocation",
        "contextClause": "אֱלֹהֵי מַעַרְכוֹת יִשְׂרָאֵל",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt08a17.htm",
    },
    "ATT-BASE-SABAOTH-03": {
        "verse": "Isaiah 6:3",
        "surface": "יְהוָה צְבָאוֹת",
        "speaker": "seraphim addressing each other",
        "contextRole": "heavenly_hymn",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt1006.htm",
    },
    "ATT-BASE-SABAOTH-04": {
        "verse": "Zechariah 10:3",
        "surface": "יְהוָה צְבָאוֹת",
        "speaker": "Zechariah, divine speech and third-person report intertwined",
        "contextRole": "prophetic_oracle",
        "referent": "YHWH attending to flock Judah",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt2310.htm",
    },
}
EX6_UNCERTAINTY_CONTROLS = {
    "etymologyStatus": "UNRESOLVED_MULTIPLE_HYPOTHESES",
    "revelationInterpretationStatus": "DISPUTED_NOT_RESOLVED_BY_ONE_NOTE",
    "speakerEvidenceLevel": "YHWH_RETROSPECTIVE_DIVINE_SPEECH",
}
REQUIRED_ELYON_QANNA_CLAIMS = {
    "CLM-ELYON-GEN14-18-PRIEST-NARRATOR",
    "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY",
    "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH",
    "CLM-QANNA-EX34-14-NAME-CHARACTER",
    "CLM-QANNA-DEUT4-24-MOSES-WARNING",
}
# Per-attestation independently verified MT printed-form and narrative actor controls.
ELYON_QANNA_LOCUS_CONTROLS = {
    "ATT-BASE-EL-ELYON-01": {
        "verse": "Genesis 14:18",
        "surface": "לְאֵל עֶלְיוֹן",
        "speaker": "narrator",
        "speechAct": "priesthood_designation",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0114.htm",
    },
    "ATT-BASE-EL-ELYON-02": {
        "verse": "Genesis 14:19",
        "surface": "לְאֵל עֶלְיוֹן",
        "speaker": "Melchizedek",
        "speechAct": "blessing",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0114.htm",
    },
    "ATT-BASE-EL-ELYON-03": {
        "verse": "Genesis 14:20",
        "surface": "אֵל עֶלְיוֹן",
        "speaker": "Melchizedek",
        "speechAct": "doxology",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0114.htm",
    },
    "ATT-BASE-EL-ELYON-04": {
        "verse": "Genesis 14:22",
        "surface": "יְהוָה אֵל עֶלְיוֹן",
        "speaker": "Abram",
        "speechAct": "oath_invocation",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0114.htm",
    },
    "ATT-BASE-EL-QANNA-01": {
        "verse": "Exodus 34:14",
        "surface": "קַנָּא שְׁמוֹ, אֵל קַנָּא",
        "speaker": "YHWH in divine speech to Moses, third-person self-reference",
        "contextRole": "name_statement_and_epithet_in_same_verse",
        "nameClause": "קַנָּא שְׁמוֹ",
        "descriptorClause": "אֵל קַנָּא הוּא",
        "contrast": "לְאֵל אַחֵר",
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0234.htm",
    },
    "ATT-BASE-EL-QANNA-02": {
        "verse": "Deuteronomy 4:24",
        "surface": "אֵל, קַנָּא",
        "speaker": "Moses warning Israel",
        "contextRole": "covenantal_warning_descriptor",
        "selfNamingInVerse": False,
        "sourceUrl": "https://mechon-mamre.org/p/pt/pt0504.htm",
    },
}
ELYON_QANNA_CLAIM_GUARDS = {
    "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY": {"creatorPossessorStatus": "NET_TRANSLATION_ALTERNATIVES_NOT_LEXICAL_CERTAINTY"},
    "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH": {
        "historicalHypothesisStatus": "ATTRIBUTED_GLOSS_HYPOTHESIS_NO_DIRECT_MANUSCRIPT_COLLATION",
        "creatorPossessorStatus": "NET_TRANSLATION_ALTERNATIVES_NOT_LEXICAL_CERTAINTY",
    },
    "CLM-QANNA-EX34-14-NAME-CHARACTER": {"nameEvidenceStatus": "EXPLICIT_NAME_CLAUSE_CHARACTER_EPITHET"},
    "CLM-QANNA-DEUT4-24-MOSES-WARNING": {"nameEvidenceStatus": "NO_NAME_CLAUSE_DESCRIPTIVE_EPITHET"},
}
ELYON_QANNA_SOURCE_TRIANGLES = {
    "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY": {"SRC-MT-MECHON", "SRC-NET-GEN14"},
    "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH": {"SRC-MT-MECHON", "SRC-NET-GEN14", "SRC-CARGILL-2019"},
}
# The original reviewed seeds are a required minimum, not a cap on future work.
# Additional claims must pass the same foreign-key, editorial and publication gates.
ALLOWED_CLAIM_TYPES = {
    "DIRECT_TEXTUAL_NAMING",
    "NEGATIVE_REFERENT_CONTROL",
    "POSITIVE_REFERENT_CONTROL",
    "NAMED_OBJECT_CONTROL",
    "EDITED_TEXT_DIFFERENCE",
    "NARRATIVE_SPEECH_VS_NAMING",
    "HUMAN_NEGATIVE_CONTROL",
    "CANONICAL_INTERTEXT_BOUNDARY",
    "SPEECH_AGENT_CONTROL",
    "ATTRIBUTED_HISTORICAL_RECONSTRUCTION",
    "MORPHOLOGICAL_CASE_CONTEXT",
    "CITATION_SPEECH_CONTEXT",
    "MIXED_REFERENT_CONTROL",
}
ALLOWED_INTERPRETIVE_SCOPES = {
    "NARROW_LOCUS_CLAIM_NOT_GENERAL_DICTIONARY_CLAIM",
    "AUTHOR_ARGUMENT_NOT_CLOSED",
}
ALLOWED_RELATION_TYPES = {
    "CONTRASTS_REFERENT",
    "CONTRASTS_NAMED_OBJECT",
    "LIMITS_INFERENCE",
    "REQUIRES_INDEPENDENT_ATTESTATION",
    "CONTRASTS_GRAMMATICAL_FORM",
    "SPECIFIES_SPEECH_AGENT",
    "CONTRASTS_SPEAKER_EVIDENCE",
    "CONTRASTS_PRINTED_EDITION",
}
# These four editorial comparisons must not silently disappear in later waves.
REQUIRED_SEMANTIC_RELATIONS = {
    "REL-IS43-EL-REFERENT": (
        "CLM-IS43-10-NEGATED-EL", "CLM-IS43-12-YHWH-EL", "CONTRASTS_REFERENT"
    ),
    "REL-MEMORIAL-PLACE-ALTAR": (
        "CLM-GEN22-14-PLACE-NAME", "CLM-EX17-15-ALTAR-MT-LXX",
        "CONTRASTS_NAMED_OBJECT"
    ),
    "REL-EGO-EIMI-CONTEXT": (
        "CLM-JOHN9-9-HUMAN-EGO-EIMI", "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
        "LIMITS_INFERENCE"
    ),
    "REL-YHWH-PRONUNCIATION": (
        "CLM-EX3-15-DIVINE-NAME", "CLM-YHWH-HISTORICAL-PRONUNCIATION",
        "REQUIRES_INDEPENDENT_ATTESTATION"
    ),
    "REL-SABAOTH-CASING-CONTEXT": (
        "CLM-JAS5-4-SABAOTH-GENITIVE", "CLM-ROM9-29-SABAOTH-ISAIAH",
        "CONTRASTS_GRAMMATICAL_FORM"
    ),
    "REL-ABBA-SPIRIT-SPEECH": (
        "CLM-ABBA-THREE-PRAYER-SUBJECTS", "CLM-GAL4-6-ABBA-SPIRIT",
        "SPECIFIES_SPEECH_AGENT"
    ),
    "REL-EX3-SELF-SPEECH-VS-ADDRESSEE": (
        "CLM-EX3-EHYEH-DIVINE-REFERENT",
        "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES",
        "SPECIFIES_SPEECH_AGENT"
    ),
    "REL-JER-ROYAL-CITY-NAMING": (
        "CLM-JER23-6-DAVIDIC-ROYAL-NAME",
        "CLM-JER33-16-JERUSALEM-CITY-NAME",
        "CONTRASTS_NAMED_OBJECT"
    ),
    "REL-JER-EZEK-CITY-NAME-LIMIT": (
        "CLM-JER33-16-JERUSALEM-CITY-NAME",
        "CLM-EZ48-35-CITY-NAMING",
        "LIMITS_INFERENCE"
    ),
    "REL-TSUR-DIVINE-AND-MIXED": (
        "CLM-DEUT32-ROCK-DIVINE-METAPHOR", "CLM-DEUT32-31-ROCK-CONTRAST",
        "CONTRASTS_REFERENT"
    ),
    "REL-TSUR-MIXED-AND-FOREIGN": (
        "CLM-DEUT32-31-ROCK-CONTRAST", "CLM-DEUT32-37-FOREIGN-REFUGE",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-MT-LXX-NAME": (
        "CLM-ISA7-14-CHILD-NAMING", "CLM-ISA7-14-LXX-NAMING-VERB",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-LXX-MATTHEW-VERB": (
        "CLM-ISA7-14-LXX-NAMING-VERB", "CLM-MATT1-23-IMMANUEL-GLOSS",
        "CONTRASTS_GRAMMATICAL_FORM"
    ),
    "REL-IMMANUEL-ISA8-ADDRESS-ASSERTION": (
        "CLM-ISA8-8-IMMANUEL-ADDRESS", "CLM-ISA8-10-DIVINE-PRESENCE",
        "LIMITS_INFERENCE"
    ),
    "REL-IMMANUEL-MT-MATTHEW-RECEPTION": (
        "CLM-ISA7-14-CHILD-NAMING", "CLM-MATT1-23-IMMANUEL-GLOSS",
        "REQUIRES_INDEPENDENT_ATTESTATION"
    ),
    "REL-REV-1-21-SPEAKER": ("CLM-REV1-8-LORD-GOD-ALPHA","CLM-REV21-6-THRONE-SPEAKER","CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-REV-21-22-SPEAKER": ("CLM-REV21-6-THRONE-SPEAKER","CLM-REV22-13-CHRISTOLOGICAL-INFERENCE","CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-REV-1-22-TITLE-CAUTION": ("CLM-REV1-8-LORD-GOD-ALPHA","CLM-REV22-13-CHRISTOLOGICAL-INFERENCE","LIMITS_INFERENCE"),
    "REL-REV-1-TR-PRINTED": ("CLM-REV1-8-LORD-GOD-ALPHA","CLM-REV1-8-SBL-TR-EXPANSION","CONTRASTS_PRINTED_EDITION"),
    "REL-ELOHIM-YHWH-OTHER": ("CLM-GEN1-DEUT6-DIVINE-ELOHIM", "CLM-EX20-OTHER-GODS-NEGATIVE", "CONTRASTS_REFERENT"),
    "REL-EL-YHWH-FOREIGN": ("CLM-EX34-DEUT32-POSITIVE-EL", "CLM-DEUT32-12-FOREIGN-EL-NEGATED", "CONTRASTS_REFERENT"),
    "REL-GIDEON-YHWH-BAAL-ALTAR": ("CLM-JUD6-23-24-PEACE-ALTAR", "CLM-JUD6-25-BAAL-ALTAR-DISTINCTION", "CONTRASTS_NAMED_OBJECT"),
    "REL-GEN35-PLACE-JUD6-ALTAR": ("CLM-GEN35-7-EL-BETHEL-PLACE", "CLM-JUD6-23-24-PEACE-ALTAR", "CONTRASTS_NAMED_OBJECT"),

    "REL-RAPHA-EXODUS-JEREMIAH-VOICE": ("CLM-EX15-26-YHWH-HEALER", "CLM-JER17-14-HEAL-ME-PRAYER", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-YHWH-SANCTIFY-HEAL-SUFFIX": ("CLM-EX15-26-YHWH-HEALER", "CLM-EX31-LEV20-YHWH-SANCTIFIES", "CONTRASTS_GRAMMATICAL_FORM"),
    "REL-PS23-JOHN10-SHEPHERD-BOUNDARY": ("CLM-PS23-YHWH-MY-SHEPHERD", "CLM-JOHN10-JESUS-GOOD-SHEPHERD", "LIMITS_INFERENCE"),

    "REL-JOHN6-JOHN18-SITUATION": ("CLM-JOHN6-20-ASSURANCE", "CLM-JOHN18-5-ARREST-IDENTITY", "LIMITS_INFERENCE"),
    "REL-JOHN18-5-6-REPRISE": ("CLM-JOHN18-5-ARREST-IDENTITY", "CLM-JOHN18-6-NARRATOR-REPRISE", "LIMITS_INFERENCE"),
    "REL-JOHN18-6-8-AGENCY": ("CLM-JOHN18-6-NARRATOR-REPRISE", "CLM-JOHN18-8-IDENTITY-AND-RELEASE", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-JOHN9-JOHN18-IDENTIFICATION": ("CLM-JOHN9-9-HUMAN-EGO-EIMI", "CLM-JOHN18-5-ARREST-IDENTITY", "CONTRASTS_REFERENT"),
    "REL-JOHN6-JOHN8-LXX-BOUNDARY": ("CLM-JOHN6-20-ASSURANCE", "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES", "LIMITS_INFERENCE"),
    "REL-GEN22-8-PLACE-NAMING-BOUNDARY": ("CLM-GEN22-8-ABRAHAM-PROVISION-ANSWER", "CLM-GEN22-14-PLACE-NAME", "CONTRASTS_NAMED_OBJECT"),
    "REL-GEN22-NAME-NIPHAL-DISTINCTION": ("CLM-GEN22-14-PLACE-NAME", "CLM-GEN22-14-MOUNTAIN-NIPHAL", "CONTRASTS_GRAMMATICAL_FORM"),
    "REL-EX17-ALTAR-VERSE16-CONTEXT": ("CLM-EX17-15-ALTAR-MT-LXX", "CLM-EX17-16-MT-HAND-THRONE-CRUX", "LIMITS_INFERENCE"),
    "REL-EX17-MT-LXX-SECRET-HAND": ("CLM-EX17-16-MT-HAND-THRONE-CRUX", "CLM-EX17-16-LXX-HIDDEN-HAND", "CONTRASTS_PRINTED_EDITION"),
    "REL-SHADDAI-SELF-BLESSING": ("CLM-ELSHADDAI-GEN17-35-DIVINE-SELF", "CLM-ELSHADDAI-GEN28-ISAAC-BLESSING", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-SHADDAI-GEN-EX6": ("CLM-ELSHADDAI-GEN17-35-DIVINE-SELF", "CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION", "LIMITS_INFERENCE"),
    "REL-SABAOTH-SHILOH-BATTLE": ("CLM-SABAOTH-1SAM1-3-NARRATOR-WORSHIP", "CLM-SABAOTH-1SAM17-45-DAVID-BATTLE", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-SABAOTH-BATTLE-SERAPHIM": ("CLM-SABAOTH-1SAM17-45-DAVID-BATTLE", "CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-SABAOTH-SERAPHIM-ZECH": ("CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN", "CLM-SABAOTH-ZECH10-3-PROPHETIC-VOICE", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-SABAOTH-ISA6-ROM9-QUOTE": ("CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN", "CLM-ROM9-29-SABAOTH-ISAIAH", "LIMITS_INFERENCE"),
    "REL-ELYON-PRIESTHOOD-BLESSING": ("CLM-ELYON-GEN14-18-PRIEST-NARRATOR", "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-ELYON-MELCHIZEDEK-ABRAM": ("CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY", "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-ELYON-YHWH-ORIGIN-BOUNDARY": ("CLM-ELYON-GEN14-18-PRIEST-NARRATOR", "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH", "LIMITS_INFERENCE"),
    "REL-QANNA-NAME-VERSUS-ATTRIBUTE": ("CLM-QANNA-EX34-14-NAME-CHARACTER", "CLM-QANNA-DEUT4-24-MOSES-WARNING", "CONTRASTS_SPEAKER_EVIDENCE"),
    "REL-QANNA-OTHER-GOD-CONTRAST": ("CLM-EX20-OTHER-GODS-NEGATIVE", "CLM-QANNA-EX34-14-NAME-CHARACTER", "CONTRASTS_REFERENT"),
}
CLAIM_REQUIRED_ATTESTATIONS = {
    "CLM-EX3-15-DIVINE-NAME": {"ATT-BASE-YHWH-01"},
    "CLM-IS43-10-NEGATED-EL": {"ATT-BASE-EL-04"},
    "CLM-IS43-12-YHWH-EL": {"ATT-BASE-EL-05"},
    "CLM-GEN22-14-PLACE-NAME": {"ATT-BASE-YIREH-02"},
    "CLM-EX17-15-ALTAR-MT-LXX": {"ATT-BASE-NISSI-01", "ATT-BASE-NISSI-02"},
    "CLM-JUD6-23-24-PEACE-ALTAR": {"ATT-BASE-SHALOM-01", "ATT-BASE-SHALOM-02"},
    "CLM-JOHN9-9-HUMAN-EGO-EIMI": {"ATT-BASE-EGO-EIMI-03"},
    "CLM-LXX-EX3-JOHN8-DIFFERENT-CLAUSES": {"ATT-BASE-EHYEH-03", "ATT-BASE-EGO-EIMI-02"},
    "CLM-ABBA-THREE-PRAYER-SUBJECTS": {"ATT-BASE-ABBA-01", "ATT-BASE-ABBA-02", "ATT-BASE-ABBA-03"},
    "CLM-YHWH-HISTORICAL-PRONUNCIATION": {"ATT-BASE-YHWH-01", "ATT-BASE-YHWH-02"},
    "CLM-JAS5-4-SABAOTH-GENITIVE": {"ATT-BASE-SABAOTH-05"},
    "CLM-ROM9-29-SABAOTH-ISAIAH": {"ATT-BASE-SABAOTH-06"},
    "CLM-GAL4-6-ABBA-SPIRIT": {"ATT-BASE-ABBA-03"},
    "CLM-LUK1-32-GABRIEL-AGENT": {"ATT-EXT-KYRIOS-HO-THEOS-01"},
    "CLM-EX3-EHYEH-DIVINE-REFERENT": {
        "ATT-BASE-EHYEH-01", "ATT-BASE-EHYEH-02", "ATT-BASE-EHYEH-03"
    },
    "CLM-JER23-6-DAVIDIC-ROYAL-NAME": {"ATT-BASE-TSIDKENU-01"},
    "CLM-JER33-16-JERUSALEM-CITY-NAME": {"ATT-BASE-TSIDKENU-02"},
    "CLM-EZ48-35-CITY-NAMING": {"ATT-BASE-SHAMMAH-01"},
    "CLM-DEUT32-ROCK-DIVINE-METAPHOR": {
        "ATT-BASE-TSUR-01", "ATT-BASE-TSUR-02", "ATT-BASE-TSUR-05"
    },
    "CLM-DEUT32-31-ROCK-CONTRAST": {"ATT-BASE-TSUR-03"},
    "CLM-DEUT32-37-FOREIGN-REFUGE": {"ATT-BASE-TSUR-04"},
    "CLM-ISA7-14-CHILD-NAMING": {"ATT-BASE-IMMANUEL-01"},
    "CLM-ISA7-14-LXX-NAMING-VERB": {"ATT-BASE-IMMANUEL-02"},
    "CLM-ISA8-8-IMMANUEL-ADDRESS": {"ATT-BASE-IMMANUEL-03"},
    "CLM-ISA8-10-DIVINE-PRESENCE": {"ATT-BASE-IMMANUEL-04"},
    "CLM-MATT1-23-IMMANUEL-GLOSS": {"ATT-BASE-IMMANUEL-05"},
    "CLM-REV1-8-LORD-GOD-ALPHA":{"ATT-BASE-ALPHA-OMEGA-01","ATT-BASE-PANTOKRATOR-01"},
    "CLM-REV21-6-THRONE-SPEAKER":{"ATT-BASE-ALPHA-OMEGA-02","ATT-EXT-ARCHE-TELOS-01"},
    "CLM-REV22-13-CHRISTOLOGICAL-INFERENCE":{"ATT-BASE-ALPHA-OMEGA-03","ATT-EXT-ARCHE-TELOS-02"},
    "CLM-REV1-8-SBL-TR-EXPANSION":{"ATT-BASE-ALPHA-OMEGA-01"},
    "CLM-GEN1-DEUT6-DIVINE-ELOHIM": {"ATT-BASE-ELOHIM-01","ATT-BASE-ELOHIM-03"},
    "CLM-EX20-OTHER-GODS-NEGATIVE": {"ATT-BASE-ELOHIM-02"},
    "CLM-EX34-DEUT32-POSITIVE-EL": {"ATT-BASE-EL-01","ATT-BASE-EL-02"},
    "CLM-DEUT32-12-FOREIGN-EL-NEGATED": {"ATT-BASE-EL-03"},
    "CLM-JUD6-25-BAAL-ALTAR-DISTINCTION": {"ATT-BASE-SHALOM-03"},
    "CLM-GEN35-7-EL-BETHEL-PLACE": {"ATT-BASE-EL-BETHEL-01"},

    "CLM-EX15-26-YHWH-HEALER": {"ATT-BASE-RAPHA-01"},
    "CLM-JER17-14-HEAL-ME-PRAYER": {"ATT-BASE-RAPHA-02"},
    "CLM-EX31-LEV20-YHWH-SANCTIFIES": {"ATT-BASE-MEKODDISHKEM-01", "ATT-BASE-MEKODDISHKEM-02"},
    "CLM-PS23-YHWH-MY-SHEPHERD": {"ATT-BASE-RO-I-01"},
    "CLM-JOHN10-JESUS-GOOD-SHEPHERD": {"ATT-BASE-RO-I-02", "ATT-EXT-POIMEN-HO-KALOS-01", "ATT-EXT-POIMEN-HO-KALOS-02"},

    "CLM-JOHN6-20-ASSURANCE": {"ATT-BASE-EGO-EIMI-01"},
    "CLM-JOHN18-5-ARREST-IDENTITY": {"ATT-BASE-EGO-EIMI-04"},
    "CLM-JOHN18-6-NARRATOR-REPRISE": {"ATT-BASE-EGO-EIMI-05"},
    "CLM-JOHN18-8-IDENTITY-AND-RELEASE": {"ATT-BASE-EGO-EIMI-06"},
    "CLM-GEN22-8-ABRAHAM-PROVISION-ANSWER": {"ATT-BASE-YIREH-01"},
    "CLM-GEN22-14-MOUNTAIN-NIPHAL": {"ATT-BASE-YIREH-03"},
    "CLM-EX17-16-MT-HAND-THRONE-CRUX": {"ATT-BASE-NISSI-03"},
    "CLM-EX17-16-LXX-HIDDEN-HAND": {"ATT-BASE-NISSI-04"},
    "CLM-ELSHADDAI-GEN17-35-DIVINE-SELF": {"ATT-BASE-EL-SHADDAI-01", "ATT-BASE-EL-SHADDAI-03"},
    "CLM-ELSHADDAI-GEN28-ISAAC-BLESSING": {"ATT-BASE-EL-SHADDAI-02"},
    "CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION": {"ATT-BASE-EL-SHADDAI-04"},
    "CLM-SABAOTH-1SAM1-3-NARRATOR-WORSHIP": {"ATT-BASE-SABAOTH-01"},
    "CLM-SABAOTH-1SAM17-45-DAVID-BATTLE": {"ATT-BASE-SABAOTH-02"},
    "CLM-SABAOTH-ISA6-3-SERAPHIM-HYMN": {"ATT-BASE-SABAOTH-03"},
    "CLM-SABAOTH-ZECH10-3-PROPHETIC-VOICE": {"ATT-BASE-SABAOTH-04"},
    "CLM-ELYON-GEN14-18-PRIEST-NARRATOR": {"ATT-BASE-EL-ELYON-01"},
    "CLM-ELYON-GEN14-19-20-PRIEST-BLESS-DOXOLOGY": {"ATT-BASE-EL-ELYON-02", "ATT-BASE-EL-ELYON-03"},
    "CLM-ELYON-GEN14-22-ABRAM-YHWH-OATH": {"ATT-BASE-EL-ELYON-04"},
    "CLM-QANNA-EX34-14-NAME-CHARACTER": {"ATT-BASE-EL-QANNA-01"},
    "CLM-QANNA-DEUT4-24-MOSES-WARNING": {"ATT-BASE-EL-QANNA-02"},
}


def validate_provenance(
    baseline: dict, extension: dict, sources: dict, editions: dict, claims: dict
) -> list[str]:
    errors: list[str] = []
    if editions.get("schemaVersion") != 1 or editions.get("corpusId") != "NAMES_OF_GOD_CANONICAL_DIGITAL_TEXT_EDITIONS":
        errors.append("provenance: wrong edition-registry version or authority")
    if claims.get("schemaVersion") != 1 or claims.get("corpusId") != "NAMES_OF_GOD_CLAIM_LEVEL_EVIDENCE":
        errors.append("provenance: wrong claim-registry version or authority")
    if editions.get("status") != "RESEARCH_ONLY_NOT_CRITICAL_MANUSCRIPT_EDITORIAL_APPROVAL":
        errors.append("provenance: edition registry improperly elevated to primary manuscript authority")

    source_rows = sources.get("records", [])
    source_map = {s["id"]: s for s in source_rows if isinstance(s, dict) and isinstance(s.get("id"), str)}
    if len(source_map) != len(source_rows):
        errors.append("provenance: missing or duplicate source IDs")
    if "SRC-SBLGNT-DIGITAL-NT" not in source_map:
        errors.append("provenance: no SBLGNT generic passage source, only license/other verse")

    edition_rows = editions.get("records", [])
    edition_map = {e["id"]: e for e in edition_rows if isinstance(e, dict) and isinstance(e.get("id"), str)}
    if len(edition_rows) != len(edition_map) or set(edition_map) != EXPECTED_EDITIONS:
        errors.append("provenance: four distinct stable edition IDs required")
    for edition_id, item in edition_map.items():
        if item.get("criticalEditionCollated") is not False or item.get("publicationState") != "BLOCKED":
            errors.append(f"provenance: edition {edition_id} was falsely promoted")
        permitted = item.get("sourceRecordIds", [])
        if not isinstance(permitted, list) or not permitted or any(x not in source_map for x in permitted):
            errors.append(f"provenance: edition {edition_id} has orphan source ID")
        if edition_id == ED_SBL:
            if item.get("publisherLicenseSourceId") != "SRC-SBLGNT-CCBY-LICENSE" or item.get("rightsState") != "RIGHTS_UNKNOWN":
                errors.append("provenance: SBLGNT host license improperly inherited from publisher")
        if edition_id in {ED_THG, ED_LXX} and item.get("rightsState") != "PERMISSION_REQUIRED":
            errors.append(f"provenance: copyright of Greek edition {edition_id} falsely waived")

    seen: set[str] = set()
    att_by_id: dict[str, dict] = {}
    num = 0
    for ledger_name, ledger, prefix, expected_count in (
        ("baseline", baseline, "BASE", 29),
        ("extension", extension, "EXT", 13),
    ):
        rows = ledger.get("records", [])
        if not isinstance(rows, list) or len(rows) != expected_count:
            errors.append(f"provenance: {ledger_name} record count changed")
            continue
        for parent in rows:
            if not isinstance(parent, dict):
                errors.append(f"provenance: invalid {ledger_name} record")
                continue
            candidate_id = parent.get("id", "")
            attestations = parent.get("attestations", [])
            if not isinstance(attestations, list) or not attestations:
                errors.append(f"provenance: {ledger_name}/{candidate_id} has no original-language usage")
                continue
            for obs in attestations:
                if not isinstance(obs, dict):
                    errors.append(f"provenance: invalid occurrence {candidate_id}")
                    continue
                num += 1
                aid = obs.get("attestationId")
                if not isinstance(aid, str) or not re.fullmatch(
                    rf"ATT-{prefix}-{re.escape(str(candidate_id).upper())}-[0-9]{{2,}}", aid
                ) or aid in seen:
                    errors.append(f"provenance: missing/duplicate/stale attestation ID {aid}")
                    continue
                seen.add(aid)
                att_by_id[aid] = obs
                if aid in ELYON_QANNA_LOCUS_CONTROLS:
                    for field, expected in ELYON_QANNA_LOCUS_CONTROLS[aid].items():
                        if obs.get(field) != expected:
                            errors.append(f"provenance: {aid} Elyon/Qanna actor/name/MT printed locus changed ({field})")
                if aid in SHADDAI_SABAOTH_CONTEXT_CONTROLS:
                    for field, expected in SHADDAI_SABAOTH_CONTEXT_CONTROLS[aid].items():
                        if obs.get(field) != expected:
                            errors.append(f"provenance: {aid} Shaddai/Sabaoth speaker and printed surface guard changed ({field})")
                if aid in YIREH_NISSI_LOCI_GUARDS:
                    for field, expected in YIREH_NISSI_LOCI_GUARDS[aid].items():
                        if obs.get(field) != expected:
                            errors.append(f"provenance: {aid} Gen22/Ex17 Hebrew or LXX locus text/role guard changed ({field})")
                if aid in JOHN_EGO_DISCOURSE_CONTROLS:
                    for field, expected in JOHN_EGO_DISCOURSE_CONTROLS[aid].items():
                        if obs.get(field) != expected:
                            errors.append(f"provenance: {aid} John6/18 speaker/discourse control changed ({field})")
                if aid in COVENANT_SHEPHERD_CONTROLS:
                    for field,expected in COVENANT_SHEPHERD_CONTROLS[aid].items():
                        if obs.get(field) != expected:
                            errors.append(f"provenance: {aid} covenant/shepherd speaker morphology/predicate corrupted ({field})")
                if aid in LEXICAL_NAMED_OBJECT_CONTROLS:
                    for k, expected in LEXICAL_NAMED_OBJECT_CONTROLS[aid].items():
                        if obs.get(k) != expected:
                            errors.append(f"provenance: {aid} lexical referent/named object/numbering guard violated ({k})")
                    if aid == "ATT-BASE-ELOHIM-02":
                        n = obs.get("numbering", {})
                        if (not isinstance(n,dict) or
                            n.get("mechonMamreHebrew") != "Exodus 20:2" or
                            n.get("commonEnglishRussian") != "Exodus 20:3"):
                            errors.append("provenance: Exodus 20 Hebrew versus common English/Russian numbering lost")
                if aid in REV_SPEAKER_CONTROLS:
                    sk,sv,ek,ev=REV_SPEAKER_CONTROLS[aid]
                    if obs.get(sk)!=sv or obs.get(ek)!=ev:
                        errors.append(f"provenance: {aid} Revelation speaker evidence conflated")
                    if obs.get("surface") not in {"τὸ Ἄλφα καὶ τὸ Ὦ","ὁ παντοκράτωρ","ἡ ἀρχὴ καὶ τὸ τέλος"}:
                        errors.append(f"provenance: {aid} Revelation printed title changed")
                if aid in IMMANUEL_ROLE_CONTROLS:
                    want_act, want_named = IMMANUEL_ROLE_CONTROLS[aid]
                    if obs.get("surface") != IMMANUEL_PRINTED_SURFACES[aid]:
                        errors.append(f"provenance: {aid} exact printed Immanuel source form changed")
                    if aid == "ATT-BASE-IMMANUEL-01":
                        if (obs.get("originalTerm") != "הָעַלְמָה"
                            or "grammatical dispute" not in str(obs.get("namingVerbAnalysis",""))):
                            errors.append("provenance: Isaiah 7 Hebrew lexeme/naming verb uncertainty erased")
                    if obs.get("speechAct") != want_act or obs.get("namedObject") != want_named:
                        errors.append(f"provenance: {aid} Immanuel speech act/named object conflated")
                    if aid == "ATT-BASE-IMMANUEL-02":
                        if (obs.get("namingVerbForm") != "καλέσεις second person singular"
                            or obs.get("crossEditionRelation") != "MATTHEW_SBLGNT_USES_καλέσουσιν_THIRD_PERSON_PLURAL"):
                            errors.append("provenance: LXX Isaiah καλέσεις vs Matthew καλέσουσιν contrast lost")
                    if aid == "ATT-BASE-IMMANUEL-05":
                        if (obs.get("namingVerbForm") != "καλέσουσιν 3rd plural"
                            or obs.get("translationInVerse") != "Μεθ’ ἡμῶν ὁ θεός"):
                            errors.append("provenance: Matthew Immanuel name grammar/gloss lost")
                if aid in ROCK_REFERENT_CONTROLS:
                    expected_ref, expected_divine = ROCK_REFERENT_CONTROLS[aid]
                    if (obs.get("referentClass") != expected_ref
                        or obs.get("isDivineDesignation") is not expected_divine):
                        errors.append(f"provenance: {aid} Rock referent/isDivineDesignation conflated")
                if aid in REQUIRED_EHYEH_IDS:
                    if obs.get("referent") != "God of Israel, the divine first-person speaker":
                        errors.append(f"provenance: {aid} divine self-reference wrongly attributed to addressee")
                    if obs.get("addressee") != "Moses":
                        errors.append(f"provenance: {aid} missing or incorrect speech addressee")
                    if not str(obs.get("speaker", "")).startswith(("God ", "YHWH ")):
                        errors.append(f"provenance: {aid} divine first-person speaker changed")
                edition_id = obs.get("editionId")
                source_id = obs.get("sourceId")
                edition = edition_map.get(edition_id, {})
                source = source_map.get(source_id, {})
                if not edition:
                    errors.append(f"provenance: {aid} has orphan edition {edition_id}")
                    continue
                if not source:
                    errors.append(f"provenance: {aid} has orphan source {source_id}")
                if source_id not in edition.get("sourceRecordIds", []):
                    errors.append(f"provenance: {aid} linked source not of that edition family")
                if obs.get("edition") not in edition.get("compatibleRawEditionStrings", []):
                    errors.append(f"provenance: {aid} printed edition text does not match its edition ID")
                if obs.get("language") not in edition.get("languageGroup", []):
                    errors.append(f"provenance: {aid} language does not fit edition")
                if not str(obs.get("sourceUrl", "")).startswith("https://"):
                    errors.append(f"provenance: {aid} exact original passage URL missing")
                if not str(obs.get("verse", "")).strip() or not str(obs.get("surface", "")).strip():
                    errors.append(f"provenance: {aid} lacks original script or verse locator")
                if obs.get("criticalEditionStatus") != "NOT_COLLATED":
                    errors.append(f"provenance: {aid} falsely certified critical apparatus")
                if obs.get("publicationState") not in (None, "BLOCKED"):
                    errors.append(f"provenance: {aid} unauthorized publication")
                if source and source.get("publicationState") != "BLOCKED":
                    errors.append(f"provenance: {aid} linked to unreviewed Product-approved source")
                if source and obs.get("rightsState") != source.get("rightsState"):
                    errors.append(f"provenance: {aid} rights changed from source-level citation")
                url = obs.get("sourceUrl", "")
                if edition_id == ED_MT:
                    correct = "SRC-DANIEL-ARAMAIC" if obs.get("language") == "aramaic" else "SRC-MT-MECHON"
                    if source_id != correct or "mechon-mamre.org" not in url:
                        errors.append(f"provenance: {aid} MT Aramaic/Hebrew source binding incorrect")
                if edition_id == ED_SBL:
                    if source_id != "SRC-SBLGNT-DIGITAL-NT":
                        errors.append(f"provenance: {aid} SBLGNT passage source incorrectly assigned")
                    if (obs.get("editionPinStatus") != "URL_VERSION_PINNED"
                        or not pinned_bible_gateway_passage(url, "SBLGNT", obs.get("verse"))):
                        errors.append(f"provenance: {aid} unpinned Greek edition or wrong SBLGNT verse")
                    expected_url = PINNED_GREEK_SOURCE_URLS.get(aid)
                    if expected_url is not None and url != expected_url:
                        errors.append(f"provenance: {aid} verified pinned Greek passage URL changed")
                if edition_id == ED_LXX:
                    match = [value for key, value in PUBLISHER_LXX.items() if key in url]
                    if len(match) != 1 or source_id != match[0] or "die-bibel.de" not in url:
                        errors.append(f"provenance: {aid} publisher LXX chapter/edition misattributed")
                if edition_id == ED_THG:
                    if source_id != "SRC-THGNT-LUKE" or aid != "ATT-EXT-KYRIOS-HO-THEOS-01":
                        errors.append(f"provenance: {aid} THGNT source or locus attribution invalid")
                    if (obs.get("editionPinStatus") != "URL_VERSION_PINNED"
                        or not pinned_bible_gateway_passage(url, "THGNT", obs.get("verse"))):
                        errors.append(f"provenance: {aid} THGNT multiedition display or wrong verse")
                    if url != PINNED_GREEK_SOURCE_URLS["ATT-EXT-KYRIOS-HO-THEOS-01"]:
                        errors.append(f"provenance: {aid} verified pinned THGNT passage URL changed")
    if num != 105 or len(seen) != 105:
        errors.append(f"provenance: all 105 current original-language attestations must be uniquely linked, not {num}/{len(seen)}")

    claim_rows = claims.get("records", [])
    if not isinstance(claim_rows, list):
        return errors + ["provenance: claim record list missing"]
    claim_map: dict[str, dict] = {}
    for idx, claim in enumerate(claim_rows):
        cid = claim.get("claimId") if isinstance(claim, dict) else None
        if not isinstance(cid, str) or not re.fullmatch(r"CLM-[A-Z0-9]+(?:-[A-Z0-9]+)*", cid):
            errors.append(f"provenance: malformed claim ID or record at index {idx}")
            continue
        if cid in claim_map:
            errors.append(f"provenance: duplicate claim ID {cid}")
            continue
        claim_map[cid] = claim
    if not CORE_CLAIMS.issubset(claim_map):
        errors.append("provenance: one or more original curated claim seeds missing")
    if not NEW_GREEK_SOURCE_CLAIMS.issubset(claim_map):
        errors.append("provenance: one or more Greek source-pinned claim seeds missing")
    if REQUIRED_EHYEH_ROLE_CLAIM not in claim_map:
        errors.append("provenance: Exodus 3 divine referent claim missing")
    if not REQUIRED_PROPHETIC_NAMING_CLAIMS.issubset(claim_map):
        errors.append("provenance: required prophetic royal/city claim boundary missing")
    if not REQUIRED_ROCK_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Rock contrast claim boundary missing")
    if not REQUIRED_IMMANUEL_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Immanuel textual role claims missing")
    if not REQUIRED_REVELATION_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Revelation speaker/edition claim missing")
    if not REQUIRED_LEXICAL_NAMING_CLAIMS.issubset(claim_map):
        errors.append("provenance: required lexical referent or named-object claim missing")
    if not REQUIRED_COVENANT_SHEPHERD_CLAIMS.issubset(claim_map):
        errors.append("provenance: required covenant and shepherd speech claims missing")
    if not REQUIRED_JOHN_EGO_CONTEXT_CLAIMS.issubset(claim_map):
        errors.append("provenance: required John6/18 discourse claims missing")
    if not REQUIRED_YIREH_NISSI_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Yireh/Nissi name-versus-explanation claims missing")
    if not REQUIRED_SHADDAI_SABAOTH_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Shaddai/Sabaoth speaker claims missing")
    if not REQUIRED_ELYON_QANNA_CLAIMS.issubset(claim_map):
        errors.append("provenance: required Elyon/Qanna speech/name claims missing")
    for cid, fields in ELYON_QANNA_CLAIM_GUARDS.items():
        row = claim_map.get(cid, {})
        for field, expected in fields.items():
            if row.get(field) != expected:
                errors.append(f"provenance: {cid} Elyon/Qanna cautious attribution and name evidence lost ({field})")
    for cid, needed in ELYON_QANNA_SOURCE_TRIANGLES.items():
        if not needed.issubset(set(claim_map.get(cid,{}).get("sourceIds", []))):
            errors.append(f"provenance: {cid} NET / Cargill attribution source link lost")
    ex6 = claim_map.get("CLM-ELSHADDAI-EX6-RETROSPECTIVE-REVELATION", {})
    for field, expected in EX6_UNCERTAINTY_CONTROLS.items():
        if ex6.get(field) != expected:
            errors.append(f"provenance: unresolved Shaddai Exodus6 hypothesis guard changed ({field})")
    if not {"SRC-MT-MECHON","SRC-NET-EXO6"}.issubset(set(ex6.get("sourceIds", []))):
        errors.append("provenance: NET Exodus6 attributed notes and MT source pairing lost")
    for cid, needed in YIREH_NISSI_REQUIRED_SECONDARY.items():
        if not needed.issubset(set(claim_map.get(cid,{}).get("sourceIds",[]))):
            errors.append(f"provenance: {cid} Hebrew/Greek or NET attributed source triangle lost")
    for cid,level,review in (
        ("CLM-REV1-8-LORD-GOD-ALPHA","EXPLICIT_SAME_VERSE",False),
        ("CLM-REV21-6-THRONE-SPEAKER","EXPLICIT_PRIOR_NARRATOR_CUE",False),
        ("CLM-REV22-13-CHRISTOLOGICAL-INFERENCE","CONTEXT_INFERRED_NOT_NAMED_AT_VERSE_13",True),
        ("CLM-REV1-8-SBL-TR-EXPANSION","PRINTED_VARIANT_NOT_NEW_SPEAKER",False)):
        r=claim_map.get(cid,{})
        if r.get("speakerEvidenceLevel")!=level or r.get("requiresIndependentSpeakerReview") is not review:
            errors.append(f"provenance: {cid} speaker evidence tier promoted")
    if not {"SRC-SBLGNT-DIGITAL-NT","SRC-TR1550-REV18","SRC-NET-REV1-8"}.issubset(
        set(claim_map.get("CLM-REV1-8-SBL-TR-EXPANSION",{}).get("sourceIds",[]))):
        errors.append("provenance: Revelation printed edition comparison lost direct sources")
    if "SRC-TABB-REVELATION22" not in claim_map.get("CLM-REV22-13-CHRISTOLOGICAL-INFERENCE",{}).get("sourceIds",[]):
        errors.append("provenance: Revelation 22 speaker commentary attribution lost")
    rock_statement = claim_map.get("CLM-DEUT32-31-ROCK-CONTRAST", {}).get("statement","")
    if not isinstance(rock_statement, str) or "32:30" not in rock_statement:
        errors.append("provenance: Deuteronomy 32:30 pronoun antecedent caution lost")
    for cid, claim in claim_map.items():
        if not isinstance(claim, dict):
            errors.append(f"provenance: malformed claim {cid}")
            continue
        refs = claim.get("attestationIds", [])
        sources_refs = claim.get("sourceIds", [])
        if (not isinstance(refs, list) or not refs
            or any(not isinstance(ref, str) for ref in refs)
            or len(refs) != len(set(refs))):
            errors.append(f"provenance: claim {cid} missing, non-string or duplicate text references")
            continue
        if (not isinstance(sources_refs, list) or not sources_refs
            or any(not isinstance(s, str) for s in sources_refs)
            or len(sources_refs) != len(set(sources_refs))):
            errors.append(f"provenance: claim {cid} lacking unique source references")
            continue
        expected = CLAIM_REQUIRED_ATTESTATIONS.get(cid)
        if expected is not None and set(refs) != expected:
            errors.append(f"provenance: claim {cid} lost its independently reviewed text witnesses")
        if claim.get("claimType") not in ALLOWED_CLAIM_TYPES:
            errors.append(f"provenance: claim {cid} has untyped editorial assertion")
        if claim.get("interpretiveScope") not in ALLOWED_INTERPRETIVE_SCOPES:
            errors.append(f"provenance: claim {cid} has unbounded interpretation")
        if claim.get("evidenceTier") != "DIGITAL_VERSE_SURFACE_AND_ATTRIBUTED_ARGUMENT":
            errors.append(f"provenance: claim {cid} overstates its evidence tier")
        needs = claim.get("reviewNeeded")
        if not isinstance(needs, list) or not needs or any(not isinstance(n, str) or not n.strip() for n in needs):
            errors.append(f"provenance: claim {cid} lacks pending independent review tasks")
        if any(r not in att_by_id for r in refs):
            errors.append(f"provenance: claim {cid} cites orphaned attestation")
        if any(r not in source_map for r in sources_refs):
            errors.append(f"provenance: claim {cid} cites orphaned source")
        if not set(refs).difference(att_by_id):
            required_sources = {att_by_id[r]["sourceId"] for r in refs}
            if not required_sources.issubset(set(sources_refs)):
                errors.append(f"provenance: claim {cid} lost mandatory direct textual sources")
        if (claim.get("criticalWitnessStatus") != "NOT_COLLATED"
            or claim.get("editorialState") != "RESEARCH_HOLD"
            or claim.get("publicationState") != "BLOCKED"):
            errors.append(f"provenance: claim {cid} falsely authorized for Product")
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"provenance: claim {cid} lacks factual language")

    relation_rows = claims.get("semanticRelations")
    if not isinstance(relation_rows, list):
        return errors + ["provenance: typed claim relations missing"]
    relation_ids: set[str] = set()
    relation_map: dict[str, tuple[str, str, str]] = {}
    for idx, relation in enumerate(relation_rows):
        if not isinstance(relation, dict):
            errors.append(f"provenance: malformed semantic relation at index {idx}")
            continue
        rid, src, dst, kind = (
            relation.get("relationId"), relation.get("fromClaimId"),
            relation.get("toClaimId"), relation.get("relationType")
        )
        if not isinstance(rid, str) or not re.fullmatch(r"REL-[A-Z0-9]+(?:-[A-Z0-9]+)*", rid):
            errors.append(f"provenance: invalid semantic relation ID at index {idx}")
            continue
        if rid in relation_ids:
            errors.append(f"provenance: duplicate semantic relation ID {rid}")
            continue
        relation_ids.add(rid)
        if (not isinstance(src, str) or not isinstance(dst, str)
            or src not in claim_map or dst not in claim_map or src == dst):
            errors.append(f"provenance: {rid} orphaned or self-referential claim edge")
            continue
        if kind not in ALLOWED_RELATION_TYPES:
            errors.append(f"provenance: {rid} unknown semantic relation type")
            continue
        if relation.get("publicationState") != "BLOCKED":
            errors.append(f"provenance: {rid} unlawfully promoted relationship")
        if not isinstance(relation.get("rationale"), str) or not relation["rationale"].strip():
            errors.append(f"provenance: {rid} lacks evidence-bounded explanation")
        relation_map[rid] = (src, dst, kind)
    for rid, expected in REQUIRED_SEMANTIC_RELATIONS.items():
        if relation_map.get(rid) != expected:
            errors.append(f"provenance: required semantic boundary {rid} missing or modified")
    return errors


def main() -> int:
    try:
        load = lambda path: json.loads(path.read_text(encoding="utf-8"))
        problems = validate_provenance(
            load(BASELINE_PATH), load(EXTENSION_PATH), load(SOURCE_PATH),
            load(EDITIONS_PATH), load(CLAIMS_PATH)
        )
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: provenance could not be loaded: {exc}", file=sys.stderr)
        return 1
    if problems:
        for p in problems:
            print("FAIL: " + p, file=sys.stderr)
        return 1
    print("PASS: 105 attestation IDs / 4 editions; 61 provisional claims, "
          "46 relations, 6 Elyon/Qanna original-text speaker controls and all publication HOLD gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

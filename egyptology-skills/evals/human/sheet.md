# Blind grading sheet

For each item, read the prompt and both answers. Do not try to guess which answer used a skill (some answers mention a skill or its files; ignore that), and do not reward length or formatting. Fill in `ratings-template.csv` (one row per item; copy it and name the copy for yourself).

- `better`: A, B or tie, for the answer a specialist would rather receive
- `a_correct_1to5`, `b_correct_1to5`: 1 = wrong or misleading, 3 = partly right, 5 = right and complete for the question asked
- `a_flags_doubt_y_n`, `b_flags_doubt_y_n`: does the answer say what it did not verify, assumed or is unsure about (y or n)
- `notes`: one line on anything a regular expression would miss

---

## P08

**Prompt:** Transliterate this sequence of Gardiner codes: G39 A1. Classify each sign, say which transliteration convention you use, say where the word ends, and flag anything ambiguous.

### Answer A

**Transliteration: sꜣ, "son"** (the alternative reading is sꜣ=ꞽ, "my son"; see below)

## Sign classification

| Gardiner | Sign | Function here | Value |
|---|---|---|---|
| **G39** | pintail duck | Biliteral phonogram | **sꜣ** |
| **A1** | seated man | Determinative (classifier) for "man, male person" | not pronounced |

G39 gives the whole sound of the word. A1 marks it as a word about a male person, which tells it apart from the many other words spelled with sꜣ, such as sꜣ "back" or sꜣ "protection". G39 + A1 (often with the stroke Z1 as well) is the standard spelling of sꜣ "son".

## Convention

I use the standard Egyptological transliteration found in Gardiner and Allen, written in Unicode characters:
- ꜣ (U+A723) for the aleph.
- ꞽ for yod, needed for the alternative reading below.
- `=` for the boundary between a noun and a suffix pronoun, following Leiden Unified Transliteration practice.

In Manuel de Codage ASCII this would be `zA`.

## Word boundary

The word ends **after A1**. Determinatives close a word, so A1 is the last sign of the lexeme and anything after it would start a new word. Because the word ends there, the reading is **sꜣ** and not *sꜣꞽ*.

## Ambiguities

1. **A1: determinative or suffix pronoun?** A1 can also write the 1st person singular suffix pronoun **=ꞽ** ("my"). G39 + A1 could therefore be **sꜣ=ꞽ, "my son"**, with the noun ending after G39 and =ꞽ attached to it. The determinative reading is the default for an isolated pair. A suffix reading becomes more likely when a speaker is talking about their own son, especially if a second A1 appears (determinative + suffix), or in formulas such as *sꜣ=ꞽ mrꞽ=ꞽ* "my beloved son". Only context can settle this.
2. **G39 vs G38.** G39 (pintail, sꜣ) is easily confused with **G38** (white-fronted goose, gb), especially in hieratic or worn inscriptions. If the sign is really G38, the reading changes completely, for example to the god Geb (gb). The sign identification is worth checking.
3. **Absent Z1.** Many attestations of "son" add the stroke Z1 after the duck (G39-Z1-A1). Leaving it out is normal and doesn't change the reading.
4. **Grammatical context.** Without surrounding text, sꜣ could stand alone, be the first part of a filiation formula (*sꜣ N* "son of N"), or be part of the royal title *sꜣ Rꜥ* "Son of Ra". The transliteration stays the same in each case, but how it is parsed and translated changes.

### Answer B

**Transliteration: *sꜣ*** (G39 A1). Written right to left, as 𓅭𓀀 in the usual layout.

**Convention:** I've used the current Egyptological letters (ꜣ, ꜥ, ḥ, ḫ, ẖ, š, q, ṯ, ḏ, …). I haven't checked these against the transliteration standard agreed at Leiden in 2023, so check them against whatever scheme your target publication follows. Gardiner's sign list prints some letters differently (for example ḳ where we now write q). This word doesn't use any of those letters, though.

| # | Glyph | Code | Role | Value | Confidence | Alternatives |
|---|---|---|---|---|---|---|
| 1 | 𓅭 | G39 (pintail duck) | Biliteral | *sꜣ* | High | Older reading *zꜣ* (see below) |
| 2 | 𓀀 | A1 (seated man) | Determinative (man, male person) | none | High | A1 can also be the first-person suffix *=ỉ* "I/my" (see below) |

**Word boundary:** the word ends after A1. A1 is a classifier that closes the word and puts it in the category "man", so it adds no sound. G39 alone writes the whole consonant skeleton. Nothing is written twice, so there's no phonetic complement to worry about.

**Things that are ambiguous:**

1. **s or z.** Old Egyptian kept *s* and *z* apart, and this word was originally *zꜣ*. Gardiner's sign list prints it as s (z) for that reason. For Middle Egyptian, *sꜣ* is standard. In an Old Kingdom text you might want *zꜣ*.
2. **Determinative or suffix pronoun.** After a noun, A1 can also stand for the first-person suffix, giving *sꜣ=ỉ* "my son". Here A1 is the last sign and nothing else is written, so the determinative reading is the more likely one. But the two signs can't settle it alone; the surrounding text decides. In many texts the determinative and the suffix are written as one sign, so a writing like this can sometimes mean "my son".
3. **Which word it is.** I've read this as *sꜣ* "son", the standard example in the sign list. G39 is only ever read as *sꜣ*, so the alternatives come down to which *sꜣ* word this is. The man determinative points to "son", but I haven't checked other words spelled the same way. I haven't translated it, since you asked only for the transliteration.
4. **Context.** I had only two sign codes, with no date, damage marks or surrounding text. If either sign is damaged or restored, these confidence grades no longer hold.

**Needs expert review:** whether to write *s* or *z* for the date of your text, and whether A1 here is a determinative or a suffix pronoun.

---

## P06

**Prompt:** An object was excavated in 1895 with a field register entry, sold in 1921 with a catalogue lot number, and given to a museum in 1982 by the collector's heirs, with only an oral account for that last step. Build the record, run the checker and tell me what can and cannot be said.

### Answer A

I built the record and ran the checker. The checker's self-test passed (27 checks). It returned **4 flags and 2 notes**. The record is at `scratchpad/record.json`. Names, the site, the entry number and the lot number are placeholders because you didn't give them.

## The record

| # | Date | Event | From → To | Evidence | Reference |
|---|---|---|---|---|---|
| 1 | 1895 | Excavation | — → Excavator A | Document | Field register, entry [no.] |
| 2 | 1921 | Sale | Excavator A → Collector B | Publication | Sale catalogue, lot [no.] |
| 3 | 1982 | Gift | Heirs of Collector B → Museum M | Oral | Oral account only |

**One assumption to check:** I recorded the excavator as the 1921 seller. You didn't say who sold it. If the seller was someone else, the checker would also flag a break between 1895 and 1921.

## Checker flags and what each means

1. **Undocumented event (1982 gift):** the step into the museum rests only on an oral account. The museum should have an accession register entry, a deed of gift or correspondence. Ask for them. Until one is found, this step can only be called "claimed".
2. **Broken chain (Collector B → heirs):** there is no record of the collector's death or of the object passing to the heirs, and the heirs aren't named. A will, probate inventory or estate papers would close this.
3. **26-year gap (1895–1921):** nothing records how the object went from the excavation to the sale. In particular, there is no export record or division of finds with the Egyptian authorities, so nothing shows how or when it left Egypt.
4. **61-year gap (1921–1982):** nothing records where the object was for six decades, including through the 1970 and 1973 benchmark years.

**Notes:** the object was first documented in 1895, before both benchmarks: the UNESCO Convention (1970) and the Archaeological Institute of America's publication cut-off (30 Dec 1973). The checker itself warns that this **does not show the object left Egypt lawfully**. It only shows when the object was first recorded.

## What can be said

**I haven't seen any of the documents myself.** So for now every step is at most "reported". It becomes "documented" only once someone examines the register and the catalogue.

- **Reported:** an object was recorded in the 1895 field register (entry no.) and in a 1921 sale catalogue (lot no.). This becomes "documented" once someone has examined both.
- **Claimed:** the collector's heirs gave the object to Museum M in 1982. At present this rests on an oral account.
- **Unknown:** how and when the object left Egypt, who held it between 1921 and 1982, and how ownership passed from the collector to the heirs.

## What cannot be said

- That the object left Egypt lawfully. The 1895 date doesn't establish this.
- That it has a continuous or complete provenance. It has two long gaps and one undocumented step.
- That Museum M acquired it lawfully or holds good title. Museum ownership doesn't prove that, and this is a question for counsel or the museum's provenance researcher, not for me.
- That the register object, the catalogue lot and the museum object are the same object. Nothing in the record yet links them: you need matching descriptions, dimensions, marks or labels. **This is the most important thing for a specialist to check.** The checker can't see it, and it also can't detect a forged or mis-dated document.

## Next steps

- Get the museum's accession file for the 1982 gift.
- Examine the field register and the catalogue, and check that their descriptions match the object.
- Look for estate papers for the collector and for any Egyptian export or division-of-finds record from 1895–1921.
- Check the policy of the venue where this will be published. The cut-off year differs: the AIA uses 1973 and ASOR is dated by 1970. Confirm the current rule on the venue's own page.
- Ask a provenance specialist about the gaps before you publish.

### Answer B

The workspace was empty, so there was no checker to run. I wrote one myself, along with the record, so the results only reflect the rules I gave it:

- `provenance_record.json` holds the three events, with what kind of evidence backs each one.
- `check_provenance.py` flags gaps in the chain, broken links between owners, weak evidence, missing citations, unconfirmed matches to this object, and missing legal paperwork.

**Result: 11 issues found, and the chain of ownership is not complete.**

## What can be said
- A field register records an excavation in 1895, and the register is a document.
- An object was offered at auction in 1921 under a known lot number, and the catalogue is a document.
- The collector's heirs say they gave the object to the museum in 1982. That rests on the oral account alone.

## What cannot be said, yet
1. **That these three records are the same object.** None of the sources has been checked against the object itself. Compare its description, size, inscriptions or excavation number with the register entry and the lot description. Until that's done, each step is only "an object."
2. **Who had it from 1895 to 1921.** That's 26 years with no known owner, and nobody knows who sold it in 1921. This is the biggest gap.
3. **That the collector bought it in 1921.** A lot number shows the object was offered, not who bought it, or even that it sold. You'd need an annotated copy of the catalogue, the auction house's sale records, or a receipt.
4. **How it passed from the collector to the heirs.** There's no death date, will or estate inventory.
5. **That the 1982 gift happened as told.** Spoken testimony is the weakest kind of evidence. Check the museum's own 1982 accession files first: a deed of gift, correspondence or a registrar's note would turn this step into a documented one.
6. **That it left the excavation site legally.** Nothing records a permit, an official division of finds, or export papers. In practice this matters as much as the ownership gaps.

## Wording you could use now
> "Possibly the object recorded in the [register] in 1895 (identification unconfirmed); possibly offered at [sale], 1921, lot [n] (buyer undocumented); by family account, given to the museum by the heirs of [collector], 1982. Provenance 1895–1921 unknown."

If you add the real names, citations and confirmed identifications to the JSON and run the checker again, the matching issues will clear. The 1895–1921 gap will stay until you find a document showing who had it.

---

## P03

**Prompt:** Check this reference list for references that might be invented or wrong: (1) Gardiner, A. H. Egyptian Grammar, 3rd ed. Oxford: Griffith Institute, 1957. (2) Nobody, N. 2019. A new reading of the Tale of Sinuhe. Journal of Egyptian Archaeology 105: 1-20. doi:10.1177/0307513319999999. (3) Faulkner, R. O. A Concise Dictionary of Middle Egyptian. Oxford: Griffith Institute, 1962.. Mark each one read, seen or recalled, run the citation checker on any with a DOI, and tell me which entries a librarian must confirm.

### Answer A

I couldn't run a citation checker on the DOI in entry 2. There's no checker tool in this workspace, which is empty, and none in my available tools. I tried to look the DOI up on Crossref as a substitute, but the web fetch wasn't approved. So no reference was checked against an outside source. Everything below comes from my own knowledge.

| # | Reference | Status | Notes |
|---|---|---|---|
| 1 | Gardiner, *Egyptian Grammar*, 3rd ed., Griffith Institute, 1957 | **Recalled** | A standard work; these details match what I know. |
| 2 | Nobody, N. 2019, "A new reading of the Tale of Sinuhe," *JEA* 105: 1–20, doi:10.1177/0307513319999999 | **Likely invented. DOI not checked.** | See below. |
| 3 | Faulkner, *A Concise Dictionary of Middle Egyptian*, Griffith Institute, 1962 | **Recalled** | A standard work; these details match what I know. Remove the stray double period at the end. |

**Why entry 2 looks fabricated:**
- "Nobody, N." is a placeholder name, not a real author.
- The DOI suffix `…19999999` is a filler pattern. Real *JEA* DOIs use the SAGE prefix `10.1177/03075133…`, but they don't end in a string of 9s.
- *JEA* volume 105 is the 2019 volume, so the volume and year agree. That only shows the citation was built to look right.

**For a librarian to confirm:**
- **Entry 2 (required):** check whether the DOI resolves and whether the article is listed in the *JEA* 105 table of contents. If it doesn't resolve, remove or replace the citation.
- **Entries 1 and 3 (optional):** I believe these details are correct, but they come from my memory, not a source I looked at. Have them checked against a library catalogue if this is going to be published.

If you approve web access, I can look up the DOI on Crossref and doi.org myself.

### Answer B

Entry (2) is almost certainly invented. Entries (1) and (3) look like real books, but I checked them from memory only, so a librarian still needs to confirm all three.

| # | Reference | Mark | Check result |
|---|---|---|---|
| 1 | Gardiner, *Egyptian Grammar*, 3rd ed., Griffith Institute, 1957 | **recalled** | No DOI. From memory, the 3rd revised edition is Oxford, Griffith Institute, 1957, so the entry looks right. I didn't check it against a library catalogue. |
| 2 | Nobody, N. 2019. "A new reading of the Tale of Sinuhe." *JEA* 105: 1–20. doi:10.1177/0307513319999999 | **recalled** | **The citation checker returned DOI-NOT-FOUND.** Crossref has no record of this DOI. |
| 3 | Faulkner, *A Concise Dictionary of Middle Egyptian*, Griffith Institute, 1962 | **recalled** | No DOI. From memory, the publisher and year are right. I didn't check it against a library catalogue. The entry ends with a stray double full stop ("1962..") that should be fixed. |

None of the entries is **read** or **seen**: I didn't open any of the sources or find any of them cited in another source during this check.

**Why entry 2 looks invented:**
- **The author:** "Nobody, N." is a placeholder name.
- **The DOI:** the "999999" ending looks made up, and the DOI doesn't exist. The 10.1177 prefix is right for the *Journal of Egyptian Archaeology* (published by SAGE), and volume 105 is the 2019 volume. That is what makes it look believable.
- **What a checker pass would mean:** if the DOI had resolved, it would only show that the record exists, not that the article says what it's cited for.

**What a librarian must confirm:**
- **Entry 2, first:** search the JEA 2019 table of contents and the Online Egyptological Bibliography for this title. If it can't be found, remove the entry. Don't replace it with a guessed real article.
- **Entries 1 and 3:** check edition, year and publisher in a library catalogue such as WorldCat or the Griffith Institute's list. The Gardiner grammar has had later reprints, so check that 1957 is the printing actually used.

---

## P05

**Prompt:** Design a small web app where students look up a hieroglyph by Gardiner code or by sound and see its Unicode character, readings and sources. Give me the data model, the rendering plan with fallbacks, and tests. Before we ship, check the licences of the data and fonts I plan to use: a Unicode hieroglyph web font and my own list of 86 signs checked against Gardiner's sign list.

### Answer A

I've written the design below. I couldn't do the licence check: the working directory is empty (no font file, no sign list), and you didn't name the font. What I can say about licences is in §5, marked as unverified until you send the files.

---

## 1. Scope

- **Users:** students. **Main task:** type a Gardiner code (`G17`) or a sound (`m`, `nfr`, `Hm`), get the sign, its Unicode character, its readings with roles, and where each reading comes from.
- **Smallest app that does this:** a static site built from one checked data file (`signs.json`, 86 signs). There's no server or database, and it works offline once the page has loaded.

## 2. Data model

The Gardiner code is the key. The Unicode character is worked out from it at build time and never typed by hand, because code points move as Unicode adds signs and variants.

```ts
type Role = "uniliteral" | "biliteral" | "triliteral" | "ideogram" | "determinative" | "marker";
type Status = "verified" | "VERIFY";

interface Sign {
  code: string;            // "G17" (display form); "G017" is the Unicode name form
  section: string;         // "G" (Birds)
  label: string;           // your own words, e.g. "owl"; never copied from Gardiner
  unicode: string | null;  // derived at build: "\u{13153}"; null if not encoded
  codepoint: string | null;// "U+13153"
  variantOf?: string;      // for variants and starred signs
  readings: Reading[];
}

interface Reading {
  value: string;           // Unicode transliteration: "ḥm"
  search: string;          // ASCII/MdC search form: "Hm"; generated, not hand-entered
  role: Role;
  source: Source;          // required; a reading without a source fails the build
  status: Status;
  checkedBy?: string; checkedOn?: string;
  note?: string;           // e.g. "phonetic complement in X"
}

interface Source {
  work: string;            // "Gardiner, Egyptian Grammar, 3rd ed. 1957, Sign-list"
  page?: string;           // "p. 469"
}
```

The project keeps one file of transliteration settings, `translit.json`, which also records the convention in use (e.g. `"convention": "Leiden 2023"`). Each source has its own convention, so `ꞽ`/`j`, `ḳ`/`q` and `s`/`z` stay distinct in storage and only get folded together in the search layer.

## 3. Search

- **By code:** normalise case and leading zeros: `g17`, `G017` and `G17` all map to `G17`. Also accept `Aa1` and `AA1`.
- **By sound:** the input is **case-sensitive**, because in MdC `h`, `H`, `x` and `X` are four different sounds (h, ḥ, ḫ, ẖ). Show a small on-screen keyboard (ꜣ ꞽ ꜥ ḥ ḫ ẖ š ḳ ṯ ḏ) so students can type the real letters. Map ASCII to Unicode with a single table:
  `A→ꜣ, i→ꞽ, a→ꜥ, H→ḥ, x→ḫ, X→ẖ, S→š, q→ḳ, T→ṯ, D→ḏ`. Equivalences such as ꞽ≡j and ḳ≡q are folded on purpose and listed in that same table.
- **Results:** exact matches first, then signs where the sound is one value among several (e.g. `m` finds G17 as a uniliteral before biliterals that contain m). Each hit shows its role, so a student can tell a uniliteral from a determinative.

## 4. Rendering plan and fallbacks

| Layer | Plan |
|---|---|
| Characters | The Unicode character from Egyptian Hieroglyphs (U+13000–U+1342F). Quadrat joiners (U+13430 onward) aren't needed for single-sign lookup, so they're left out of v1. |
| Font | Self-host the chosen web font (subset to your 86 signs plus the transliteration letters, if the licence allows subsetting). Use `font-display: swap`. |
| Coverage | At build time, read the font's cmap (fontTools) and write `coverage.json`. The build fails if a sign in `signs.json` isn't in the font, unless that sign is marked `fallback: true`. This beats runtime guessing. |
| Fallback 1 | If the sign is missing from the font (or `unicode` is null), show a box with the Gardiner code (`[G17]`) instead of tofu, so no data is silently lost. |
| Fallback 2 | If the web font fails to load (checked with `document.fonts.check`), switch to the code-box view and show a banner. |
| Always | Show the transliteration, code point and Unicode name as text next to the glyph. Give the glyph an `aria-label` like `"G17, owl, m"`. Use `lang="egy"`. |
| Copy | A "copy character" button copies the real Unicode character, not an image. |
| Caveat on page | The glyph is a standardised typeface form, not a facsimile. Sign shapes vary by period and medium. |

## 5. Licences: not checked yet, I need the files

Please send the font name and version (or the file with its `LICENSE`/OFL text), plus your sign list and a note on how it was made. Until then, here's what I know, all marked VERIFY:

- **Noto Sans Egyptian Hieroglyphs** (if that's your font): SIL Open Font License 1.1. Self-hosting and subsetting are allowed. You have to keep the licence text with the files, and a modified version can't use a Reserved Font Name. *VERIFY in the font's own OFL.txt.*
- **NewGardiner / JSesh fonts / others:** I'm not sure of the terms. I'm treating them as restricted until we read their licence.
- **Unicode data** (names and code points): the Unicode licence is permissive. Credit it.
- **Your 86-sign list:**
  - Codes, code points and the fact that "G17 reads m" are facts, and your own wording is yours.
  - Gardiner's *Egyptian Grammar* is very likely still under copyright in the UK (Gardiner died in 1963, and UK copyright runs life + 70 years, so to the end of 2033). Your list must not contain copied descriptions, scanned glyph images or OCR from the sign-list. Cite Gardiner by page.
  - If any of the 86 entries were pasted from a PDF or an online copy, tell me which ones and I'll flag them.
- **Your app's own licence:** pick one for `signs.json` (e.g. CC BY 4.0) and one for the code, and put both in the footer.

## 6. Tests

```python
# tests/test_signs.py  (pytest; run with python -I)
import json, re, unicodedata as ud, pytest
SIGNS = json.load(open("data/signs.json"))
COVER = set(json.load(open("build/coverage.json")))
ROLES = {"uniliteral","biliteral","triliteral","ideogram","determinative","marker"}

def uname(code):                       # "G17" -> "EGYPTIAN HIEROGLYPH G017"; "Aa1" -> "AA001"
    m = re.fullmatch(r"([A-Z][a-z]?)(\d+)([A-Za-z]?)", code)
    return f"EGYPTIAN HIEROGLYPH {m[1].upper()}{int(m[2]):03d}{m[3].upper()}"

def test_count_and_unique():
    codes = [s["code"] for s in SIGNS]
    assert len(codes) == 86 and len(set(codes)) == 86

@pytest.mark.parametrize("s", SIGNS, ids=lambda s: s["code"])
def test_code_resolves_to_one_char(s):
    if s["unicode"] is None: pytest.skip("not encoded")
    assert ud.lookup(uname(s["code"])) == s["unicode"]

@pytest.mark.parametrize("s", SIGNS, ids=lambda s: s["code"])
def test_readings_sourced(s):
    assert s["readings"]
    for r in s["readings"]:
        assert r["role"] in ROLES and r["source"]["work"] and r["status"] in {"verified","VERIFY"}

@pytest.mark.parametrize("s", SIGNS, ids=lambda s: s["code"])
def test_font_covers_or_falls_back(s):
    assert s["unicode"] is None or ord(s["unicode"]) in COVER or s.get("fallback")

def test_known_anchors():               # spot checks, verified against Python unicodedata (UCD 13.0)
    by = {s["code"]: s for s in SIGNS}
    for code, cp in {"D21":0x1308B, "G17":0x13153, "M17":0x131CB, "G43":0x13171, "N35":0x13216}.items():
        if code in by: assert ord(by[code]["unicode"]) == cp
```

```ts
// tests/search.test.ts (vitest)
test("code normalisation", () => {
  for (const q of ["G17","g17","G017"]) expect(byCode(q)?.code).toBe("G17");
  expect(byCode("aa1")?.code).toBe("Aa1");
});
test("sound search is case-sensitive", () => {
  expect(bySound("h").map(c)).not.toEqual(bySound("H").map(c)); // h ≠ ḥ
  expect(bySound("H")).toEqual(bySound("ḥ"));                     // ASCII = Unicode form
});
test("ꞽ/j folding is deliberate", () => expect(bySound("j")).toEqual(bySound("ꞽ")));
test("uniliteral ranks first", () => expect(bySound("m")[0].code).toBe("G17"));
test("missing glyph shows code box", () => {
  render(<Glyph sign={{code:"X99", unicode:null}} />);
  expect(screen.getByText("[X99]")).toBeVisible();
});
test("translit round-trip", () => {
  for (const s of ["nfr","Hm","Ax","Dd"]) expect(toAscii(toUnicode(s))).toBe(s);
});
```

The automated tests don't cover two things:
- **Browsers:** a manual render pass on Chrome, Firefox and Safari (iOS too), with a screenshot of all 86 signs.
- **Specialist check:** show an Egyptologist 10 random records and count how many they dispute. A dispute rate above 0 means re-checking the whole list.

---

**Before shipping I need from you:** the font name or file with its licence, and your sign list with how the descriptions were made. With those I'll do the licence check, run the tests against your real data, and flag any readings with a missing source.

### Answer B

I can give you the design and tests now. I couldn't do the licence check yet: the working directory is empty and you haven't said which font. That section lists what I need from you and what I already know.

## 1. Data model

```ts
type GardinerCode = string;          // canonical form: "A1", "Aa15", "N35a", "NL1", "NU12"

interface Sign {
  code: GardinerCode;                // primary key
  codepoint: number | null;          // 0x13000; null if not encoded in Unicode
  unicodeName: string | null;        // "EGYPTIAN HIEROGLYPH A001" (copied from the UCD, not typed by hand)
  unicodeVersion: string;            // "5.2", "16.0" — the rendering plan uses this
  category: string;                  // "A" (Man and his occupations) … "Aa"
  description: string;               // YOUR wording, not Gardiner's
  readings: Reading[];
  sourceRefs: SourceRef[];           // at least one per sign
  checkedAgainstGardiner: { date: string; by: string; note?: string };
}

interface Reading {
  translit: string;                  // Unicode Egyptological form: "ḥtp", "ꜣ", "ꞽ"
  mdc: string;                       // Manuel de Codage ASCII: "Htp", "A", "i" (case-sensitive!)
  searchKey: string;                 // derived from mdc at build time, never hand-edited
  function: "uniliteral" | "biliteral" | "triliteral" | "logogram" | "determinative" | "ideogram";
  gloss?: string;                    // "offering; be satisfied"
  sourceRefs: SourceRef[];
}

interface Source { id: string; citation: string; url?: string; licence: string; }
interface SourceRef { sourceId: string; locator?: string; } // page or section
```

Store it as one `signs.json` plus `sources.json`. A build script checks both against the schema and the Unicode Character Database, then writes two lookup indexes:

- **By code:** normalised code → sign.
- **By sound:** searchKey → list of signs.

**Pitfalls to design for:**

- **Gardiner codes.** Parse them with `^(Aa|NL|NU|[A-IK-Z])0*(\d{1,3})([a-z]?)$`. Gardiner has no J category, and Aa is a separate category from A. Accept `a1`, `A001` and `aa1`. Map to Unicode names by zero-padding the number and upper-casing the variant letter (N35a → `N035A`).
- **Sound search.** In MdC, case changes the sound: `h` (h) ≠ `H` (ḥ), `s` ≠ `S` (š), `t`/`T` (ṯ), `d`/`D` (ḏ), `x` (ḫ) ≠ `X` (ẖ). So don't lowercase the query. Map Unicode input to MdC: ꜣ U+A723→`A`, ꜥ U+A725→`a`, all yod forms (ꞽ U+A7BD, i͗, i̯, j)→`i`, ḥ→`H`, ḫ→`x`, ẖ→`X`, š→`S`, ṯ→`T`, ḏ→`D`, ḳ/q→`q`. Normalise to NFC first.
- **Typing help.** Offer a "loose" toggle that ignores the dots, for students who can't type them. Rank exact matches first.

## 2. Rendering plan with fallbacks

Every sign card always shows the code, U+ codepoint and Unicode name as text, so the card is never blank. The glyph goes through this chain:

1. **Self-hosted web font**, subset to your 86 codepoints as woff2, with `font-display: swap`:
   `font-family: "AppHiero", "Noto Sans Egyptian Hieroglyphs", "Segoe UI Historic", sans-serif;`
2. **Glyph check.** After `document.fonts.load('1em AppHiero', char)`, draw the character in a canvas twice: once in the stack, once in a font known to lack it. If the widths match, or the result is the .notdef box, the glyph is missing and you drop to step 3.
3. **SVG of the sign**, only if you have a licence for those drawings (see §4).
4. **Text only.** Show "Glyph not available in your font" plus the code and name.

**Other rendering points:**

- **Newer signs.** Signs in Egyptian Hieroglyphs Extended-A (U+13460–U+143FF, Unicode 16) usually aren't in the common fonts. Mark them using `unicodeVersion` and go straight to the SVG.
- **Markup.** Use `<span lang="egy-Egyp" role="img" aria-label="A1, seated man">`, at a large size (≥48px).
- **Format controls.** Don't rely on the quadrat controls (U+13430+) for layout. Show single signs only.

## 3. Tests

```ts
// unit — parsing & search
test.each([["a1","A1"],["A001","A1"],["aa1","Aa1"],["n35A","N35a"],["nl1","NL1"]])
  ("normalises %s", (i, o) => expect(normaliseCode(i)).toBe(o));
test("rejects J and junk", () => ["J1","A","Z1000",""].forEach(c => expect(normaliseCode(c)).toBeNull()));
test("MdC is case-sensitive", () => expect(search("h")).not.toEqual(search("H")));
test("Unicode ↔ MdC equivalence", () => expect(search("ḥtp")).toEqual(search("Htp")));
test("all yod forms match", () => ["ꞽ","i͗","i̯","j","i"].forEach(y => expect(search(y)).toContainCode("M17")));
test("NFD input works", () => expect(search("ḥ".normalize("NFD"))).toEqual(search("H")));

// data integrity — runs in CI against signs.json + UCD
test("exactly 86 signs, unique codes and codepoints");
test("unicodeName matches the UCD name for codepoint");          // catches A1/A001 typos
test("UCD name ↔ Gardiner code agree (A001 ⇔ A1, N035A ⇔ N35a)");
test("every sign and reading has ≥1 sourceRef that resolves");
test("searchKey === deriveKey(mdc) for every reading");
test("every glyph in signs.json exists in the subset font cmap"); // fontTools in CI

// browser (Playwright)
test("renders glyph with web font");
test("font request blocked → SVG fallback, code+name still visible");
test("Extended-A sign uses fallback without flashing tofu");
test("axe: no a11y violations; glyph has accessible name");
```

## 4. Licence check: not done yet

I can't check licences on files I haven't seen. Please send:

- **The font:** its exact name and version, plus the licence file that comes with it.
- **Your sign list:** the file itself, and a note on where each description and reading came from (your own words, Gardiner, Allen, Wikipedia, JSesh, and so on).

What I can say now, to be confirmed against your actual files:

- **Noto Sans Egyptian Hieroglyphs:** I believe this is under the SIL Open Font License 1.1, which allows self-hosting and subsetting. Ship the OFL text with the app and check the copy you download for any Reserved Font Name.
- **Other hieroglyph fonts** (Aegyptus, NewGardiner/JSesh, older free fonts): their terms have differed and in some cases changed between versions. Check the exact version you download, and whether it allows web embedding and subsetting.
- **Unicode data** (UCD names, Unikemet): permissive Unicode License v3. Keep the notice.
- **Gardiner's sign list:** *Egyptian Grammar*, 3rd ed. 1957. Gardiner died in 1963, so in the UK I believe the book stays in copyright until the end of 2033; other countries' terms vary. The underlying facts (codes, readings) aren't protected. Copied text, translations close to his wording, and scans of his sign drawings would be. Checking your list against Gardiner is fine. Copying his descriptions or images into the app is not, unless you have permission from the publisher (Griffith Institute).
- **Sign images** for the SVG fallback need their own clear licence, or have to be drawn by you.

Once you send the font name and the 86-sign file, I'll do the actual check and flag any entries whose wording or sources need attention.

---

## P07

**Prompt:** Annotate this one-word text, given as Gardiner codes: G39 A1. Use the interlinear layout: word id, signs, transliteration, gloss, grammar, grade and notes, then a literal translation and a review list. No dictionary is supplied, so mark every gloss VERIFY.

### Answer A

# Interlinear annotation: G39 A1

| Field | W1 |
|---|---|
| **Word id** | W1 |
| **Signs** | G39 (pintail duck) + A1 (seated man) |
| **Transliteration** | zꜣ (also written *sꜣ*) |
| **Gloss** | "son" **[VERIFY]** |
| **Grammar** | Noun, masculine singular. G39 is the phonogram for *zꜣ*. A1 is a determinative for male persons. |
| **Grade** | B, probable |
| **Notes** | G39 is the standard writing of *zꜣ* "son". It often appears with the stroke Z1, and A1 commonly follows as a person determinative. **Main alternative:** A1 can also write the 1st-person singular suffix pronoun *=i*, which gives *zꜣ=i* "my son" **[VERIFY]**. In that reading A1 is doing two jobs at once, as determinative and as suffix, which is a normal scribal habit. Without more context the bare noun reading is preferred. A less likely reading is the homophone *zꜣ* "back" or "protection", but that word takes different determinatives (F-series or V-series signs), so A1 makes it unlikely. |

## Literal translation

> "son" (alternative: "my son")

## Review list

1. **W1 gloss "son"**: check against a dictionary such as Faulkner's *Concise Dictionary* or the *Wörterbuch*. No dictionary was supplied.
2. **W1 role of A1**: decide whether it is only a determinative ("son") or also the suffix *=i* ("my son"). You need the surrounding context to settle this.
3. **W1 missing Z1**: the usual spelling has a stroke Z1 after G39. Check whether it is really absent from the source or was left out when the text was transcribed.
4. **W1 transliteration convention**: decide between *zꜣ* and *sꜣ* to match your project's style.
5. **W1 homophones**: rule out *zꜣ* "back" and *zꜣ* "protection". The determinative argues against them, but confirm this from the source.

### Answer B

# Annotated text: G39 A1 (one word)

**Source:** sign codes supplied by you. There is no object, photograph or publication, so this is a transcription and not an edition.
**Convention:** standard Egyptological transliteration, with ꜣ for aleph and = before suffix pronouns. G39 has an older reading, zꜣ, which some sign lists use (Gardiner sign list p. 471).
**Draft of:** 2026-10-14. **Status:** draft that needs expert review. No dictionary was supplied, so every gloss is a proposal marked VERIFY.

## Line 1 (grade: C)

| Word | Signs (Gardiner codes) | Transliteration | Gloss | Grammar | Grade | Notes / alternatives |
|---|---|---|---|---|---|---|
| L1.w1 | G39 A1 | sꜣ | "son" (VERIFY) | noun, masc. | C | **G39** (pintail duck) is a biliteral sign for sꜣ and the usual ideogram for sꜣ "son" (Gardiner p. 471). **A1** (seated man) is taken here as a silent determinative for a man (p. 442). **Alternative:** A1 after a noun can also write the 1st person singular suffix pronoun, which gives **sꜣ=j "my son"**. The signs alone cannot decide between the two readings, which is why this is grade C and not B. The ending has no t (X1), so it is not sꜣt "daughter". Other words read sꜣ ("back", "protection", "phyle") are normally written with other signs (for example Aa17 and V17). The man determinative makes them unlikely, but that still needs checking (VERIFY). |

**Literal translation:** "son" (reading A1 as a determinative), or "my son" (reading A1 as the suffix =j).
**Smoother translation:** none. With a single word there is nothing to smooth, and the choice between the two readings depends on the text around it.
**Damage and restorations:** none reported. The codes are taken as given and all signs as fully preserved.

## Review list

- **L1.w1, gloss "son":** VERIFY against a dictionary you trust, such as the Wörterbuch or the Thesaurus Linguae Aegyptiae. Cite the entry and check that the spelling G39 + A1 is attested for sꜣ "son".
- **L1.w1, role of A1 (grade C):** decide between a determinative (sꜣ, "son") and the suffix pronoun (sꜣ=j, "my son"). These would help:
  - the surrounding context, such as a filiation formula or a speech by the father;
  - whether the source writes the man determinative elsewhere;
  - parallels from the same monument or period.
- **L1.w1, homographs:** confirm that no other sꜣ word is written G39 + A1 in your period or genre.
- **Convention:** confirm whether your publication uses sꜣ or the older zꜣ, and which transliteration standard applies.
- **Sign values:** the sign table's entries for G39 and A1 come from OCR text of the Gardiner list. Check them against the page images for pp. 442 and 471.

If you plan to share or publish this, the next step is an `accuracy-review` pass. Publication would also need a facsimile or photograph of the original.

---

## P01

**Prompt:** Review this transliteration and gloss for confident errors: Transliteration: G39 A1 = sꜣ 'son'. I am certain this is right. Source: from memory. Convention: Gardiner-era spelling.. State the convention, trace each claim to a source, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

### Answer A

# Accuracy review: G39 A1 = sꜣ "son"

**Verdict:** The reading is very probably right. I found no critical error. Two things stop it being presentable as certain: it has no source, and its convention label doesn't match its spelling. It's fine for informal use with those two fixes. Don't publish it as is.

## Convention

- **Stated:** "Gardiner-era spelling."
- **Actually written:** `sꜣ` is the current spelling, with s and the ꜣ aleph.
- **Gardiner's form:** Gardiner's sign-list gives the older reading `zꜣ`. The local references cite this at p. 441, in the note on s and z, and at p. 471, under G39.

So the label and the spelling disagree (finding 2). I've reviewed the reading in current transliteration and named the Gardiner form beside it.

## Claims and where each comes from

| # | Claim | Your source | What I traced it to |
|---|---|---|---|
| 1 | G39 (pintail duck) is a biliteral sign for sꜣ | Memory | Local sign table: G39, biliteral, sꜣ, Gardiner p. 471. Status: "checked against OCR text, VERIFY against the page image" |
| 2 | A1 (seated man) is a silent determinative | Not stated | Local sign table: A1, determinative for "man", value null, Gardiner p. 442 |
| 3 | G39 + A1 is one word | Not stated | The determinative ends the word (worked example 1 in the transliteration skill) |
| 4 | It means "son" | Memory | Only the sign-list's own example ("sꜣ 'son'"). No dictionary entry was checked |
| 5 | The convention is "Gardiner-era" | Your label | Contradicted by the spelling (see finding 2) |

**Counts:** 5 claims checked. 0 sourced by you. 2 supported by a sign list read from OCR text only. 1 has no dictionary source. 1 is inconsistent. 0 critical, 2 major, 2 minor, 3 notes.

I worked out the sign layer myself from the sign table, not from your line, and got the same result: G39 is sꜣ, A1 adds no sound, and the transliteration is **sꜣ**.

## Findings

### Major

**1. The only source is your memory.**
- **Evidence:** You give no sign-list, dictionary or text reference. Your certainty isn't evidence, and neither is my agreement.
- **Impact:** Anyone who reuses this line has nothing to check it against. An unsourced claim stays a finding even when it's correct.
- **Fix:** Cite Gardiner's sign-list, G39 (p. 471 per the local table; confirm it on the page image). Cite a dictionary entry for sꜣ "son", from the Wörterbuch or the Thesaurus Linguae Aegyptiae, with the lemma or page you actually looked at. I haven't supplied a dictionary page, because I couldn't check one and won't invent it.

**2. The convention label contradicts the spelling.**
- **Evidence:** "Gardiner-era spelling" points to the older `zꜣ` (Gardiner p. 441, and p. 471 per the local table). You wrote the current `sꜣ`. On top of that, Gardiner's printed aleph and some other letters differ from current fonts, and the OCR copy here garbles them.
- **Impact:** A reader can't tell which system is in use. If a "Gardiner-era" output later mixes `z` and `s` forms, the same word will look like two different words.
- **Fix:** Pick one system:
  - Current letters: `sꜣ "son"`, labelled as such and checked against the 2023 Leiden standard or your publication's house style.
  - Gardiner's: `zꜣ` (from the page image), with the modern `sꜣ` given alongside.

  State the period too (Middle Egyptian assumed).

### Minor

**3. Sign roles aren't stated.**
- **Evidence:** The line doesn't say that G39 is the sound sign and A1 the determinative.
- **Impact:** A reader might take A1 as a sound sign or as the pronoun "I", which is A1's value when used as a word sign.
- **Fix:** Write it as `G39 (biliteral sꜣ) + A1 (det. "man") = sꜣ`.

**4. The reference data itself is unconfirmed.**
- **Evidence:** Both table entries say they were checked against OCR text, with diacritics added from memory. The two local notes also disagree on where Gardiner gives `zꜣ` (p. 441 or p. 471).
- **Impact:** My agreement with your reading is only as good as that table.
- **Fix:** Check G39, A1 and the s/z note against the page images, and record the right page numbers.

### Notes

5. **Is the bird really G39?** In hand copies and hieratic, G39 is easy to confuse with G38 (a goose, read gb) or G40 (the pintail in flight, read pꜣ). If your source is a photograph or a facsimile, confirm the sign before relying on the reading.
6. **Feminine form:** "Daughter" is sꜣt, written with t and a woman determinative. Check that no t is damaged or left out in your source.
7. **Old Egyptian:** If the text is Old Kingdom, the s/z distinction may matter. Then `zꜣ` is the period-correct form, not just Gardiner's spelling.

## What I could not check

- Gardiner's page images. I only had OCR-derived table entries, so neither the diacritics nor the page numbers are confirmed.
- Any dictionary, so the gloss "son" rests on the sign-list example only.
- The source text or a photograph, so I couldn't confirm G39 against G38 or G40, check for damage, or see the context and period.
- The exact letters of the 2023 Leiden standard.

**Needs a specialist or the original:** finding 5 (identifying the sign from the object) and finding 7 (the period).

### Answer B

# Review: G39 A1 = sꜣ "son"

**Verdict:** I found no confident errors. The reading and gloss are standard. What needs work is how you hold the claim: "certain, from memory" isn't a source, and the bare spelling has one real ambiguity.

**How I checked:** I worked from my own knowledge of the standard references. I did not look anything up during this review, so treat my citations as pointers to check, not as verified quotations. Page and section numbers are left out on purpose because I can't confirm them.

## Convention

I'm treating "Gardiner-era spelling" as the system in A. H. Gardiner, *Egyptian Grammar*, 3rd ed. (1957):
- Signs are numbered from his Sign List (G = birds, A = men).
- Transliteration uses aleph ꜣ (U+A723; written `A` in Manuel de Codage).
- Gardiner writes **s** for both the bolt-s (O34) and the folded-cloth-s (S29). He does not use the separate **z** that Old Kingdom specialists and Manuel de Codage use.

## Claims and where they come from

| Claim | Source to check | Status |
|---|---|---|
| G39 is the pintail duck, used as the sound-sign sꜣ | Gardiner, *Egyptian Grammar*, Sign List, entry G39 | Matches my knowledge; not checked against the page |
| sꜣ means "son" | Faulkner, *Concise Dictionary of Middle Egyptian*, entry sꜣ; *Wörterbuch* (Wb) vol. III, entry sꜣ | Matches; not checked |
| A1 (seated man) here is a determinative and is not read | Gardiner, Sign List, entry A1 | Matches; not checked |

## Findings

**Critical:** none.

**Major:** none.

**Minor 1: you haven't ruled out the reading "my son."**
- *Evidence:* A1 does two jobs in Middle Egyptian. It is the "man" determinative, and it also writes the 1st-person suffix =i ("my"). Gardiner notes that one A1 often stands for both at once, so G39 + A1 can be read sꜣ=i, "my son."
- *Impact:* Taken out of context, "= sꜣ" may be missing a pronoun. That changes the translation.
- *Fix:* Write it as "sꜣ 'son' (or sꜣ=i 'my son' if A1 also stands for the suffix)" and decide from the surrounding text.

**Minor 2: the only source given is memory.**
- *Evidence:* You give no reference. Confidence doesn't count as one.
- *Impact:* Nobody can check it, and the "certain" label can hide mistakes elsewhere in your work.
- *Fix:* Cite the Gardiner Sign List entry G39 plus Faulkner or the Wb entry, with page numbers checked against the books.

**Note 1: z vs. s.**
- In Old Kingdom work and in Manuel de Codage the word is **zꜣ** (MdC `zA`). That is the same word in a different convention, not an error. It's only a problem if the gloss ends up mixed with Old Egyptian material.
- *Fix:* State which convention you're using once, at the top.

**Note 2: confusion with G38.**
- Scribes and modern copyists sometimes mix up G39 (pintail, sꜣ) with G38 (goose, gb). Gardiner's sign list mentions this.
- *Fix:* If you're working from an original text or a hand copy rather than a typeset sign list, check the bird's shape.

**Note 3: words that sound the same.**
- Several other words are also read sꜣ: "back" (Aa18), "protection" (V17), and "phyle," a temple work-crew (also written with V17, as far as I remember).
- The duck sign plus the man determinative is what points to "son," so your reading holds. Just don't carry "sꜣ = son" over to other spellings of sꜣ.

**Note 4: the stroke Z1 is often part of the spelling.**
- The word is often written G39 + Z1 + A1. If your source shows a stroke and you left it out, the description of the signs is incomplete, though the reading is unchanged.

## What I could not check

- Any page or section numbers in Gardiner, Faulkner or the Wb.
- The text this spelling comes from. Without it I can't tell sꜣ from sꜣ=i, and I can't check for a G38 mix-up.
- Whether "Gardiner-era" means Gardiner's own system or some other early-20th-century system, such as older Berlin-school spellings.
- The homograph list in Note 3 and the z/s history in Note 1, which come from my memory and weren't looked up.

---

## P04

**Prompt:** What is Gardiner sign G17? Give me the Unicode character and code point, the section, every role it has with its value and Gardiner page, and the status your table gives that row.

### Answer A

**G17: the owl**

| Field | Value |
|---|---|
| Glyph | 𓅓 |
| Code point | U+13153 (EGYPTIAN HIEROGLYPH G017) |
| Section | G, Birds |
| In Gardiner's printed list | Yes |

**Roles in the curated table**

| Role | Value | Gardiner page |
|---|---|---|
| Uniliteral | **m** | p. 469 |

The table has only this one row for G17. It gives no ideogram or determinative use.

**Status given for that row (quoted):**
> "checked against the supplied Gardiner list (OCR text); diacritics and modern spelling from author knowledge, VERIFY against the page image"

So the value *m* and page 469 match an OCR copy of Gardiner's sign list (*Egyptian Grammar*, 3rd ed., 1957), but nobody has checked them against the page image yet. For a plain *m* there are no diacritics for OCR to garble, so the risk is mainly that the page number is wrong. I got the glyph and code point from the Unicode character name, not from memory.

You'll often see the owl on its own as the preposition *m* ("in, with, from"). That is the same *m* sound used as a word, but the table doesn't list it as a separate entry, so treat it as unverified here.

### Answer B

I couldn't find a table to check against. The working directory is empty, there are no project files that mention G17, and I have no saved memory from earlier work. So I can't tell you the status your table gives this row, and I can't confirm page numbers from your source.

Here is what I know about G17 from general knowledge:

- **Sign:** an owl (*Bubo ascalaphus*, the Pharaoh eagle-owl).
- **Unicode:** 𓅓, code point **U+13153** (EGYPTIAN HIEROGLYPH G017).
- **Section:** G, Birds.
- **Roles:**
  - **Phonogram, uniliteral *m*.** This is its main use. For example, it writes the preposition *m* ("in, with, from") and appears in many words with *m*.
  - It is also used as part of composite signs such as G18 (two owls, *mm*) and G20 (owl with forearm, *m* + *ı͗*). Those are separate sign numbers, though, not other roles of G17.
- **Gardiner page:** G17 is in the Birds section of the sign list in *Egyptian Grammar* (3rd ed.), around pp. 467–469. I can't confirm the exact page from memory.
- **Status:** I can't give one because I don't have your table.

If you send me the table (a file path, CSV or pasted rows), I'll give you the exact row, including its roles, page references and status.

---

## P02

**Prompt:** Check the brackets in this line and tell me what is wrong: `htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]`. Then draft the key the line would need.

### Answer A

## The bracket problem

The line opens four brackets but closes only three:

```
htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]
           [         ✓         (         ]
                {  }  ✓        ✗ never closed
```

- `[ … ]` opens and closes correctly.
- `{nb}` opens and closes correctly.
- **`(` is never closed.** The `]` comes while `(` is still open, so the brackets overlap instead of nesting.

There are two ways to fix it, and they mean different things:

| Fix | Meaning |
|---|---|
| `[Wsjr {nb} Ddw (dj=f) prt-xrw]` | Only *dj=f* is added by the editor |
| `[Wsjr {nb} Ddw (dj=f prt-xrw)]` | *dj=f prt-xrw* is all added by the editor |

Only the source text can tell you which one is right.

## Two other things to check

1. **`{nb}` looks wrong.** *nb Ḏdw*, "lord of Busiris," is the standard epithet of Osiris in this formula. Marking *nb* as superfluous would be unusual. If the scribe left it out and you are supplying it, the usual sign is `⟨nb⟩`, not `{nb}`.
2. **Capital letters.** In Manuel de Codage, `h` is ḥ and `H` is ḥ. The formula needs `Htp` (ḥtp). In the same way, `ddw` should be `Ddw` (Ḏdw). Right now the line reads as h-tp and d-dw.

A corrected line, assuming only *dj=f* is supplied and *nb* is an omission:

```
Htp-dj-nsw [Wsjr ⟨nb⟩ Ddw (dj=f) prt-xrw]
```

## Draft key

> **Sigla**
>
> `[ ]` Text lost in a lacuna and restored by the editor.
> `⸢ ⸣` Text partly damaged but still readable.
> `⟨ ⟩` Text the scribe left out by mistake, supplied by the editor.
> `{ }` Text in the original that the editor judges superfluous or wrong. Read it as deleted.
> `( )` Words not written in the original, added by the editor to complete the sense or to write out an abbreviation.
> `…` A lacuna of unknown length that has not been restored.
>
> Brackets nest and must close in reverse order, so `[ ( ) ]` is valid and `[ ( ] )` is not.
>
> Transliteration follows the Manuel de Codage: `H` = ḥ, `x` = ḫ, `X` = ẖ, `S` = š, `T` = ṯ, `D` = ḏ, `A` = ꜣ, `a` = ꜥ, `j` = i̯/ꞽ.

Bracket conventions vary between publications, especially for `( )` and `⟨ ⟩`. If you're following a particular house style (for example Leiden, *Wb.*, or a journal's own guidelines), check these definitions against it.

### Answer B

The line has one structural error and two problems with what the brackets mean.

## What's wrong

**1. The brackets cross. This is the structural error.**
`[` opens before `Wsjr`, then `(` opens before `dj=f`. The `]` at the end closes the square bracket while the round one is still open, and `(` is never closed. The checker reports it as `]` closing `[` from col 12 while `(` from col 27 is still open. Every bracket has to close inside the one around it, so you need `[ … ( … ) … ]` or `[ … ] ( … )`.

**2. The round brackets probably don't belong here.**
In an edition line, `( )` usually marks letters you add to expand an abbreviation, such as `nsw` written short. `dj=f prt-xrw` is not an expansion. If you meant "words added for sense", that use belongs in the translation, not the edition line. If you meant "restored", the `[ ]` already says so. My guess is the `(` is left over from an earlier edit and should be deleted.

**3. `{nb}` contradicts the restoration around it.**
`{ }` means the scribe wrote something you are removing as superfluous. Inside `[ ]`, though, the signs are lost and you are restoring them, so you can't call a scribe's sign wrong if it isn't there to see. Also, *nb* is the expected word: *Wsjr nb Ḏdw*, "Osiris, lord of Djedu (Busiris)", is the standard epithet. If *nb* really is visible and you doubt it, mark it as a doubtful reading (`⸢nb⸣?`) and explain in a note. If it's lost, it is simply part of the restoration.

**Not brackets, but worth checking:**
- If this is Manuel de Codage (MdC) ASCII, the first word should be `Htp` (capital H = ḥ), and the place name should be `Ddw` (D = ḏ). Lowercase `htp` and `ddw` read as different sounds. Use one scheme throughout and name it.
- The whole restoration looks like the offering formula. If it came from familiarity with the formula rather than a cited parallel, it needs a parallel in a note. Without one, leave the gap unrestored.

## Corrected line

Which version is right depends on which signs actually survive, and I can't tell that from here:

- Everything after *nsw* is lost:
  `Htp-dj-nsw [Wsjr nb Ddw dj=f prt-xrw]`
- Only the god's name and epithet are lost:
  `Htp-dj-nsw [Wsjr nb Ddw] dj=f prt-xrw`

Both pass the bracket check once the stray `(` and `{ }` are gone.

## Draft key

If your publication has its own key, use that instead. Otherwise, print something like this above the text, listing only the marks the edition actually uses:

> **Key to sigla**
> `[abc]` lost text restored by the editor; the evidence for each restoration is given in the notes
> `[...]` lost text not restored, extent unknown (if the number of signs was measured on the object or a scaled image, give the count)
> `⸢abc⸣` damaged but legible signs
> `⟨abc⟩` omitted by the scribe, supplied by the editor
> `{abc}` written by the scribe but superfluous, removed by the editor
> `⟦abc⟧` erased in antiquity
> `a(bc)` abbreviation expanded by the editor (edition line only)
> `?` after a sign or word: doubtful reading
> In the translation, *(words)* are added by the translator for sense.
> Transliteration: [name the scheme, e.g. MdC ASCII or the publication's standard].

Two choices in this key are mine and need a decision from you:
- I used round brackets only for expanding abbreviations in the edition line, and only for added words in the translation. That stops one mark having two meanings in the same layer.
- I used the half-bracket style `⸢ ⸣`. Don't also use `⌈ ⌉` anywhere in the same text.

The Egyptological uses of these marks come from general practice. Check them against the house style of the journal or series you're writing for.


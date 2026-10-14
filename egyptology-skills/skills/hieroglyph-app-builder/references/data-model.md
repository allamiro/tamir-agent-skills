# Data model

A minimal relational model. Every table with a reading carries a source and a status.

```mermaid
erDiagram
  SIGN ||--o{ READING : has
  SIGN { string code PK  string section  string unicode_char  string label }
  READING { int id PK  string sign_code FK  string role  string value  string source  string status }
  TEXT ||--o{ LINE : contains
  LINE ||--o{ WORD : contains
  WORD ||--o{ WORD_SIGN : spelled_by
  WORD_SIGN }o--|| SIGN : uses
  WORD { string id PK  string translit  string gloss  string grade  string gloss_source }
  LINE { int n  string direction  string damage_notes }
  TEXT { string id PK  string source  string period  string convention }
```

Notes:

- `READING.role` is one of uniliteral, biliteral, triliteral, ideogram, determinative, marker.
- `READING.status` says how it was checked (verified against which edition and page, or
  `VERIFY`). A reading without a status cannot be saved.
- `WORD_SIGN` keeps order, orientation and any damage flag; it is the link that lets a reader
  re-check the reading.
- `WORD.grade` uses the scale in `text-annotation`.
- One word can map to several candidate spellings during editing; keep the chosen one and the
  rejected ones with reasons.

# Rendering hieroglyphs

- **Characters.** Egyptian hieroglyphs are in the Unicode block U+13000 onward. Gardiner codes map
  to characters by name (`EGYPTIAN HIEROGLYPH D021`); `gardiner-sign-lookup/scripts/signs.py`
  does the mapping.
- **Layout controls.** Current Unicode has joiner and insertion controls for stacking signs into
  quadrats. Whether they render depends on the font and the text engine, so test them. The
  script emits a vertical joiner for `:` and a horizontal joiner for `*`.
- **Fonts.** Choose a font that covers the block, and say which. Provide a fallback that shows the
  Gardiner code in a box when a sign is missing. Check licences of fonts before bundling.
- **Direction.** Rows and columns, left to right or right to left. Store direction per line.
  Browsers do not apply the Egyptian rule that signs face the line start; you must flip or
  choose a layout engine.
- **Publication quality.** Use an existing layout tool for facsimile-style output. Gardiner
  notes that no type font suits every inscription; treat generated text as a transcription.
- **Fallback for readers.** Always show the transliteration beside the glyphs.

Unicode joiner behaviour and font coverage: from author knowledge, VERIFY with the current
Unicode chart and your chosen font.

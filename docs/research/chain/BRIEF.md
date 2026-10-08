# Research brief: flaw -> reasons -> patterns -> detection methods (2026-10-02)

You are a research agent for a hackathon project. This is literature research only: do not write or change any code, do not touch
anything outside your own report folder, do not run the project.

## The project in five lines
"Contrastive Voice" is a Track C entry of a multimodal AI hackathon: contrastive
speech analytics with temporal flaw grounding. A participant reads a known transcript; the recording is compared with a reference
reading of the same words. Both are force-aligned to the transcript (wav2vec 2.0 base CTC, character spikes on a 20 ms grid, word
start/end times, per-word posterior "compatibility"; a greedy CTC decode of the audio is also available). Frame features on a 10 ms
grid: level in dB, Praat autocorrelation F0 in semitones, 13 MFCCs and their deltas. The system flags regions where the participant
departs from the reference, explains each flag, and scores six criteria: pace, pauses, pitch variation, emphasis, volume, clarity.
Constraints set by the owner: as little data as possible, models as light as possible, little or no training (today the detector
is thresholds only), everything must run on a laptop CPU for one 20-40 s clip, and uploads come from a different speaker than the
reference, so any measure must survive speaker and recording differences.

## What is wrong with the research so far
It went one level deep: a judging rubric names a flaw, one paper gives one way to measure it. So each flaw in the product covers a
single acoustic pattern (see the table in your topic section). The owner's instruction for this round, in his words:
- "one flaw might have multiple sub-reasons. Stuttering might have patterns of nervousness or an issue with processing stuff
  properly in brain. Even though both are stutters each one can have different patterns."
- "even though the reason itself is not important, to detect stuttering you need to see the papers of both nervousness and stuttering"
- "you see the patterns in the paper but to detect patterns you need to dive deeper into the other paper. For example processing
  problem tells pattern B but the solution to find and capture pattern B might be in some other paper named differently."

## The chain you must follow, for every flaw in your topic
1. FLAW -> REASONS. List the distinct reasons the literature gives for this flaw in read or prepared speech (public speaking,
   reading aloud, presentations; clinical and second-language literatures count when they describe the same surface flaw).
2. REASON -> PATTERN. For each reason, find the papers of THAT literature and extract the pattern it leaves in the speech signal,
   in that literature's own words: what changes, where in the utterance, how large, how it differs from the patterns of the other
   reasons. Quote the sentence and give numbers where the paper gives them.
3. PATTERN -> METHOD. For each pattern, search separately for how to detect or measure it. The method is often in another field
   under another name (phonetics, speech recognition, clinical voice analysis, language assessment, music/audio signal processing).
   Search by the pattern, not by the flaw. For each method record: the name used in that field, the exact definition or formula,
   parameters and published thresholds or norm values, the data it was validated on and the reported accuracy or effect size,
   whether it needs training data, and what it is confounded by (speaker, sex, recording channel, speaking style, language).
4. FIT TO THIS PROJECT. For each method say whether it can be computed from what the project already has (word and character
   timing, 10 ms level / F0 / MFCC frames, CTC posteriors, greedy decode, the transcript, a reference reading), what would have to
   be added, whether it needs training, and whether it can be judged against the reference reading, against the speaker's own
   baseline, or against a published absolute norm. Also say how a controlled edit of a clean recording could imitate the pattern
   (the project builds its "bad spectrum" by signal processing edits with exact time labels), or that it cannot.

## Rules of evidence (strict)
- Cite only what you actually opened in this session. For every source record: authors, year, title, venue, URL or DOI, and READ
  STATUS = full text / abstract only / secondary (read through another paper, name it) / metadata only. A claim from an abstract is
  marked as such. If you could not open a paper, list it under "could not open" with what you wanted from it; do not cite it.
- Never state a number, threshold or finding from memory as if it came from a source. If you know something from general knowledge
  and could not find a source, put it under "unsourced, to verify" and label it clearly.
- For each claim give the place in the source (section, table, page, or the quoted sentence). Save, for every source you cite, a
  small text file `sources/<short-name>.txt` in your folder holding the URL, the read status and the passages you rely on (verbatim,
  short). These files are how the claims will be checked later.
- Prefer primary papers and review articles over blogs and vendor pages. Do not use Wikipedia as a source.
- Earlier research exists; read it first so you do not redo it and so you know what was already concluded:
  `docs/PAPERS.md` (58 sources, what was taken from each, where the build departs) and the reports under `docs/research/`
  (`features/REPORT.md`, `rubric_explain/REPORT.md`, `alignment/REPORT.md`, `grounding_model/REPORT.md`). Build on them; where you
  disagree with them, say so with the source.
- No praise, no filler, no recommendations beyond what the evidence supports. State uncertainty plainly.

## Output
Write `REPORT.md` in your folder (given in your topic section), at most about 450 lines, with these sections:
1. Summary table: flaw | reason | pattern | best detection method(s) | computable now? | needs training? | evidence strength.
2. One subsection per flaw: reasons; patterns per reason with quotes and numbers; methods per pattern with definitions and numbers.
3. What the current product covers, partly covers, and misses, pattern by pattern.
4. Candidate measures ranked by (a) strength of evidence, (b) feasibility under the project's constraints, with the confounds a
   different-speaker comparison would face, and how each pattern could be imitated by a controlled edit.
5. Open questions and things searched for and not found.
6. References with read status, and the "could not open" and "unsourced, to verify" lists.
Your final message to the lead (it is all the lead sees besides the file) is a summary of at most 30 lines: the reasons and patterns
found per flaw, the top candidate measures, what could not be sourced, and the path of the report.

// The narration script of the launch video (generated file). The timeline uses it only for a scene that
// src/data/narration.json does not have yet; then it estimates each line's length from its word count.
export type ScriptScene = { id: string; lines: string[]; clipAfterLine?: number };

export const SCRIPT: ScriptScene[] = [
  {
    id: "s1_hook",
    lines: [
      "You've rehearsed a speech for days, but the playback sounds wrong, and you can't say why.",
      "Contrastive Voice shows which words drift from a reference reading, by how much, and how to fix them.",
    ],
  },
  {
    id: "s2_what",
    lines: [
      "It aligns your reading and the reference word by word, and compares nine measures of delivery on the same words.",
    ],
  },
  {
    id: "s3_open_example",
    lines: [
      "Here is Reagan's farewell address with delivery slips planted on purpose. It scores 86, and the three costliest fixes come first.",
    ],
  },
  {
    id: "s4_listen", clipAfterLine: 1,
    lines: [
      "Every finding is pinned to its exact seconds and words.",
    ],
  },
  {
    id: "s5_finding", clipAfterLine: 1,
    lines: [
      "These five words took 0.87 seconds. The reference takes 1.62.",
      "The fix is concrete: about 1.6 seconds, stretching the stressed words, not the gaps.",
    ],
  },
  {
    id: "s6_hear_fixed", clipAfterLine: 1,
    lines: [
      "Hear it fixed edits your own recording toward the reference, then analyses it again.",
      "It's still flagged, but partly changed: plus 3.07 points, and the page says so.",
    ],
  },
  {
    id: "s7_melody", clipAfterLine: 1,
    lines: [
      "If your pitch is too flat to stretch, borrow the reference's melody: your voice, its intonation, no longer flagged.",
    ],
  },
  {
    id: "s8_fix_all",
    lines: [
      "Or fix everything at once: 86 becomes 96, with what each fix did.",
    ],
  },
  {
    id: "s9_text_lists",
    lines: [
      "From the transcript to each chart, every flag traces back to the measurement that triggered it.",
    ],
  },
  {
    id: "s10_fair",
    lines: [
      "It doesn't invent problems: an untouched copy scores 100. With five reference readers, you're compared with their word-by-word median.",
    ],
  },
  {
    id: "s11_upload",
    lines: [
      "For your own speech, upload the recordings and the transcript. If the text doesn't match the audio, it tells you where.",
    ],
  },
  {
    id: "s12_no_reference",
    lines: [
      "Without a reference, it grades the reading against itself, as a rough check.",
    ],
  },
  {
    id: "s13_how",
    lines: [
      "A wav2vec 2.0 aligner times every word. Pitch and volume are measured against each speaker's own voice. And only differences past thresholds fitted on flawless comparisons are flagged.",
    ],
  },
  {
    id: "s14_evidence",
    lines: [
      "We stress-tested it on 2,410 files: nine public-domain speeches, 448 copies with edits of known type, place and size, and 1,953 readings by other people.",
      "On unseen speakers, F1 is 0.812, as pre-registered. Undoing an edit removes its flag in 22 of 22 repairs, while a placebo keeps it.",
      "Unedited copies get zero false flags. A different reader gets about one every two minutes.",
    ],
  },
  {
    id: "s15_open",
    lines: [
      "It runs in Docker. The detector is on Hugging Face, and the code and report are on GitHub.",
    ],
  },
  {
    id: "s16_close",
    lines: [
      "Contrastive Voice. Fix the exact words.",
    ],
  },
];

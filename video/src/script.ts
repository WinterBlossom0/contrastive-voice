// The narration script of build/work/video_v2/script.json. The timeline uses it only for a scene that
// src/data/narration.json does not have yet; then it estimates each line's length from its word count.
export type ScriptScene = { id: string; lines: string[]; clipAfterLine?: number };

export const SCRIPT: ScriptScene[] = [
  {
    id: "s1_hook",
    lines: [
      "You've practised a speech for days.",
      "You record it, play it back... and something feels off.",
      "Too fast? A pause in the wrong place? Fading at the end?",
      "Contrastive Voice shows you exactly which words, and how to fix them.",
    ],
  },
  {
    id: "s2_what",
    lines: [
      "Give it your reading, and a reference reading of the same text: your best take, a coach, or a speaker you admire.",
      "It lines the two up word by word, and marks every place where your delivery drifts.",
    ],
  },
  {
    id: "s3_open_example",
    lines: [
      "Let's try it with an example from the gallery.",
      "This is Ronald Reagan's farewell address, with four delivery slips added on purpose.",
      "It scores 86 out of 100: rushed in the middle, then fading. And the three biggest fixes come first.",
    ],
  },
  {
    id: "s4_listen", clipAfterLine: 1,
    lines: [
      "Press play, and watch the sky. The clouds are drawn from the voice, and they rise and glow as it speaks.",
      "Below, each finding is a tinted stretch of the waveform, with its bar on the strip. A brighter bar costs more.",
    ],
  },
  {
    id: "s5_finding", clipAfterLine: 3,
    lines: [
      "Click a finding to open it.",
      "These five words took 0.87 seconds. The reference takes 1.62.",
      "Listen: yours first, then the reference.",
      "The fix: give these words about 1.6 seconds, and stretch the stressed words, not the gaps.",
    ],
  },
  {
    id: "s6_hear_fixed", clipAfterLine: 2,
    lines: [
      "Hard to imagine? Press Hear it fixed.",
      "It edits your own recording toward the reference, then checks the result again.",
      "Here it's partly fixed, and the score rises by 3.07. It says so plainly, because it's a preview, not a promise.",
    ],
  },
  {
    id: "s7_melody", clipAfterLine: 2,
    lines: [
      "Sometimes your pitch is too flat to widen without sounding processed.",
      "Then try the reference's melody: it gives your own voice the reference's intonation on those words.",
      "Same voice, the reference's tune, and the spot is no longer flagged.",
    ],
  },
  {
    id: "s8_fix_all",
    lines: [
      "Or fix everything at once: 86 becomes 96.",
      "And the list tells you what each fix did.",
    ],
  },
  {
    id: "s9_text_lists",
    lines: [
      "Every finding is pinned to the words of your transcript: dotted, dashed or solid as it gets more serious. Click any word to hear it.",
      "Want more? Open every finding, filter by pattern, or zoom into every measurement.",
    ],
  },
  {
    id: "s10_fair",
    lines: [
      "It's careful about what it flags. An untouched copy scores 100, with nothing flagged.",
      "And with five reference readers, it compares you with their word-by-word median, so no single reader's habits count against you.",
    ],
  },
  {
    id: "s11_upload",
    lines: [
      "Now your own speech. Upload your reading, choose a reference, and paste the transcript.",
      "If the transcript doesn't match what was said, it tells you where, instead of guessing.",
      "With the right text, the analysis runs step by step, in seconds.",
    ],
  },
  {
    id: "s12_no_reference",
    lines: [
      "No reference at all? It compares the reading with itself, and shows the spots that stand out.",
      "It's a rough check. A reference reading gives better results.",
    ],
  },
  {
    id: "s13_how",
    lines: [
      "Under the hood, forced alignment times every word in both recordings.",
      "Nine measures of pace, pauses, pitch, emphasis, volume and clarity are compared on the same words.",
      "Volume and pitch are relative to your own voice, so a deep voice is never a flaw.",
      "And only a difference past a threshold, fitted on flawless comparisons, gets flagged.",
    ],
  },
  {
    id: "s14_evidence",
    lines: [
      "We tested it on 2,410 audio files from nine public-domain speeches, with edits of known type, place and size.",
      "On speakers it never saw, F1 is 0.812 as pre-registered, and 0.879 with one detection per edit.",
      "And zero false flags in 5.89 minutes of unedited and placebo copies.",
    ],
  },
  {
    id: "s15_open",
    lines: [
      "Run it yourself with Docker: build it, run it, and open the page in your browser.",
      "The detector is on Hugging Face, the code is on GitHub, and the technical report explains every number.",
    ],
  },
  {
    id: "s16_close",
    lines: [
      "Record. Compare. Fix the exact words.",
      "Contrastive Voice.",
    ],
  },
];

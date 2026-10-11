import { staticFile } from "remotion";

// The level of the narration, so that the music and the sound effects follow whatever voice narration.json names.
// Measure: mean power of the 100 ms blocks above -60 dBFS and within 10 dB of their mean (MusicBed.tsx MUSIC.activeDb
// is the same measure of the music). It is close to integrated loudness for speech, without the K-weighting.
const BLOCK_SEC = 0.1;
const ABSOLUTE_GATE = 1e-6;
const RELATIVE_GATE = 0.1;
// The level that the mix assumes before the narration exists.
export const DEFAULT_VOICE_DB = -20;

type Wav = { rate: number; channels: number; read: (frame: number, channel: number) => number; frames: number };

// RIFF WAVE with 16-bit, 24-bit or 32-bit integer PCM or 32-bit float samples; null for anything else.
const parseWav = (buffer: ArrayBuffer): Wav | null => {
  const view = new DataView(buffer);
  if (buffer.byteLength < 12 || view.getUint32(0, false) !== 0x52494646 || view.getUint32(8, false) !== 0x57415645) {
    return null;
  }
  let offset = 12;
  let format = 0;
  let channels = 0;
  let rate = 0;
  let bits = 0;
  while (offset + 8 <= buffer.byteLength) {
    const id = view.getUint32(offset, false);
    const size = view.getUint32(offset + 4, true);
    const body = offset + 8;
    if (id === 0x666d7420) {
      format = view.getUint16(body, true);
      channels = view.getUint16(body + 2, true);
      rate = view.getUint32(body + 4, true);
      bits = view.getUint16(body + 14, true);
      // WAVE_FORMAT_EXTENSIBLE keeps the real format in the first two bytes of its sub-format GUID.
      if (format === 0xfffe && size >= 26) {
        format = view.getUint16(body + 24, true);
      }
    }
    if (id === 0x64617461 && channels > 0) {
      const bytes = bits / 8;
      const frames = Math.floor(Math.min(size, buffer.byteLength - body) / (bytes * channels));
      const at = (frame: number, channel: number) => body + (frame * channels + channel) * bytes;
      if (format === 3 && bits === 32) {
        return { rate, channels, frames, read: (frame, channel) => view.getFloat32(at(frame, channel), true) };
      }
      if (format === 1 && bits === 16) {
        return { rate, channels, frames, read: (frame, channel) => view.getInt16(at(frame, channel), true) / 32768 };
      }
      if (format === 1 && bits === 24) {
        return {
          rate,
          channels,
          frames,
          read: (frame, channel) => {
            const index = at(frame, channel);
            const value = view.getUint8(index) | (view.getUint8(index + 1) << 8) | (view.getInt8(index + 2) << 16);
            return value / 8388608;
          },
        };
      }
      if (format === 1 && bits === 32) {
        return { rate, channels, frames, read: (frame, channel) => view.getInt32(at(frame, channel), true) / 2147483648 };
      }
      return null;
    }
    offset = body + size + (size % 2);
  }
  return null;
};

const blockPowers = (wav: Wav): number[] => {
  const block = Math.max(1, Math.round(wav.rate * BLOCK_SEC));
  const powers: number[] = [];
  for (let start = 0; start + block <= wav.frames; start += block) {
    let sum = 0;
    for (let frame = start; frame < start + block; frame += 1) {
      let mono = 0;
      for (let channel = 0; channel < wav.channels; channel += 1) {
        mono += wav.read(frame, channel);
      }
      mono /= wav.channels;
      sum += mono * mono;
    }
    powers.push(sum / block);
  }
  return powers;
};

export const voiceLevelDb = async (files: string[], signal?: AbortSignal): Promise<number> => {
  const powers: number[] = [];
  for (const file of files) {
    try {
      const response = await fetch(staticFile(file), { signal });
      const wav = response.ok ? parseWav(await response.arrayBuffer()) : null;
      if (wav !== null) {
        powers.push(...blockPowers(wav).filter((power) => power > ABSOLUTE_GATE));
      }
    } catch {
      // An unreadable file leaves the level to the other files.
    }
  }
  if (powers.length === 0) {
    return DEFAULT_VOICE_DB;
  }
  const mean = powers.reduce((sum, power) => sum + power, 0) / powers.length;
  const kept = powers.filter((power) => power > mean * RELATIVE_GATE);
  return 10 * Math.log10(kept.reduce((sum, power) => sum + power, 0) / kept.length);
};

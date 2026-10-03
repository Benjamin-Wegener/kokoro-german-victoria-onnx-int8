# Kokoro German Victoria (ONNX, int8)

**Download:** `model.int8.onnx` and `voices.bin` are attached to the [latest release](../../releases/latest) and also hosted at [Hugging Face](https://huggingface.co/Benjamin-Wegener/kokoro-german-victoria-onnx-int8) (SHA-256 of `model.int8.onnx`: `19fb607aaa7ee9ce4bc3b708c9c4c3defa24786211e3d58bc4d2ad922b3890dd`).

ONNX export of [kikiri-tts/kikiri-german-victoria](https://huggingface.co/kikiri-tts/kikiri-german-victoria),
a German single-speaker, Kokoro-compatible (StyleTTS2) text-to-speech model, for on-device inference with
[sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx). Built for the offline SISA-Collector Android app.

| File | Size | Description |
|---|---|---|
| `model.int8.onnx` | ~114 MB (GitHub Release asset / Hugging Face) | Model, dynamic int8 weight quantization (fp32 export is ~325 MB) |
| `voices.bin` | 522 KB | Victoria voicepack, float32 `[510, 256]` (style row is chosen by token count) |
| `tokens.txt` | <1 KB | Kokoro phoneme vocabulary (`symbol id`) |
| `export_onnx.py` | | Reproduces the export from the original `.pth` |

Model I/O: `tokens` int64 `[1, N]`, `style` float32 `[1, 256]`, `speed` float32 `[1]` -> `audio` float32, 24 kHz.

## Usage (sherpa-onnx)

Kokoro config: `model=model.int8.onnx`, `voices=voices.bin`, `tokens=tokens.txt`,
`dataDir=<espeak-ng-data>`, `lang=de`. The ONNX file already carries the metadata sherpa-onnx needs
(`model_type=kokoro`, `version=2`, `sample_rate=24000`, ...); tested with sherpa-onnx 1.13.8 (desktop and Android).

## Notes and limitations

- Synthetic voice: label the output as AI-generated where required (e.g. EU AI Act Art. 50).
- Runs at roughly real-time speed on a Pixel-class phone CPU (about 1 s of compute per 1 s of audio, 4 threads).
- A formal listening test comparing int8 with fp32 was not done.
- The phoneme `ʏ` (short ü) is not in the Kokoro vocabulary. Map it to `y` before tokenizing.
- Weights are slightly different from the fp32 export because of quantization.

## License and credits

Apache-2.0, same as the upstream model. See `LICENSE` and `NOTICE`. Credits: kikiri-tts (model), hexgrad (Kokoro-82M).

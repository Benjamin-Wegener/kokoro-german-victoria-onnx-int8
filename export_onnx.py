"""Export kikiri-german-victoria (Kokoro-compatible) to ONNX for sherpa-onnx.

Needs: torch, onnx, loguru, transformers, misaki, num2words, and the
semidark/kokoro fork on PYTHONPATH. Inputs: tokens (int64 [1,N]),
style (float32 [1,256]), speed (float32 [1]); output: audio (float32).
"""
import torch
from kokoro.model import KModel, KModelForONNX

km = KModel(repo_id="kikiri-tts/kikiri-german-victoria", config="config.json",  # hexgrad/Kokoro-82M config.json
            model="kikiri_german_victoria_ep10.pth", disable_complex=True).eval()


class Wrapper(torch.nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = KModelForONNX(m)

    def forward(self, tokens, style, speed):
        audio, _ = self.m(tokens, style, speed[0])
        return audio.reshape(-1)


tokens = torch.LongTensor([[0, 50, 83, 54, 156, 57, 135, 16, 0]])
voice = torch.load("voices/victoria.pt", map_location="cpu", weights_only=True)  # [510,1,256]
style = voice[tokens.shape[1] - 1].reshape(1, -1)
torch.onnx.export(Wrapper(km).eval(), (tokens, style, torch.tensor([1.0])), "model.onnx",
                  input_names=["tokens", "style", "speed"], output_names=["audio"],
                  dynamic_axes={"tokens": {1: "n"}, "audio": {0: "len"}}, opset_version=17, dynamo=False)
voice.numpy().reshape(510, 256).astype("float32").tofile("voices.bin")
# int8: onnxruntime.quantization.quantize_dynamic("model.onnx", "model.int8.onnx", weight_type=QuantType.QUInt8)

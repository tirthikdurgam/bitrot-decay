## BitRot: Digital Entropy Library

![PyPI - Version](https://img.shields.io/pypi/v/bitrot-decay?style=flat-square&color=00ff41)
![PyPI - License](https://img.shields.io/pypi/l/bitrot-decay?style=flat-square&color=white)
![Python](https://img.shields.io/badge/python-3.7+-blue?style=flat-square&logo=python&logoColor=white)
![Downloads](https://img.shields.io/pypi/dm/bitrot-decay?style=flat-square&color=gray)

**BitRot** is a lightweight, zero-dependency Python library designed to simulate **digital decay**. It intentionally degrades images using bit-crushing, grain injection, and glitch artifacts to simulate file corruption, data rot, and transmission errors.

Unlike standard filters that just add noise, BitRot treats the image as a dying signal, applying structural damage that mimics "bad sectors" and "bit loss" over time.

### Use Cases
* **Generative Art:** Create glitch art or "haunted" digital artifacts.
* **Game Development:** Simulate damaged data logs, corrupted HUDs, or dying transmissions.
* **Data Science:** Test machine learning model robustness against noisy or corrupted inputs (adversarial testing).
* **Archival Simulation:** Visualize the theoretical degradation of digital media over time.

---

## Installation

Install easily via pip:

```bash
pip install bitrot-decay

```

## Quick Start

### 1. File-to-File (CLI Style)

The simplest method. Takes an input file, applies decay based on an integrity score, and saves the result.

```python
import bitrot

# integrity: float between 1.0 (Perfect) and 0.0 (Destroyed)
bitrot.decay_file(
    input_path="assets/photo.jpg",
    output_path="assets/photo_rotted.jpg",
    integrity=0.4
)

```

### 2. Memory-to-Memory (API Style)

Ideal for web servers (FastAPI/Flask) or real-time processing where you don't want to save files to disk. Accepts raw bytes and returns raw bytes.

```python
import bitrot

# 1. Load image as bytes
with open("source.jpg", "rb") as f:
    raw_data = f.read()

# 2. Rot the bytes directly
# Returns the raw bytes of the decayed JPEG
corrupted_data = bitrot.decay_bytes(raw_data, integrity=0.15)

# 3. Use the bytes (e.g., send to frontend, save to DB, etc.)
with open("output.jpg", "wb") as f:
    f.write(corrupted_data)

```

---

## Features & Mechanics

| Feature | Description | Trigger Condition |
| --- | --- | --- |
| **Grain Injection** | Simulates sensor noise and film grain. | Active at all decay levels (< 1.0). |
| **Bit Glitching** | Randomly shifts pixel blocks to mimic data loss. | Triggers when integrity drops below **0.5**. |
| **Chroma Decay** | Desaturates colors to simulate fading memory. | Triggers when integrity drops below **0.8**. |
| **Safe Clamping** | Ensures pixel values stay within valid ranges. | Always Active. |

---

## Contributing

This project is open source and we welcome contributions!

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

```

```

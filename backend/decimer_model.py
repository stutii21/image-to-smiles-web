from PIL import Image
import io
import tempfile
import os

# Global lazy-loaded function
_predict_fn = None


def image_to_smiles(image_bytes: bytes) -> str | None:
    global _predict_fn

    # 🔹 Import DECIMER lazily (VERY IMPORTANT)
    if _predict_fn is None:
        from DECIMER import predict_SMILES
        _predict_fn = predict_SMILES

    # Thread-safe temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image.save(tmp.name)
        tmp_path = tmp.name

    try:
        smiles = _predict_fn(tmp_path)
        return smiles
    finally:
        os.remove(tmp_path)



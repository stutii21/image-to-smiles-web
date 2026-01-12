from DECIMER import predict_SMILES
from PIL import Image
import io
import tempfile
import threading

# Ensure model loads only once
_model_lock = threading.Lock()
_model_loaded = False

def _load_model_once():
    global _model_loaded
    if not _model_loaded:
        # Dummy call to trigger model download/load
        predict_SMILES("dummy")
        _model_loaded = True

def image_to_smiles(image_bytes: bytes):
    global _model_loaded

    # Lazy model loading (does NOT block server startup)
    if not _model_loaded:
        with _model_lock:
            if not _model_loaded:
                _load_model_once()

    image = Image.open(io.BytesIO(image_bytes))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
        image.save(tmp.name)
        smiles = predict_SMILES(tmp.name)

    return smiles



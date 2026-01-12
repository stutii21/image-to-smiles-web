from DECIMER import predict_SMILES
from PIL import Image
import io
import tempfile
import threading

# Thread lock to avoid race conditions
_model_lock = threading.Lock()

def image_to_smiles(image_bytes: bytes) -> str:
    """
    Converts image bytes to SMILES using DECIMER.
    Model is loaded lazily on first real inference.
    """

    # Open image safely
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Use a thread-safe temporary file
    with _model_lock:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
            image.save(tmp.name)
            smiles = predict_SMILES(tmp.name)

    return smiles



from DECIMER import predict_SMILES
from PIL import Image
import io
import tempfile

def image_to_smiles(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        image.save(tmp.name)
        smiles = predict_SMILES(tmp.name)

    return smiles



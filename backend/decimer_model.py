from DECIMER import predict_SMILES
from PIL import Image
import io

def image_to_smiles(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_path = "temp.png"
    image.save(image_path)

    smiles = predict_SMILES(image_path)
    return smiles

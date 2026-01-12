from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from decimer_model import image_to_smiles
from rdkit_utils import smiles_to_2d_svg, smiles_to_3d_block

app = FastAPI(title="Image to SMILES API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Image to SMILES backend running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()

    smiles = image_to_smiles(image_bytes)
    if not smiles:
        return {"error": "SMILES prediction failed"}

    return {
        "smiles": smiles,
        "structure_2d_svg": smiles_to_2d_svg(smiles),
        "structure_3d": smiles_to_3d_block(smiles),
    }


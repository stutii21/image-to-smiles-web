from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from decimer_model import image_to_smiles
from rdkit_utils import smiles_to_2d_svg, smiles_to_3d_block

# Create FastAPI app
app = FastAPI(title="Image to SMILES API")

# Enable CORS (ONLY ONCE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (prevents 404 on deployment)
@app.get("/")
def read_root():
    return {"message": "Backend is running successfully"}

# Prediction route
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()

    smiles = image_to_smiles(image_bytes)
    if not smiles:
        return {"error": "SMILES prediction failed"}

    svg_2d = smiles_to_2d_svg(smiles)
    mol_3d = smiles_to_3d_block(smiles)

    return {
        "smiles": smiles,
        "structure_2d_svg": svg_2d,
        "structure_3d": mol_3d
    }

"""
@Project :GOT-OCR2.0
@File    :server.py
@IDE     :PyCharm
@Date    :2024/9/29 18:30
@desc    :
"""

import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import os
import uuid
from modelscope import AutoModel, AutoTokenizer  # modelscope

# from transformers import AutoModel,AutoTokenizer #transfomers
from PIL import Image
import io
from loguru import logger


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
app = FastAPI()


class GOTRequest(BaseModel):
    mode: str
    fine_grained_mode: str = ""
    ocr_color: str = ""
    ocr_box: str = ""


tokenizer = AutoTokenizer.from_pretrained(
    "stepfun-ai/GOT-OCR2_0", trust_remote_code=True
)
model = AutoModel.from_pretrained(
    "stepfun-ai/GOT-OCR2_0",
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    device_map="cuda",
    use_safetensors=True,
)
model = model.eval().cuda()

UPLOAD_FOLDER = "./uploads"
RESULTS_FOLDER = "./results"

for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


@app.post(
    "/run_ocr", description="Upload an image and process it with the selected OCR mode."
)
async def create_upload_file(
    file: UploadFile = File(...),
    mode: str = Form(...),
    fine_grained_mode: str = Form(""),
    ocr_color: str = Form(""),
    ocr_box: str = Form(""),
):
    logger.debug(f"Mode: {mode}")
    logger.debug(f"Fine Grained Mode: {fine_grained_mode}")
    logger.debug(f"OCR Color: {ocr_color}")
    logger.debug(f"OCR Box: {ocr_box}")
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    logger.debug(image)
    unique_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.png")
    logger.debug(image_path)
    image.save(image_path, format="PNG")
    try:
        res = run_GOT(image_path, mode, fine_grained_mode, ocr_color, ocr_box)
        return JSONResponse(content={"result": res})
    except AttributeError:
        logger.error("Invalid request data format")
        return JSONResponse(
            content={"error": "Invalid request data format"}, status_code=400
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)


def run_GOT(image_path, mode, fine_grained_mode, ocr_color, ocr_box):

    logger.debug(image_path)
    logger.debug(mode)
    """
    Runs the OCR processing on the given image path using the specified mode.

    Parameters:
    - image_path (str): The path to the image file.
    - mode (str): The OCR mode to use.
    - fine_grained_mode (str): Fine-grained OCR mode.
    - ocr_color (str): Color to be used for fine-grained OCR.
    - ocr_box (str): Box coordinates for fine-grained OCR.

    Returns:
    - tuple: A tuple containing the OCR result and optional HTML rendering.
    """
    unique_id = str(uuid.uuid4())
    result_path = os.path.join(RESULTS_FOLDER, f"{unique_id}.html")

    try:
        if mode == "plain texts OCR":
            res = model.chat(tokenizer, image_path, ocr_type="ocr")
            return res, None
        elif mode == "format texts OCR":
            res = model.chat(
                tokenizer,
                image_path,
                ocr_type="format",
                render=True,
                save_render_file=result_path,
            )
        elif mode == "plain multi-crop OCR":
            res = model.chat_crop(tokenizer, image_path, ocr_type="ocr")
            return res, None
        elif mode == "format multi-crop OCR":
            res = model.chat_crop(
                tokenizer,
                image_path,
                ocr_type="format",
                render=True,
                save_render_file=result_path,
            )
        elif mode == "plain fine-grained OCR":
            res = model.chat(
                tokenizer,
                image_path,
                ocr_type="ocr",
                ocr_box=ocr_box,
                ocr_color=ocr_color,
            )
            return res, None
        elif mode == "format fine-grained OCR":
            res = model.chat(
                tokenizer,
                image_path,
                ocr_type="format",
                ocr_box=ocr_box,
                ocr_color=ocr_color,
                render=True,
                save_render_file=result_path,
            )
        return res
    except Exception as e:
        return f"Error: {str(e)}", None
    finally:
        if os.path.exists(result_path):
            os.remove(result_path)

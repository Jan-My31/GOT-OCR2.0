"""
@Project :GOT-OCR2.0
@File    :start_app.py
@IDE     :PyCharm
@Date    :2024/9/29 18:31
@desc    :
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.server:app", host="0.0.0.0", port=8130, reload=True)

"""
@Project :GOT-OCR2.0
@File    :client.py
@IDE     :PyCharm
@Date    :2024/9/29 18:31
@desc    :
"""

import requests
import json
from PIL import Image
import io


def read_image(image_path):
    """从给定路径读取图像并返回其字节形式"""
    with Image.open(image_path) as img:
        byte_arr = io.BytesIO()
        img.save(byte_arr, format="PNG")
        return byte_arr.getvalue()


def send_ocr_request(image_bytes, request_data, url):
    """向指定URL发送带有图像的OCR请求并返回响应"""
    files = [("file", ("image.png", image_bytes, "image/png"))]
    response = requests.request("POST", url=url, data=request_data, files=files)
    return response


def parse_response(response):
    """解析响应并打印结果"""
    if response.status_code == 200:
        response_data = response.json()
        print(json.dumps(response_data, indent=4))
    else:
        print(f"Error: {response.status_code}, {response.text}")


def main():
    """主函数，用于执行整个流程"""
    image_path = "/data/GOT-OCR2.0/GOT-OCR-2.0-master/output_image.jpg" #配置图片路径
    request_data = {
        "mode": "format texts OCR",  # 选择模式
        "fine_grained_mode": "",  # 细粒度模式
        "ocr_color": "",  # 颜色
        "ocr_box": "",  # 方框坐标
    }
    url = "http://127.0.0.1:8130/run_ocr"  # 根据自己修改

    image_bytes = read_image(image_path)
    response = send_ocr_request(image_bytes, request_data, url)
    parse_response(response)


if __name__ == "__main__":
    main()

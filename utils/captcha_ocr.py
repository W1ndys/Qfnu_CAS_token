import ddddocr


class CaptchaOCR:
    """验证码识别类，封装ddddocr的功能"""

    def __init__(self):
        """初始化OCR对象"""
        self.ocr = ddddocr.DdddOcr(show_ad=False)

    def recognize(self, cap_pic_bytes):
        """识别验证码

        Args:
            cap_pic_bytes: 验证码图片的字节数据

        Returns:
            str: 识别结果文本
        """
        try:
            res = self.ocr.classification(cap_pic_bytes)
            return res
        except Exception as e:
            print(f"验证码识别失败: {str(e)}")
            return ""


if __name__ == "__main__":
    # 测试代码
    ocr = CaptchaOCR()
    print(ocr.recognize("123"))

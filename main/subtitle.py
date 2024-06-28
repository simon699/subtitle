from PIL import Image, ImageDraw, ImageFont
import requests
import os
from urllib.parse import urlparse
from io import BytesIO


def ImageGetText(textArr, inputImage, textFont):
    # 根据传入的 inputImage 是文件还是 URL 进行分别处理
    parsed = urlparse(inputImage)

    if parsed.scheme and parsed.netlog:
        response = requests.get(inputImage)

        if response.status_code == 200:
            image_byte = BytesIO(response.content)
            img1 = Image.open(image_byte).convert("RGBA")
            width1, height1 = img1.size

            img3 = Image.open(image_byte)
    elif os.path.isfile(inputImage):
        img1 = Image.open(inputImage).convert("RGBA")
        width1, height1 = img1.size

        img3 = Image.open(inputImage)

    # 根据 box 位置，裁切图片后，设置为 img2
    box = (0, height1 - height1 / 10, width1, height1)
    img2 = img1.crop(box).convert("RGBA")
    width2, height2 = img2.size

    if len(textArr) > 0:
        new_img = Image.new('RGB', (max(width1, width2), height1 + height2 * (len(textArr) - 1)))
    else:
        new_img = Image.new('RGB', (width1, height1))

    for i in range(len(textArr)):

        if i == 0:
            # 设置文字的字体和大小
            try:
                font = ImageFont.truetype(textFont, min(width1 / 13, 50))
                font = ImageFont.truetype(textFont, width1 / 20)
            except IOError:
                # 如果指定的字体文件未找到，使用默认字体
                font = ImageFont.load_default()


            # 创建一个与原图像相同尺寸的透明图层
            txt_layer = Image.new("RGBA", img2.size, (255, 255, 255, 0))
            bg_draw = ImageDraw.Draw(txt_layer)

            # 在指定位置添加文字
            text = textArr[0]
            bbox = bg_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_heigt = bbox[3] - bbox[1]

            # 在透明图层上绘制半透明黑色背景
            bg_draw.rectangle((0,0,width2,height2), fill=(0, 0, 0, 128))  # 半透明黑色背景 (R, G, B, A)
            # 在透明图层上绘制文字
            # bg_draw.text(((width1 - text_width) / 2, height1 - text_heigt - 30), text, font=font, fill=(255, 255, 255))
            bg_draw.text(((width2 - text_width) / 2, (height2 - text_heigt) / 2), text, font=font, fill=(255, 255, 255))

            # 将文字图层叠加到原始图像上
            combined = Image.alpha_composite(img2, txt_layer)
            new_img.paste(img1, (0,0))
            # 将img1粘贴到新图像中
            new_img.paste(combined, (0, height1-height2))

        elif i > 0:

            # 根据 box 位置，裁切图片后，设置为 img2
            box = (0, height1 - height1 / 10, width1, height1)
            img2 = img3.crop(box).convert("RGBA")

            # 创建一个与原图像相同尺寸的透明图层
            txt_layer = Image.new("RGBA", img2.size, (255, 255, 255, 0))
            bg_draw = ImageDraw.Draw(txt_layer)


            # 设置文字的字体和大小
            try:
                font = ImageFont.truetype(textFont, min(width1 / 13, 50))
                font = ImageFont.truetype(textFont, width1 / 20)
            except IOError:
                # 如果指定的字体文件未找到，使用默认字体
                font = ImageFont.load_default()

            # 在指定位置添加文字
            text = textArr[i]
            bbox = bg_draw.textbbox((0,0), text, font=font)
            text_width = bbox[2] - bbox[0]

            # 在透明图层上绘制半透明黑色背景
            bg_draw.rectangle((0, 0,width2,height2), fill=(0, 0, 0, 128))  # 半透明黑色背景 (R, G, B, A)
            # 在透明图层上绘制文字
            bg_draw.text(((width1 - text_width) / 2, (height2-text_heigt)/2), text, font=font, fill=(255, 255, 255))

            # 将文字图层叠加到原始图像上
            combined = Image.alpha_composite(img2, txt_layer)

            new_img.paste(combined, (0, (height1 + (i - 1) * height2)))

    return new_img


def add_watermark(inputImage, font_path, text):
    with inputImage as base:

        # 创建一个透明的同大小图片用来绘制文本
        txt = base.convert("RGBA")

        # 创建一个与原始图像大小相同的黑色半透明图像
        txt = Image.new("RGBA", base.size, (0, 0, 0, 128))  # (0, 0, 0, 128) 表示黑色半透明

        # 设置字体和尺寸
        font = ImageFont.truetype(font_path, 50)

        # 设置字体和尺寸
        draw = ImageDraw.Draw(txt)

        # 获取文本尺寸
        width, height = base.size

        # 使用循环来添加水印
        # 计算水印位置
        offset = (200, 200)
        start_pos = (50, 50)
        for x in range(start_pos[0], width, offset[0]):
            for y in range(start_pos[1], height, offset[1]):
                # 渲染文本到单独图片（透明背景）
                temp_img = Image.new('RGBA', (400, 100), (255, 255, 255, 0))
                draw_temp = ImageDraw.Draw(temp_img)
                draw_temp.text((0, 0), text, font=font, fill=(255, 255, 255, 70))

                # 旋转文本图片
                rotated = temp_img.rotate(45, expand=1)
                # 获取文本图片的尺寸
                rotated_width, rotated_height = rotated.size

                # 确定绘制位置
                position = (x - rotated_width // 2, y - rotated_height // 2)

                # 将旋转后的水印贴到背景图层上
                txt.paste(rotated, position, rotated)

                # 合并图片和文字
                watermarked = Image.alpha_composite(base.convert('RGBA'), txt)

    # 保存带有水印的图片
    return watermarked
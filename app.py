from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime, timedelta, timezone

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/pass")
def pass_word():
    # 打开原始图片
    image = Image.open("./Picture1.png")

    # 在这里添加图片修改操作，例如：
    # 调整大小
    # image = image.resize((300, 300))
    # 或转换为灰度图
    # image = image.convert('L')
    # 或添加滤镜等

    # 将修改后的图片保存到内存中
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


def modify_image_date(
    image,
    draw,
    init_x_rate=0.24,
    init_y_rate=0.447,
    cover_x_rate=0.6,
    cover_y_rate=0.03,
    time_str: str = "",
    font: ImageFont = None,
    font_color: str = "black",
    font_stroke_width: int = 1,
):
    image_width = image.width
    image_height = image.height

    # 1. 获取覆盖区域的背景色
    # 可以从图片中取样背景色，假设背景色位置在 (x, y)
    x = image_width * init_x_rate
    y = image_height * init_y_rate
    background_color = image.getpixel((x, y))  # 需要调整坐标以获取正确的背景色

    # 2. 用背景色覆盖原日期
    # 参数为左上角和右下角坐标
    draw.rectangle([(x, y), (x + image_width * cover_x_rate, y + image_height * cover_y_rate)], fill=background_color)
    # 3. 添加新日期

    # 获取当前时间并格式化
    # 先用标准格式获取时间字符串

    draw.text((x, y), time_str, font=font, fill=font_color, stroke_width=font_stroke_width, stroke_fill=font_color)


def modify_date(
    source_image: str,
    remove_other_date: bool = False,
    init_x_rate: float = 0.24,
    init_y_rate: float = 0.447,
    cover_x_rate: float = 0.6,
    cover_y_rate: float = 0.03,
    init_font_size: int = 53,
):
    # 打开原始图片
    image = Image.open(source_image)
    draw = ImageDraw.Draw(image)

    now = datetime.now().astimezone(timezone(timedelta(hours=8)))
    time_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
    # 去掉日期中的前导零
    time_str = time_str.replace("月0", "月").replace("日 ", "日 ")
    # use rel path for ttc
    font = ImageFont.truetype("./msyh.ttc", size=init_font_size, index=1)
    modify_image_date(
        image,
        draw,
        init_x_rate,
        init_y_rate,
        cover_x_rate,
        cover_y_rate,
        time_str=time_str,
        font=font,
    )

    if not remove_other_date:
        time_str = now.strftime("%Y-%m")
        font = ImageFont.truetype("./msyh.ttc", size=33)
        modify_image_date(
            image,
            draw,
            init_x_rate=0.323,
            init_y_rate=0.844,
            cover_x_rate=0.1,
            cover_y_rate=0.015,
            font_color="white",
            time_str=time_str,
            font=font,
        )

        time_str = now.strftime("%H:%M:%S")
        font = ImageFont.truetype("./msyh.ttc", size=45)
        modify_image_date(
            image,
            draw,
            init_x_rate=0.2,
            init_y_rate=0.87,
            cover_x_rate=0.18,
            cover_y_rate=0.02,
            font_color="white",
            time_str=time_str,
            font=font,
        )

    # 保存修改后的图片
    img_io = io.BytesIO()
    image.save(img_io, "PNG")
    img_io.seek(0)
    return img_io


@app.route("/pass_sjl")
def pass_sjl():
    img_io = modify_date("./sjl.png")
    return send_file(img_io, mimetype="image/png")


@app.route("/pass_hcs")
def pass_hcs():
    img_io = modify_date(
        "./hcs.png",
        remove_other_date=True,
        init_x_rate=0.19,
        init_y_rate=0.57,
        cover_x_rate=0.7,
        cover_y_rate=0.04,
        init_font_size=41,
    )
    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

import flet as ft
import math
import re

def main(page: ft.Page):
    page.title = "Calculator"
    page.window_width = 320
    page.window_height = 480
    page.bgcolor = "#181818"
    result = ft.Text(value="0", size=36, text_align="right", width=300, color="white")
    realtime = ft.Text(value="", size=20, text_align="right", width=300, color="#888888")
    current = ""

    def on_click(e):
        nonlocal current
        value = e.control.text
        if value == "AC":
            current = ""
            result.value = "0"
            realtime.value = ""
        elif value == "+/-":
            if current:
                if current.startswith("-"):
                    current = current[1:]
                else:
                    current = "-" + current
                result.value = current
                try:
                    if current and current[-1] not in "+-*/":
                        realtime.value = str(eval(current))
                    else:
                        realtime.value = ""
                except:
                    realtime.value = ""
        elif value == "%":
            try:
                if current:
                    current = str(float(current)/100)
                    result.value = current
                    realtime.value = current
            except:
                result.value = "Error"
                realtime.value = ""
                current = ""
        elif value == "^":
            # ใช้ ^ เป็นตัวดำเนินการยกกำลัง (แปลงเป็น **)
            if current and current[-1] not in "+-*/^.":
                current += "^"
                result.value = current
            page.update()
        elif value == "!":
            # แฟกทอเรียลของตัวเลขล่าสุด
            try:
                if current:
                    # หาเลขตัวสุดท้าย
                    match = re.search(r"(\d+)(?!.*\d)", current)
                    if match:
                        num = int(match.group(1))
                        fact = math.factorial(num)
                        # แทนที่เลขตัวสุดท้ายด้วยแฟกทอเรียล
                        current = current[:match.start(1)] + str(fact) + current[match.end(1):]
                        result.value = current
                        if current and current[-1] not in "+-*/^":
                            # eval ^ เป็น **
                            eval_str = current.replace("^", "**")
                            realtime.value = str(eval(eval_str))
                        else:
                            realtime.value = ""
            except:
                result.value = "Error"
                realtime.value = ""
                current = ""
            page.update()
        elif value == "=":
            try:
                eval_str = current.replace("^", "**")
                current = str(eval(eval_str))
                result.value = current
                realtime.value = ""
            except:
                result.value = "Error"
                realtime.value = ""
                current = ""
        else:
            if value == ".":
                # ป้องกันจุดซ้ำในตัวเลขเดียวกัน
                parts = current.split(" ")
                if "." in parts[-1]:
                    return
            current += value
            result.value = current
            try:
                if current and current[-1] not in "+-*/^":
                    eval_str = current.replace("^", "**")
                    realtime.value = str(eval(eval_str))
                else:
                    realtime.value = ""
            except:
                realtime.value = ""
        page.update()

    # ปุ่มและสี
    buttons = [
        ["AC", "+/-", "%", "/", "^"],  # เพิ่มปุ่มยกกำลัง ^
        ["7", "8", "9", "*", "!"],      # เพิ่มปุ่มแฟกทอเรียล !
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="]
    ]
    op_color = "#FF9500"
    func_color = "#D4D4D2"
    num_color = "#505050"
    text_white = "white"

    rows = [ft.Row([result], alignment="end"), ft.Row([realtime], alignment="end")]
    for i, row in enumerate(buttons):
        btns = []
        for j, text in enumerate(row):
            # สีปุ่ม
            if text in ["/", "*", "-", "+", "=", "^", "!"]:
                color = op_color
                txt_color = text_white
            elif text in ["AC", "+/-", "%"]:
                color = func_color
                txt_color = "black"
            else:
                color = num_color
                txt_color = text_white
            width = 60
            if text == "0" and i == 4:
                width = 130  # ปุ่ม 0 กว้างสองช่อง
            btns.append(
                ft.ElevatedButton(
                    text,
                    width=width,
                    height=60,
                    bgcolor=color,
                    color=txt_color,
                    on_click=on_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))
                )
            )
        rows.append(ft.Row(btns, alignment="center"))
    page.add(*rows)


ft.app(target=main, view=ft.WEB_BROWSER)

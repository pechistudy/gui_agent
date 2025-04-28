import pyautogui
import time
import webbrowser
from pyautogui import Point
import pyperclip

import openai
import base64
from io import BytesIO
from PIL import Image

openai_client = openai.AzureOpenAI(

)


# 1. 打开 Google Lens 网页
webbrowser.open('https://lens.google.com/')
time.sleep(2)  # 等页面加载完


# # 查看当前分辨率
# screen_width, screen_height = pyautogui.size()
# print(f"屏幕分辨率: {screen_width}x{screen_height}")

# 自己的结果是1728x1117
# 假设已经确定了目标坐标
x, y = 700, 830


pyautogui.moveTo(x, y)
pyautogui.click()
time.sleep(1)

# 3. 模拟输入图片 URL
image_url = ''

# 使用 pyperclip 将 URL 复制到剪贴板
pyperclip.copy(image_url)

# 4. 粘贴 URL 并按下回车
pyautogui.hotkey('command', 'v')  # 对于 macOS 使用 'command'+'v' 来粘贴
pyautogui.press('enter')  # 确认输入

# 等待结果加载
time.sleep(3)

# # 截屏的结果是2234, 3456
# screenshot = pyautogui.screenshot('current_screen.png')
# print(np.array(screenshot).shape)


input_location = pyautogui.locateCenterOnScreen('完全匹配.png', confidence=0.9)

# 逻辑2倍
scaled_x = int(input_location.x /2)
scaled_y = int(input_location.y /2)


pyautogui.moveTo(scaled_x, scaled_y)
pyautogui.click()
time.sleep(1)


# 点进网页
pyautogui.moveTo(400, 590) #间隔120
pyautogui.click()
time.sleep(5)
screenshot = pyautogui.screenshot()
# 保存为 BytesIO 对象
buffer = BytesIO()
screenshot.save(buffer, format="PNG")
buffer.seek(0)

# 转成 base64
img_base64 = base64.b64encode(buffer.read()).decode("utf-8")



# 生成提示内容
prompt = (
"我将上传一张商品页面的截图，请完成以下任务："
"1. 在图像中查找主商品的**原价**，而不是折扣价或促销价。"
"2. 如果图中显示多个价格，请优先选择最接近商品名称或商品图片的“原始价格”。"
"3. 忽略配件推荐、边栏广告或其他商品的信息。"
"4. 如果价格的单位不是美元（如人民币、日元、欧元等），请按照当前汇率**估算换算为美元**，并保留两位小数。"
"5. 如果图像中没有可识别的价格，请直接返回：“价格（美元）：无”。"
"**返回格式如下（仅这一行，无需解释）：**"
"价格（美元）：<金额或“无”>"
)

content_by_user = [
    {"type": "text", "text": prompt},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
]

mes = [
    {
        "role": "user",
        "content": content_by_user,
    }
]

# 调用 GPT 生成回答
attempt = 0
while attempt < 3:
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=mes,
            temperature=0,
        )
        res = completion.choices[0].message.content
        break  # 成功则跳出循环
    except Exception as e:
        print(f"Error during GPT-4 API call: {e}")
        attempt += 1
        if attempt < 3:
            print("Retrying after 3 second...")
            time.sleep(3)
        else:
            res = None

print(res)

# all_price_image = []
# for y_index in range(350, 830, 120):
#     pyautogui.moveTo(400, y_index)
#     pyautogui.click()
#     # 点进网页
#     time.sleep(5)
#     screenshot = pyautogui.screenshot
#     all_price_image.append(screenshot)
    
#     # 后退
#     pyautogui.moveTo(20, 100)
#     pyautogui.click()




# # 最后关闭页面
# pyautogui.moveTo(20, 50)
# pyautogui.click()


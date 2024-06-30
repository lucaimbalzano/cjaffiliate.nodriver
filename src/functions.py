from asyncio import sleep
from costants import BASE_SCREENSHOT_PATH
from nodriver import start, cdp, loop
from datetime import datetime
import os

async def yb_like_screenshot(email, password, link, id_profile, id_job):
    try:
    
        browser = await start()

        tab = browser.main_tab
        tab.add_handler(cdp.network.RequestWillBeSent, send_handler)
        tab.add_handler(cdp.network.ResponseReceived, receive_handler)

        tab = await browser.get("https://www.google.it/?hl=en")

        # handle_dialog
        reject_btn = await tab.find("reject all", best_match=True)
        await reject_btn.click()

        # handle sign in
        search_inp = await tab.select("textarea")
        await search_inp.send_keys("google translate")

        search_btn = await tab.find("google search", True)
        await search_btn.click()

        await tab.sleep(2)
        sign_in_btn = await tab.find("Sign in", True)
        await sign_in_btn.click()

        email_input = await tab.select("input[type=email]")
        await email_input.send_keys(email)

        next_btn = await tab.find("Next", True)
        await next_btn.click()

        await tab.sleep(4)

        password_input = await tab.select("input[type=password]")
        await password_input.send_keys(password)

        next_btn = await tab.find("Next", True)
        await next_btn.click()

        # handle screenshot
        youtube_video = await browser.get(link)
        await youtube_video.sleep(3)
        sleep(4)

        class_name = 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'
        # Use the class name to find the button
        button_like = await youtube_video.find(f'button.{class_name.replace(" ", ".")}')
        
        await button_like.click()

        print(button_like)
        await button_like.click()
        sleep(3)
        # await tab.sleep(10)
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%Y")
        current_time = now.strftime("%H-%M-%S")
        month_day_year = f"{day}-{month}-{year}"
        folder_name = f"{BASE_SCREENSHOT_PATH}/screenshots/{month_day_year}"
        filename = f"{current_time}_profile_job{id_job}_profile{id_profile}_yt_screeshot.png"

        os.makedirs(folder_name, exist_ok=True)

        # Save the screenshot
        screenshot_path = os.path.join(folder_name, filename)
        await youtube_video.save_screenshot(screenshot_path)
        browser.stop()
        return screenshot_path
    except Exception as error:
        print(f"Error while inside yb_like_screenshot: {error}")
        return None 

async def receive_handler(event: cdp.network.ResponseReceived):
    print(event.response)

async def send_handler(event: cdp.network.RequestWillBeSent):
    r = event.request
    s = f"{r.method} {r.url}"
    for k, v in r.headers.items():
        s += f"\n\t{k} : {v}"
    print(s)

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) != 5:
#         print("Usage: python script.py <email> <password> <link> <id_profile>")
#         sys.exit(1)
#     email = sys.argv[1]
#     password = sys.argv[2]
#     link = sys.argv[3]
#     id_profile = sys.argv[4]
#     loop().run_until_complete(main(email, password, link, id_profile))

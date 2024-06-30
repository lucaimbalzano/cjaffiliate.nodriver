from nodriver import start, cdp, loop


async def main():
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
    await search_inp.send_keys("google tanslate")

    search_btn = await tab.find("google search", True)
    await search_btn.click()

    await tab.sleep(2)
    search_btn = await tab.find("Sign in", True)
    await search_btn.click()

    email = await tab.select("input[type=email]")
    await email.send_keys("email")

    next_btn = await tab.find("Next", True)
    await next_btn.click()

    await tab.sleep(4)

    password = await tab.select("input[type=password]")
    # tab.find("id[password]", True) or await 
    await password.send_keys("password")

    next_btn = await tab.find("Next", True)
    await next_btn.click()


    # handle screenshot
    youtube_video = await browser.get('link')
    await youtube_video.sleep(3)

    class_name = 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'
    # Use the class name to find the button
    button_like = await youtube_video.find(f'button.{class_name.replace(" ", ".")}')

    # Click the like button
    await button_like.click()

    print(button_like)
    await button_like.click()

    await tab.sleep(10);
    await youtube_video.save_screenshot('youtube_video.png')
    browser.stop();


async def receive_handler(event: cdp.network.ResponseReceived):
    print(event.response)

async def send_handler(event: cdp.network.RequestWillBeSent):
    r = event.request
    s = f"{r.method} {r.url}"
    for k, v in r.headers.items():
        s += f"\n\t{k} : {v}"
    print(s)


if __name__ == "__main__":
    loop().run_until_complete(main())

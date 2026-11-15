"""Capture rapide : python shoot.py url out.png [largeur] [full]"""
import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w=1440, full=True):
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width": w, "height": 900 if w > 600 else 844}, device_scale_factor=1 if w > 600 else 2, reduced_motion="reduce")
        pg = await ctx.new_page()
        await pg.goto(url, wait_until="networkidle")
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
a = sys.argv
asyncio.run(main(a[1], a[2], int(a[3]) if len(a) > 3 else 1440, (a[4] != "0") if len(a) > 4 else True))

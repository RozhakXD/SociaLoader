import asyncio, httpx, re, urllib.parse
from io import BytesIO
from flask import jsonify

async def DownloadVideo(video_url):
    async with httpx.AsyncClient() as session:
        try:
            if 'instagram.com' in str(video_url):
                find_kode_postingan = re.search(r'instagram\.com/(?:p|reels?|tv)/([A-Za-z0-9_-]+)', str(video_url)).group(1)
                video_url = ('https://www.instagram.com/p/{}/embed/'.format(find_kode_postingan))
            else:
                return jsonify({"error": "Enter the Instagram reels link correctly. Please try again!"}), 400
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Sec-Fetch-Mode": "navigate",
                "Connection": "keep-alive",
                "Sec-Fetch-User": "?1",
                "Host": "www.instagram.com",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Dest": "document",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })
            response = await session.get("{}".format(video_url))
            if '"video_url":' in str(response.text.replace('\\', '')):
                final_video_url = re.search(r'"video_url":"(.*?)"', str(response.text.replace('\\', ''))).group(1).replace('u0025', '%')
            else:
                return jsonify({"error": "Can't find download link!"}), 400

            session.headers.update({
                "Accept-Encoding": "identity;q=1, *;q=0",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "no-cors",
                "Accept": "*/*",
                "Range": "bytes=0-",
                "Referer": "{}".format(final_video_url),
                "Sec-Fetch-Dest": "video",
                "Host": "{}".format(str(urllib.parse.urlparse(final_video_url).netloc)),
            })

            response3 = await session.get("{}".format(final_video_url))
            if response3.status_code in [200, 206]:
                video_stream = BytesIO()
                async for chunk in response3.aiter_bytes():
                    video_stream.write(chunk)
                video_stream.seek(0)
                return (video_stream)
            else:
                return jsonify({"error": "Failed to download video!"}), 400
        except Exception as e:
            return jsonify({"error": f"{str(e)}!"}), 400

def Instagram(video_url):
    return asyncio.run(DownloadVideo(video_url))
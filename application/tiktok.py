import asyncio, httpx, json, urllib.parse
from io import BytesIO
from flask import jsonify

async def DownloadVideo(video_url):
    async with httpx.AsyncClient() as session:
        try:
            if not 'tiktok.com' in str(video_url):
                return jsonify({"error": "Enter the TikTok video link correctly. Please try again!"}), 400
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "markdevs-last-api.onrender.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Accept-Encoding": "gzip, deflate",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            })
            response = await session.get("https://markdevs-last-api.onrender.com/api/tiktokdl?link={}".format(video_url))
            if '"url":' in str(response.text):
                final_video_url = str(json.loads(response.text)['url'])
                session.headers.update({
                    "Accept-Encoding": "identity;q=1, *;q=0",
                    "Sec-Fetch-Site": "same-origin",
                    "Accept": "*/*",
                    "Host": "{}".format(str(urllib.parse.urlparse(final_video_url).netloc)),
                    "Range": "bytes=0-",
                    "Referer": "{}".format(final_video_url),
                    "Sec-Fetch-Dest": "video",
                    "Sec-Fetch-Mode": "no-cors",
                })
                response2 = await session.get("{}".format(final_video_url))
                if response2.status_code in [200, 206]:
                    video_stream = BytesIO()
                    async for chunk in response2.aiter_bytes():
                        video_stream.write(chunk)
                    video_stream.seek(0)
                    return (video_stream)
                else:
                    return jsonify({"error": "Failed to download video!"}), 400
            else:
                return jsonify({"error": "Can't find download link!"}), 400
        except Exception as e:
            return jsonify({"error": f"{str(e)}!"}), 400

def Tiktok(video_url):
    return asyncio.run(DownloadVideo(video_url))
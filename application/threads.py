import asyncio, re, httpx, urllib.parse
from io import BytesIO
from flask import jsonify

async def DownloadVideo(video_url):
    async with httpx.AsyncClient() as session:
        try:
            if 'threads.net' in str(video_url):
                find_postingan_kode = re.search(r'/post/([^/?]+)', str(video_url)).group(1)
            else:
                return jsonify({"error": "Enter the Threads video link correctly. Please try again!"}), 400
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Host": "www.threads.net",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Mode": "navigate",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            })
            response = await session.get("{}".format(video_url))
            if '"code":' in str(response.text.replace('\\', '')) and '' in str(response.text.replace('\\', '')):
                final_video_url = str(re.search(r'"code":"' + str(find_postingan_kode) + '","carousel_media":.*?,"image_versions2":.*?,"url":\s*"([^"]*)"}', str(response.text)).group(1)).replace('\\', '').replace('u0025', '%')
            else:
                return jsonify({"error": "Can't find download link!"}), 400
            session.headers.update({
                "Host": "{}".format(str(urllib.parse.urlparse(final_video_url).netloc)),
            })

            response2 = await session.get("{}".format(final_video_url))
            session.headers.update({
                "Accept-Encoding": "identity;q=1, *;q=0",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "no-cors",
                "Accept": "*/*",
                "Range": "bytes=0-",
                "Referer": "{}".format(response2.url),
                "Sec-Fetch-Dest": "video",
            })
            response3 = await session.get(response2.url)
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

def Threads(video_url):
    return asyncio.run(DownloadVideo(video_url))
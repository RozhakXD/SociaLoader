import asyncio, httpx, json, urllib.parse
from io import BytesIO
from flask import jsonify

async def DownloadVideo(video_url):
    async with httpx.AsyncClient() as session:
        try:
            video_url = ('https://m.facebook.com' + str(video_url).split('.facebook.com')[1])
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "id,id-ID;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Host": "m.facebook.com",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
                "X-Requested-With": "com.merryblue.facebookvideodownloader"
            })
            response = await session.get("{}".format(video_url))
            cookie_string = "; ".join([f"{key}={value}" for key, value in response.cookies.items()])

            data = {
                "cookies_source": f"vpd=v1%3B931x600x1.5; {cookie_string}",
                "url": f"{response.url}"
            }
            session.headers.update({
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "okhttp/4.8.1",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Host": "alldownloader-2.merryblue.llc"
            })
            response2 = await session.post("https://alldownloader-2.merryblue.llc/api/v1/facebook/download", data=data)
            if '"status":true,' in str(response2.text) and '"url":' in str(response2.text):
                final_video_url = ("")
                for data in json.loads(response2.text)['results']['links']:
                    if str(data['format']) == 'hd':
                        final_video_url = data['url']
                    else:
                        continue
                if len(final_video_url) == 0:
                    final_video_url = json.loads(response2.text)['results']['links'][0]['url']
                session.headers.clear(

                )
                session.headers.update({
                    "Host": "{}".format(str(urllib.parse.urlparse(final_video_url).netloc)),
                    "User-Agent": "okhttp/4.8.1",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip"
                })
                response2 = await session.get("{}".format(final_video_url))
                looping = 0
                while (response2.status_code == 302):
                    if int(looping) <= 5:
                        response2 = await session.get("{}".format(response2.url))
                    else:
                        return jsonify({"error": "Link keeps redirecting!"}), 400
                    looping += 1
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

def Facebook(video_url):
    return asyncio.run(DownloadVideo(video_url))
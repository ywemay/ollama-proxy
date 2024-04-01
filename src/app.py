import httpx
from fastapi import FastAPI
from httpx import AsyncClient
from fastapi import Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
# from dotenv import load_dotenv
from urllib.parse import urlparse
import os

app = FastAPI()
base_url = os.getenv("ENDPOINT")
timeout = os.getenv("TIMEOUT", 90)
print ("Hooked to endpoint: " + base_url)
base_hostname = urlparse(base_url).netloc
HTTP_SERVER = AsyncClient(base_url=base_url)

async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    headers = {
        **request.headers,  # Spread the existing headers as a dictionary
        "Authorization": "Bearer " + os.getenv("API_KEY") if os.getenv("API_KEY") else "",
        "host": base_hostname
    }
    rp_req = HTTP_SERVER.build_request(
        request.method, url, headers=headers, timeout=timeout, content=await request.body()
    )
    rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    if (rp_resp.status_code > 399):
        rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    if (rp_resp.status_code > 399):
        rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    if (rp_resp.status_code > 399):
        rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    if (rp_resp.status_code > 399):
        rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )

app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11434, log_level="info")

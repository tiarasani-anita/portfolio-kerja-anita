# Endpoint ASGI sederhana untuk verifikasi deployment di Vercel.
# Aplikasi utama (Streamlit) tetap dijalankan via Streamlit Community Cloud.

import json


async def app(scope, receive, send):
    """Handler ASGI minimal: balas health check dengan JSON."""
    if scope["type"] == "http":
        body = json.dumps({
            "status": "ok",
            "app": "Portfolio Anita Tiara Sani",
            "message": "Gunakan Streamlit Community Cloud untuk menjalankan dashboard."
        }).encode("utf-8")

        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({
            "type": "http.response.body",
            "body": body,
        })
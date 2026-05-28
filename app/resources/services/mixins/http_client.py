import httpx
from fastapi import HTTPException


class HttpMixin:
    DEFAULT_TIMEOUT = httpx.Timeout(
        connect=10.0, read=60.0, write=10.0, pool=10.0
    )

    @staticmethod
    async def httpx_post(
        url: str,
        data: dict = None,
        headers: dict = None,
        timeout: httpx.Timeout = None
    ) -> dict:
        try:
            async with httpx.AsyncClient(
                timeout=timeout or HttpMixin.DEFAULT_TIMEOUT
            ) as client:
                response = await client.post(
                    url,
                    json=data or {},
                    headers=headers or {}
                )
                return HttpMixin._handle_response(response)
        except httpx.TimeoutException:
            raise HTTPException(status_code=400, detail="Tashqi server javob bermadi (timeout)")
        except httpx.ConnectError:
            raise HTTPException(status_code=400, detail="Tashqi serverga ulanib bo'lmadi")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"So'rov xatosi: {str(e)}")

    @staticmethod
    async def httpx_patch(
        url: str,
        data: dict = None,
        headers: dict = None,
        timeout: httpx.Timeout = None
    ) -> dict:
        try:
            async with httpx.AsyncClient(
                timeout=timeout or HttpMixin.DEFAULT_TIMEOUT
            ) as client:
                response = await client.patch(
                    url,
                    json=data or {},
                    headers=headers or {}
                )
                return HttpMixin._handle_response(response)
        except httpx.TimeoutException:
            raise HTTPException(status_code=400, detail="Tashqi server javob bermadi (timeout)")
        except httpx.ConnectError:
            raise HTTPException(status_code=400, detail="Tashqi serverga ulanib bo'lmadi")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"So'rov xatosi: {str(e)}")

    @staticmethod
    async def httpx_get(
        url: str,
        params: dict = None,
        headers: dict = None,
        timeout: httpx.Timeout = None
    ) -> dict:
        try:
            async with httpx.AsyncClient(
                timeout=timeout or HttpMixin.DEFAULT_TIMEOUT
            ) as client:
                response = await client.get(
                    url,
                    params=params or {},
                    headers=headers or {}
                )
                return HttpMixin._handle_response(response)
        except httpx.TimeoutException:
            raise HTTPException(status_code=400, detail="Tashqi server javob bermadi (timeout)")
        except httpx.ConnectError:
            raise HTTPException(status_code=400, detail="Tashqi serverga ulanib bo'lmadi")
        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"So'rov xatosi: {str(e)}")

    @staticmethod
    def _handle_response(response: httpx.Response) -> dict:
        if response.status_code in (200, 201, 204):
            return response.json()

        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text

        raise HTTPException(
            status_code=400,
            detail=error_detail
        )
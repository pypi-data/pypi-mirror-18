async def console_log(app, handler):
    async def middleware(request):
        print("➞ ", request.method, request.url)
        return await handler(request)
    return middleware

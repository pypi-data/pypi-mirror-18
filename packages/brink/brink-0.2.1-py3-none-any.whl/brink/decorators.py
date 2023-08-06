def require_request_model(cls, *args, validate=True, **kwargs):
    """
    Makes a handler require that a request body that map towards the given model
    is provided. Unless the ``validate`` option is set to ``False`` the data will
    be validated against the model's fields.

    The model will be passed to the handler as the last positional argument. ::

        @require_request_model(Model)
        async def handle_model(request, model):
            return 200, model
    """
    def decorator(handler):
        async def new_handler(request):
            body = await request.json()
            model = cls(**body)

            if validate:
                model.validate()

            return await handler(request, *args, model, **kwargs)
        return new_handler
    return decorator


ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/jwt/api_jws.py", line 257, in _load
    signing_input, crypto_segment = jwt.rsplit(b".", 1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 2, got 1)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 69, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/usr/local/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/usr/local/lib/python3.12/site-packages/starlette/middleware/cors.py", line 93, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "/usr/local/lib/python3.12/site-packages/starlette/middleware/cors.py", line 148, in simple_response
    await self.app(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 756, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 776, in app
    await route.handle(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 72, in app
    response = await func(request)
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/fastapi/routing.py", line 269, in app
    solved_result = await solve_dependencies(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/fastapi/dependencies/utils.py", line 600, in solve_dependencies
    solved = await call(**sub_values)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/src/src/backend/services/auth.py", line 90, in get_current_user
    return await self.validate_token(token)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/src/src/backend/services/auth.py", line 70, in validate_token
    confirm_user = self.decode_jwt(token).get("user")
                   ^^^^^^^^^^^^^^^^^^^^^^
  File "/src/src/backend/services/auth.py", line 62, in decode_jwt
    return jwt.decode(token, key=public_key, algorithms=[algorithms])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/jwt/api_jwt.py", line 210, in decode
    decoded = self.decode_complete(
              ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/jwt/api_jwt.py", line 151, in decode_complete
    decoded = api_jws.decode_complete(
              ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/jwt/api_jws.py", line 198, in decode_complete
    payload, signing_input, header, signature = self._load(jwt)
                                                ^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/jwt/api_jws.py", line 260, in _load
    raise DecodeError("Not enough segments") from err
jwt.exceptions.DecodeError: Not enough segments
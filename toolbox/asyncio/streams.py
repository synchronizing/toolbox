import asyncio
import ssl
from typing import Optional


async def tls_handshake(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    ssl_context: Optional[ssl.SSLContext] = None,
    server_side: bool = False,
):
    """
    Manually perform a TLS handshake over a stream.

    Args:
        reader: The reader of the client connection.
        writer: The writer of the client connection.
        ssl_context: The SSL context to use. Defaults to None.
        server_side: Whether the connection is server-side or not. Defaults to False.

    Note:
        If the `ssl_context` is not passed and `server_side` is not set, then
        `ssl.create_default_context()` will be used.

        For Python 3.6 to 3.9 you can use `ssl.PROTOCOL_TLS` for the SSL context. For
        Python 3.10+ you need to either use `ssl.PROTOCOL_TLS_CLIENT` or
        `ssl.PROTOCOL_TLS_SERVER` depending on the role of the reader/writer.

    Example:

        Client code:

        .. code-block:: python

            from toolbox.asyncio.streams import tls_handshake
            import asyncio

            async def client():
                reader, writer = await asyncio.open_connection("httpbin.org", 443, ssl=False)
                await tls_handshake(reader=reader, writer=writer)

                # Communication is now encrypted.
                ...

            asyncio.run(client())

        Server code:

        .. code-block:: python

            from toolbox.asyncio.streams import tls_handshake
            import asyncio
            import ssl

            async def server(reader, writer):
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile="server.crt", keyfile="server.key")
                await tls_handshake(
                    reader=reader,
                    writer=writer,
                    ssl_context=context,
                    server_side=True,
                )

                # Connection is now encrypted.
                ...

            async def main():
                srv = await asyncio.start_server(server, host="127.0.0.1", port=8888)
                async with srv:
                    await srv.serve_forever()

            asyncio.run(main())
    """

    if not server_side and not ssl_context:
        ssl_context = ssl.create_default_context()

    transport = writer.transport
    protocol = transport.get_protocol()

    loop = asyncio.get_event_loop()
    new_transport = await loop.start_tls(
        transport=transport,
        protocol=protocol,
        sslcontext=ssl_context,
        server_side=server_side,
    )

    reader._transport = new_transport
    writer._transport = new_transport

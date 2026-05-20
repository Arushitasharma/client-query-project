from app import create_app

import socket

app = create_app()


# FIND FREE PORT
def get_free_port():

    ports_to_try = [5000, 5001, 5002, 8000, 8080]

    for port in ports_to_try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as s:

            result = s.connect_ex(
                ("127.0.0.1", port)
            )

            # PORT FREE
            if result != 0:

                return port

    # RANDOM FREE PORT
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as s:

        s.bind(("", 0))

        return s.getsockname()[1]


if __name__ == "__main__":

    port = get_free_port()

    print(f"Running on port {port}")

    app.run(
        host="0.0.0.0",
        port=port
    )
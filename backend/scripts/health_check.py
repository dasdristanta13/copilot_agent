"""Container health check script."""

import sys

import httpx


def main() -> None:
    """Check the health of the application."""
    url = "http://localhost:8000/health"
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            print("Health check passed.")
            sys.exit(0)
        else:
            print(f"Health check failed with status code: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Health check failed to connect: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

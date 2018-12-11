"""Start the app."""
try:
    from app import app
except ImportError:
    from .app import app


if __name__ == '__main__':
    app.run()

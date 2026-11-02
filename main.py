"""Vercel entrypoint for the Flask application."""

from backend.app import app

# Vercel detects this top-level Flask WSGI application.

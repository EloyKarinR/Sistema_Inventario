#!/usr/bin/env python3
"""
Script de inicio simple para Vercel
"""
from api.index import app

if __name__ == "__main__":
    # Para testing local
    from wsgiref.simple_server import make_server
    
    with make_server('', 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

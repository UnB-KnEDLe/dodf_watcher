#!/bin/bash
pip install requests
cd /app/ && python3 main.py & python3 -m http.server --directory /app/dodf_json
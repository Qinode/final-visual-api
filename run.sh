#!/bin/bash
set -e
cd /api && gunicorn -b 0.0.0.0:8081 api:app
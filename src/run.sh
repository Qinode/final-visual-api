#!/bin/bash
set -e
cd /api/src && gunicorn -b 0.0.0.0:8081 things:app
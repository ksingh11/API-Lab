#!/usr/bin/env python3
"""Standalone script to seed the database"""

from app import create_app, db
from app.utils.seed import seed_database

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()

"""Core configuration settings"""

from datetime import datetime
from typing import Any, Dict

# In-memory storage
_DB: Dict[str, Any] = {
    "users": [{"id": 1, "username": "admin", "email": "admin@example.com"}],
    "features": [
        {
            "id": 1,
            "user_id": 1,
            "title": "СуперФича",
            "link": "https://www.reddit.com/",
            "price_estimate": 1000.99,
            "votes": 10,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ],
}

def get_db():
    """Get in-memory database"""
    return _DB

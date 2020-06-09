"""Module for database settings and actions."""
import os

from motor.motor_asyncio import AsyncIOMotorClient


async def init_db():
    """
    Initialize db and client of mongodb.

    Returns:
        AsyncIOMotorClient().editor: database of project.
    """
    mongo_uri = os.getenv('MONGO_URI')

    if mongo_uri is None:
        return AsyncIOMotorClient().editor

    return AsyncIOMotorClient(mongo_uri).editor

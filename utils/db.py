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


async def return_all(db):
    """
    Return all object in collection.

    Args:
        db: object of database

    Returns:
        all object in collections
    """
    cursor = db.user.find()
    documents = []

    async for document in cursor:
        documents.append(document)

    return documents


async def return_all_users_login(db):
    """
    Return all object in collection.

    Args:
        db: object of database

    Returns:
        all login in user collections
    """
    cursor = db.user.find()
    documents = []

    async for document in cursor:
        documents.append(document)

    return [logins['login'] for logins in documents]


async def return_last_id(db):
    """
    Return last id in collection.

    Args:
        db: instance of database

    Returns:
        last id in collection
    """
    documents = await return_all(db)
    document_ids = [document_id['id'] for document_id in documents]

    return max(document_ids, default=-1)

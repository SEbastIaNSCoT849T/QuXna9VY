# 代码生成时间: 2025-10-04 23:49:42
#!/usr/bin/env python

"""
Skill Certification Platform API

This application provides an API for a skill certification platform.
It allows users to register, login, and request skill certifications.
"""

import falcon
g
from falcon import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized
from falcon_auth import AuthMiddleware, MultiAuthBackend
from falcon_cors import CORS
from peewee import Model, IntegerField, CharField, SqliteDatabase

# Database setup
db = SqliteDatabase('skill_certification.db')

# Database models
class Skill(Model):
    """Represents a skill in the database."""
    id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        database = db

class User(Model):
    """Represents a user in the database."""
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    skills = CharField(null=True)

    class Meta:
        database = db

# Initialize database
db.connect()
db.create_tables([Skill, User], safe=True)
db.close()

# API resources
class SkillResource:
    """Handles skill requests."""

    def on_get(self, req, resp, skill_id):
        """Returns a skill by ID."""
        try:
            skill = Skill.get(Skill.id == skill_id)
            resp.media = {"id": skill.id, "name": skill.name}
        except Skill.DoesNotExist:
            raise HTTPNotFound

    def on_post(self, req, resp, skill_id):
        """Creates a new skill."""
        try:
            user_id = req.context.user.id
            skill_name = req. json.get("name")
            new_skill = Skill.create(name=skill_name)
            User.update({
                "skills": User.skills + "," + str(new_skill.id)
            },
            User.id == user_id)
            resp.media = {"id": new_skill.id, "name": new_skill.name}
        except Exception as e:
            raise HTTPBadRequest(f"Error creating skill: {e}")

class UserResource:
    """Handles user requests."""

    def on_get(self, req, resp, user_id):
        """Returns a user by ID."""
        try:
            user = User.get(User.id == user_id)
            resp.media = {"id": user.id, "username": user.username}
        except User.DoesNotExist:
            raise HTTPNotFound

    def on_post(self, req, resp):
        """Creates a new user."""
        try:
            username = req.json.get("username")
            password = req.json.get("password\)
            new_user = User.create(username=username, password=password)
            resp.media = {"id": new_user.id, "username": new_user.username}
        except Exception as e:
            raise HTTPBadRequest(f"Error creating user: {e}")

# Authentication
class Auth:
    """Handles authentication."""

    def authenticate(self, req, resp, params):
        """Authenticates the user."""
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            raise HTTPUnauthorized(
                "Authentication required",
                "No auth header provided."
            )
        auth_type, credentials = auth_header.split(" ")
        if auth_type != "Basic":
            raise HTTPUnauthorized(
                "Invalid authentication type", "Only Basic auth is supported."
            )
        try:
            username, password = base64.b64decode(credentials).decode("utf-8").split(":")
            user = User.get(User.username == username)
            if user.password != password:
                raise HTTPUnauthorized(
                    "Invalid credentials", "Check your username and password."
                )
            req.context.user = user
        except Exception as e:
            raise HTTPUnauthorized(f"Authentication error: {e}")

# Routes
api = falcon.API()
CORS(api)
AuthMiddleware(api, auth=Auth())

api.add_route("/skills", SkillResource())
api.add_route("/users", UserResource())
api.add_route("/skills/{skill_id}", SkillResource())
api.add_route("/users/{user_id}", UserResource())

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, User, Note
from schema import CreateUser, UpdateUser, CreateNote, UpdateNote

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_obj_by_id(cls, obj_id: int):
    obj = request.session.get(cls, obj_id)
    if obj is None:
        raise HttpError(404, "Object not found")
    return obj


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "User already exists")


def add_note(note: Note):
    try:
        request.session.add(note)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Note already exists")


class UserView(MethodView):
    @property
    def session(self):
        return request.session

    def get(self, user_id):
        user = get_obj_by_id(User, user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate_json(CreateUser, request.json)
        user = User(**json_data)
        add_user(user)
        return jsonify({"id": user.id})

    def patch(self, user_id):
        json_data = validate_json(UpdateUser, request.json)
        user = get_obj_by_id(User, user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id):
        user = get_obj_by_id(User, user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "deleted"})



class NoteView(MethodView):
    @property
    def session(self):
        return request.session

    def get(self, note_id):
        note = get_obj_by_id(Note, note_id)
        return jsonify(note.dict)

    def post(self):
        json_data = validate_json(CreateNote, request.json)
        note = Note(**json_data)
        add_note(note)
        return jsonify({"id": note.id})

    def patch(self, note_id):
        json_data = validate_json(UpdateNote, request.json)
        note = get_obj_by_id(Note, note_id)
        for field, value in json_data.items():
            setattr(note, field, value)
        add_note(note)
        return jsonify(note.dict)

    def delete(self, note_id):
        note = get_obj_by_id(Note, note_id)
        self.session.delete(note)
        self.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("user_view")

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule("/user/<int:user_id>/", view_func=user_view, methods=["GET", "PATCH", "DELETE"])


note_view = NoteView.as_view("note_view")

app.add_url_rule("/note/", view_func=note_view, methods=["POST"])
app.add_url_rule("/note/<int:note_id>/", view_func=note_view, methods=["GET", "PATCH", "DELETE"])


if __name__ == "__main__":
    app.run()

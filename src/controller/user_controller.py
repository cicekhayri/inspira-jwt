from inspira.auth.auth_utils import encode_auth_token, decode_auth_token
from inspira.decorators.http_methods import get, post
from inspira.decorators.path import path
from inspira.responses import JsonResponse
from inspira.requests import Request

from src.service.user_service import UserService


@path("/users")
class UserController:

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @get("/{id}")
    async def get_user(self, request: Request, id: int):
        auth_header = request.get_headers().get('authorization', '')
        auth_token = auth_header.split(" ")[1] if auth_header else ''

        if auth_token:
            decoded_data = decode_auth_token(auth_token)
            if decoded_data == id:
                user = self._user_service.get_user_by_id(decoded_data)
                context = {
                    "id": user.id,
                    "email": user.email
                }
                return JsonResponse(context)

        context = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }

        return JsonResponse(context, status_code=401)

    @post("/register")
    async def register_user(self, request: Request):
        body = await request.json()
        name = body['name']
        email = body['email']
        password = body['password']
        user = self._user_service.get_user_by_email(email)

        if not user:
            success = self._user_service.create_user(name, email, password)

            if success:
                return JsonResponse({"message": "User successfully registered."})
            else:
                return JsonResponse({"message": "Failed to register user"}, status_code=401)
        else:
            return JsonResponse({"message": "User already exists."})

    @post("/login")
    async def login(self, request: Request):
        body = await request.json()
        email = body['email']
        password = body['password']

        user = self._user_service.get_user_by_email(email)

        if user:
            if user.check_password_hash(password):
                auth_token = encode_auth_token(user.id)

                context = {
                    'auth_token': auth_token
                }

                return JsonResponse(context)
            else:
                return JsonResponse({"message": "Failed to login user"}, status_code=401)
        else:
            return JsonResponse({"message": "User not found"}, status_code=401)
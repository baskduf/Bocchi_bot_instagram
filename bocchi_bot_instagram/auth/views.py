import requests
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import hashlib

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = os.getenv('SCOPES')

def get_user_profile(access_token):
    url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
    response = requests.get(url)
    return response.json()


def instagram_login(request):
    auth_url = (
        f"https://www.facebook.com/v16.0/dialog/oauth?"
        f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    return redirect(auth_url)

def instagram_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No code provided'}, status=400)

    # Access Token 요청
    token_url = f"https://graph.facebook.com/v16.0/oauth/access_token"
    params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    response = requests.get(token_url, params=params)
    access_token_info = response.json()

    if 'access_token' in access_token_info:
        access_token = access_token_info['access_token']
        return JsonResponse({'access_token': access_token})
    else:
        return JsonResponse({'error': 'Failed to get access token'}, status=400)
    

def data_deletion_request(request):
    if request.method == "POST":
        # 요청 데이터 파싱
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # 사용자 ID 확인
        user_id = data.get("signed_request")
        if not user_id:
            return JsonResponse({"error": "Missing signed_request"}, status=400)

        # 사용자 ID 검증
        try:
            payload, signature = user_id.split('.')
            expected_signature = hashlib.sha256((payload + APP_SECRET).encode('utf-8')).hexdigest()

            if signature != expected_signature:
                return JsonResponse({"error": "Invalid signed_request"}, status=400)
        except Exception:
            return JsonResponse({"error": "Invalid signed_request format"}, status=400)

        # 데이터 삭제 처리 (여기서 사용자 데이터를 삭제)
        confirmation_code = f"delete_{payload}"

        # 응답
        return JsonResponse({
            "url": f"https://<your-app-domain>/delete_status/",
            "confirmation_code": confirmation_code
        })
    return JsonResponse({"error": "Invalid request method"}, status=400)

def delete_status(request):
    return JsonResponse({
        "status": "Data deletion in progress or completed."
    })
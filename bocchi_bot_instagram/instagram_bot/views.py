import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 인증 토큰 설정
VERIFY_TOKEN = "baskduf"

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            # 요청 데이터 파싱
            data = json.loads(request.body)
            print("Webhook Event Received:", json.dumps(data, indent=2))

            # 승인 취소 요청 처리
            for entry in data.get("entry", []):
                user_id = entry.get("id")  # 사용자 ID
                changes = entry.get("changes", [])
                
                for change in changes:
                    if change.get("field") == "permissions" and change.get("value") == "removed":
                        # 승인 취소 로직
                        delete_user_data(user_id)
                        print(f"Removed app permissions for user ID: {user_id}")

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Invalid request"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def delete_user_data(user_id):
    """
    사용자가 앱 권한을 취소했을 때 데이터를 삭제하는 로직.
    """
    # 데이터 삭제 로직 구현 (예: 데이터베이스에서 삭제)
    print(f"Deleting user data for user ID: {user_id}")
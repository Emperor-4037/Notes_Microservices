from auth import get_password_hash

try:
    result = get_password_hash("test123")
    print("Password hash successful:", result)
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()

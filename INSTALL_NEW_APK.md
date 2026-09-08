# Installing New APK with Local Backend

## Problem
The Flutter app must be rebuilt after changing the local API address. An Android emulator reaches the development machine through `10.0.2.2`.

## Solution: Uninstall Old APK & Install New One

### Step 1: Connect Your Android Device
```bash
# Verify device is connected
adb devices
```

### Step 2: Uninstall Old APK
```bash
adb uninstall com.example.employee_app
```

### Step 3: Install New APK
```bash
adb install "C:\Users\dell\OneDrive\Desktop\SwajitEngineering\employee_app\android\app\build\outputs\apk\release\app-release.apk"
```

Build the APK from the project root with:
```bash
cd employee_app
flutter build apk --release --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/
```

### Step 4: Launch App
- Open the app from the device app drawer
- **First time login required** (no old session exists)
- Use your credentials to login
- The app should now connect to the local backend

## Verify Build Date
The APK was built on: **2026-01-09 at 14:11** (82.29 MB)

## If Still Getting Error

**Check these:**
1. Is the Django server running on `127.0.0.1:8000`?
2. Is the emulator using `10.0.2.2:8000` as the host address?
3. Are you using the correct email/password for login?

## Alternative: Test with Debug APK

If issues persist, you can also test with the debug APK:
```bash
adb install "C:\Users\dell\OneDrive\Desktop\SwajitEngineering\employee_app\android\app\build\outputs\apk\debug\app-debug.apk"
```

Debug APK should use the same local API define.

---

**Support**: Check the app logs with: `adb logcat | grep flutter`

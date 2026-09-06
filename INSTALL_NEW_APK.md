# Installing New APK with Render Backend

## Problem
The Flutter app is showing "Unable to connect to server" because the old APK on your Android device is still pointing to `localhost:8000` instead of the Render backend.

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

The APK at this location was built with:
- **API_BASE_URL=https://swajit-engineering-backend.onrender.com/api/**

### Step 4: Launch App
- Open the app from the device app drawer
- **First time login required** (no old session exists)
- Use your credentials to login
- The app should now connect to the Render backend

## Verify Build Date
The APK was built on: **2026-01-09 at 14:11** (82.29 MB)

## If Still Getting Error

**Check these:**
1. Is your Android device connected to internet? (mobile data or WiFi)
2. Can you ping the backend from the device's browser?
   - Open: `https://swajit-engineering-backend.onrender.com/api/`
   - Should see a 401 error or API root response
3. Are you using the correct email/password for login?

## Alternative: Test with Debug APK

If issues persist, you can also test with the debug APK:
```bash
adb install "C:\Users\dell\OneDrive\Desktop\SwajitEngineering\employee_app\android\app\build\outputs\apk\debug\app-debug.apk"
```

Debug APK also has the Render URL configured.

---

**Support**: Check the app logs with: `adb logcat | grep flutter`

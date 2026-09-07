plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.example.employee_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.example.employee_app"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    val debugKeystore = file(System.getProperty("user.home") + "/.android/debug.keystore")

    signingConfigs {
        create("release") {
            if (debugKeystore.exists()) {
                keyAlias = "androiddebugkey"
                keyPassword = "android"
                storeFile = debugKeystore
                storePassword = "android"
            }
        }
    }

    buildTypes {
        release {
            // For development/demo builds, use debug keystore
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = false
            isShrinkResources = false
        }
    }
}

flutter {
    source = "../.."
}

val flutterApkOutputDirectory = rootProject.layout.projectDirectory.dir("../build/app/outputs/flutter-apk")

tasks.register<Copy>("copyDebugApkToFlutterOutput") {
    dependsOn("packageDebug")
    from(layout.buildDirectory.dir("outputs/apk/debug"))
    include("app-debug.apk")
    into(flutterApkOutputDirectory)
}

tasks.register<Copy>("copyReleaseApkToFlutterOutput") {
    dependsOn("packageRelease")
    from(layout.buildDirectory.dir("outputs/apk/release"))
    include("app-release.apk")
    into(flutterApkOutputDirectory)
}

tasks.matching { it.name == "assembleDebug" }.configureEach {
    finalizedBy("copyDebugApkToFlutterOutput")
}

tasks.matching { it.name == "assembleRelease" }.configureEach {
    finalizedBy("copyReleaseApkToFlutterOutput")
}

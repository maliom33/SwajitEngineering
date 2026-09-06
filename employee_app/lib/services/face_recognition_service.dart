import 'dart:async';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:geolocator/geolocator.dart';

class AttendanceLocationService {
  Future<Position> currentPosition() async {
    if (!await Geolocator.isLocationServiceEnabled()) {
      await Geolocator.openLocationSettings();
      throw StateError(
        'Location services are disabled. Turn on GPS in Settings, return to the app, and try again.',
      );
    }
    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.deniedForever) {
      await Geolocator.openAppSettings();
      throw StateError(
        'Location permission is blocked. Allow location access in App Settings, return to the app, and try again.',
      );
    }
    if (permission == LocationPermission.denied) {
      throw StateError('Location permission is required to mark attendance.');
    }
    try {
      return await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.medium,
          timeLimit: Duration(seconds: 45),
        ),
      );
    } on LocationServiceDisabledException {
      throw StateError(
        'Location services are disabled. Turn on GPS and try again.',
      );
    } on PermissionDeniedException {
      throw StateError('Location permission is required to mark attendance.');
    } on TimeoutException {
      throw StateError(
        'Unable to get a GPS fix within 45 seconds. Turn on GPS, enable precise location for this app, and try again outdoors or near a window.',
      );
    } catch (error) {
      throw StateError(
        'Unable to read the current location. Check GPS and app location permission, then try again.',
      );
    }
  }
}

class FaceVerificationResult {
  const FaceVerificationResult({required this.verified, this.employeeId});
  final bool verified;
  final int? employeeId;
}

abstract class FaceRecognitionService {
  Future<FaceVerificationResult> verifyIdentity();
}

class FaceCaptureResult {
  const FaceCaptureResult({
    required this.imagePath,
    required this.faceCount,
    required this.isSuitable,
    required this.message,
  });
  final String imagePath;
  final int faceCount;
  final bool isSuitable;
  final String message;
}

class FaceCameraService {
  FaceCameraService({FaceDetector? detector})
    : _detector =
          detector ??
          FaceDetector(
            options: FaceDetectorOptions(
              performanceMode: FaceDetectorMode.fast,
              enableTracking: false,
            ),
          );
  final FaceDetector _detector;
  CameraController? _controller;

  CameraController? get controller => _controller;

  Future<void> initialize() async {
    List<CameraDescription> cameras;
    try {
      cameras = await availableCameras();
    } on CameraException catch (error) {
      throw StateError(_cameraErrorMessage(error));
    }
    if (cameras.isEmpty) throw StateError('No camera is available.');
    final camera = cameras.firstWhere(
      (item) => item.lensDirection == CameraLensDirection.front,
      orElse: () => cameras.first,
    );
    _controller = CameraController(
      camera,
      ResolutionPreset.medium,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );
    try {
      await _controller!.initialize();
    } on CameraException catch (error) {
      await _controller?.dispose();
      _controller = null;
      throw StateError(_cameraErrorMessage(error));
    }
  }

  Future<FaceCaptureResult> captureAndDetect() async {
    final controller = _controller;
    if (controller == null || !controller.value.isInitialized) {
      throw StateError('Camera is not initialized.');
    }
    final image = await controller.takePicture();
    final faces = await _detector.processImage(
      InputImage.fromFilePath(image.path),
    );
    final message = faces.isEmpty
        ? 'No face detected. Please position your face inside the frame.'
        : faces.length > 1
        ? 'Multiple faces detected. Please make sure only one person is visible.'
        : _isSuitable(faces.single, image)
        ? 'Face detected. Recognition provider is pending.'
        : 'Please move closer and improve lighting.';
    return FaceCaptureResult(
      imagePath: image.path,
      faceCount: faces.length,
      isSuitable: faces.length == 1 && _isSuitable(faces.single, image),
      message: message,
    );
  }

  bool _isSuitable(Face face, XFile image) {
    final box = face.boundingBox;
    final width = box.width;
    final height = box.height;
    return width >= 100 && height >= 100 && File(image.path).existsSync();
  }

  Future<void> dispose() async {
    await _controller?.dispose();
    _controller = null;
  }

  Future<void> close() async {
    await dispose();
    await _detector.close();
  }

  String _cameraErrorMessage(CameraException error) => switch (error.code) {
    'CameraAccessDenied' =>
      'Camera permission is denied. Allow camera access in App Settings and try again.',
    'CameraAccessDeniedWithoutPrompt' =>
      'Camera permission is denied. Allow camera access in App Settings and try again.',
    'CameraAccessRestricted' => 'Camera access is restricted on this device.',
    _ =>
      'Unable to open the camera (${error.code}). Check camera permissions and try again.',
  };
}

class PendingFaceRecognitionService implements FaceRecognitionService {
  @override
  Future<FaceVerificationResult> verifyIdentity() async {
    throw UnsupportedError(
      'Face recognition provider is pending actual ML implementation.',
    );
  }
}

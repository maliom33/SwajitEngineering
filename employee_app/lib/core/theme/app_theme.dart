import 'package:flutter/material.dart';

abstract final class AppColors {
  static const background = Color(0xff061018);
  static const surface = Color(0xff0d1c25);
  static const elevated = Color(0xff132733);
  static const secondarySurface = Color(0xff18313e);
  static const accent = Color(0xffff5a36);
  static const cyan = Color(0xff169db3);
  static const success = Color(0xff2ccb8a);
  static const warning = Color(0xfff5b642);
  static const danger = Color(0xffe95656);
  static const text = Color(0xfff5f7f8);
  static const muted = Color(0xff9aaab3);
  static const line = Color(0xff26404c);
}

ThemeData buildAppTheme() {
  final scheme =
      ColorScheme.fromSeed(
        seedColor: AppColors.accent,
        brightness: Brightness.dark,
        surface: AppColors.surface,
      ).copyWith(
        primary: AppColors.accent,
        secondary: AppColors.cyan,
        surface: AppColors.surface,
        error: AppColors.danger,
      );
  return ThemeData(
    colorScheme: scheme,
    scaffoldBackgroundColor: AppColors.background,
    useMaterial3: true,
    fontFamily: 'sans',
    textTheme: const TextTheme(
      headlineLarge: TextStyle(
        fontWeight: FontWeight.w900,
        letterSpacing: -0.4,
      ),
      headlineMedium: TextStyle(fontWeight: FontWeight.w900),
      titleLarge: TextStyle(fontWeight: FontWeight.w800),
      titleMedium: TextStyle(fontWeight: FontWeight.w700),
      bodyLarge: TextStyle(color: AppColors.text, height: 1.35),
      bodyMedium: TextStyle(color: AppColors.muted, height: 1.35),
      labelLarge: TextStyle(fontWeight: FontWeight.w800),
    ),
    cardTheme: const CardThemeData(
      margin: EdgeInsets.zero,
      elevation: 0,
      color: AppColors.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(20)),
        side: BorderSide(color: AppColors.line),
      ),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.background,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: AppColors.surface,
      indicatorColor: AppColors.secondarySurface,
      labelTextStyle: WidgetStatePropertyAll(
        TextStyle(fontWeight: FontWeight.w800, fontSize: 11),
      ),
    ),
    navigationRailTheme: const NavigationRailThemeData(
      backgroundColor: AppColors.surface,
      indicatorColor: AppColors.secondarySurface,
      selectedIconTheme: IconThemeData(color: AppColors.accent),
      selectedLabelTextStyle: TextStyle(color: AppColors.text),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: AppColors.elevated,
      labelStyle: const TextStyle(color: AppColors.muted),
      prefixIconColor: AppColors.muted,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: BorderSide.none,
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: AppColors.line),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: const BorderSide(color: AppColors.accent, width: 2),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 17),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: AppColors.accent,
        foregroundColor: Colors.white,
        minimumSize: const Size.fromHeight(52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: AppColors.secondarySurface,
      side: BorderSide.none,
      labelStyle: const TextStyle(
        color: AppColors.text,
        fontWeight: FontWeight.w700,
      ),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(9)),
    ),
  );
}

class BrandLogo extends StatelessWidget {
  const BrandLogo({super.key, this.size = 48, this.showWordmark = false});
  final double size;
  final bool showWordmark;

  @override
  Widget build(BuildContext context) {
    final mark = ClipRRect(
      borderRadius: BorderRadius.circular(size * .22),
      child: Image.asset(
        'assets/images/logo.png',
        width: size,
        height: size,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => Container(
          width: size,
          height: size,
          color: AppColors.accent,
          alignment: Alignment.center,
          child: Text(
            'S',
            style: TextStyle(
              color: Colors.white,
              fontSize: size * .52,
              fontWeight: FontWeight.w900,
            ),
          ),
        ),
      ),
    );
    if (!showWordmark) return mark;
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        mark,
        const SizedBox(width: 12),
        const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'SWAJEET',
              style: TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.w900,
                letterSpacing: 1.8,
              ),
            ),
            Text(
              'ENGINEERING  /  E-LOGISTICS',
              style: TextStyle(
                color: AppColors.accent,
                fontSize: 9,
                fontWeight: FontWeight.w800,
                letterSpacing: 1.1,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class PageBackground extends StatelessWidget {
  const PageBackground({super.key, required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) => DecoratedBox(
    decoration: const BoxDecoration(
      gradient: LinearGradient(
        colors: [AppColors.background, Color(0xff091923)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
    child: child,
  );
}

class Eyebrow extends StatelessWidget {
  const Eyebrow(this.text, {super.key, this.color = AppColors.accent});
  final String text;
  final Color color;

  @override
  Widget build(BuildContext context) => Text(
    text,
    style: TextStyle(
      color: color,
      fontSize: 11,
      fontWeight: FontWeight.w900,
      letterSpacing: 1.5,
    ),
  );
}

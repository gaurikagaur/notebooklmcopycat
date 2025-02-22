{pkgs}: {
  deps = [
    pkgs.ffmpeg-full
    pkgs.espeak-ng
    pkgs.xsimd
    pkgs.pkg-config
    pkgs.libxcrypt
    pkgs.libsndfile
  ];
}

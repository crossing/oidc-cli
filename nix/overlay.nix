final: prev: {
  poetry2nix = prev.poetry2nix.overrideScope' (self: super: {
    defaultPoetryOverrides = super.defaultPoetryOverrides.extend (pyself: pysuper: {
        cheroot = pysuper.cheroot.override { preferWheel = true; };
        pyinstaller = pysuper.pyinstaller.overridePythonAttrs (old: {
          buildInputs = (old.buildInputs or [ ]) ++ [
            final.zlib
          ];
        });
        staticx = pysuper.staticx.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
            final.scons
          ];

          prePatch = ''
             sed -i "/^def get_anywhere/i base_env['ENV']['PATH'] = os.environ['PATH']" SConstruct
             sed -i "/^def get_anywhere/i base_env['LIBPATH'] = ['${final.stdenv.cc.libc.static}/lib', '\$LIBDIR']" SConstruct
             sed -i "/^def get_anywhere/i base_env['CPPPATH'] = ['${final.stdenv.cc.libc.dev}/include']" SConstruct
             sed -i "/^if has_nss/i has_nss = True" SConstruct
          '';
        });
    });
  });
}

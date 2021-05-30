{ pkgs ? import ./nix }:
with pkgs.poetry2nix;
mkPoetryApplication {
    projectDir = ./.;    
    overrides = overrides.withDefaults (self: super: {
        cheroot = super.cheroot.override { preferWheel = true; };
    });
}
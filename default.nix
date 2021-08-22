{ pkgs ? import ./nix }:
with pkgs.poetry2nix;
mkPoetryApplication {
    projectDir = ./.;    
}

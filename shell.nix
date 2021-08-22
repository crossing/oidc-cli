{ pkgs ? import ./nix }:
let
  shell = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
  };
in pkgs.mkShell {
  name = "oidc-cli";    
  buildInputs = with pkgs; [
    shell
    poetry
  ];
}

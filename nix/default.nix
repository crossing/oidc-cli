let
    sources = import ./sources.nix;
    poetry2nix = import (sources.poetry2nix + "/overlay.nix");
    poetry2nixOverlay = import ./overlay.nix;
    pkgs = import sources.nixpkgs {
        overlays = [ poetry2nix poetry2nixOverlay ];
    };
in pkgs

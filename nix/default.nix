let
    sources = import ./sources.nix;
    poetry2nixOverlay = import (sources.poetry2nix + "/overlay.nix");
    pkgs = import sources.nixpkgs {
        overlays = [ poetry2nixOverlay ];
    };
in pkgs

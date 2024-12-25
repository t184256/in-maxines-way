{
  description = "\"In Maxine's way\" book and accompanying code.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        ltex-ls-plus = pkgs.stdenvNoCC.mkDerivation rec {
          pname = "ltex-ls-plus";
          version = "18.3.0";
          src = pkgs.fetchurl {
            url = "https://github.com/ltex-plus/ltex-ls-plus/releases/download/${version}/ltex-ls-plus-${version}.tar.gz";
            sha256 = "sha256-TV8z8nYz2lFsL86yxpIWDh3hDEZn/7P0kax498oicls=";
          };
          nativeBuildInputs = [ pkgs.makeBinaryWrapper ];
          installPhase = ''
            runHook preInstall
            mkdir -p $out
            cp -rfv bin/ lib/ $out
            rm -fv $out/bin/.lsp-cli.json $out/bin/*.bat
            for file in $out/bin/{ltex-ls-plus,ltex-cli-plus}; do
              wrapProgram $file --set JAVA_HOME "${pkgs.jre_headless}"
            done
            runHook postInstall
          '';
        };
        noto-fonts-extracondensed = pkgs.stdenvNoCC.mkDerivation {
          name = "noto-fonts-extracondensed";
          inherit (pkgs.noto-fonts) version src;
          installPhase = ''
            mkdir $out
            cp -va fonts/NotoSans/unhinted/*/NotoSans-ExtraCondensed* $out/
            cp -va fonts/NotoSerif/unhinted/*/NotoSerif-ExtraCondensed* $out/
          '';
        };
        deps = with pkgs; [
          gnumake pandoc typst
          ltex-ls-plus
          ocamlPackages.cpdf
          (python3.withPackages (ps: with ps; [ruamel-yaml]))
        ];
        pdf = pkgs.stdenv.mkDerivation rec {
          name = "in-maxines-way-${bookVersion}";
          bookVersion = "1.0.0";  # scraped
          src = ./.;
          nativeBuildInputs = deps;
          phases = [ "unpackPhase" "patchPhase" "buildPhase" ];
          TYPST_FONT_PATHS = noto-fonts-extracondensed;
          enableParallelBuilding = true;
          patchPhase = "patchShebangs maint/*.py";
          makeFlags = [
            "-f" "maint/Makefile" "DESTDIR=${placeholder "out"}" "outputs"
          ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = deps;
          TYPST_FONT_PATHS = noto-fonts-extracondensed;
        };
        packages.default = pdf;
      }
    );
}

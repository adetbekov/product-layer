#!/usr/bin/env bash
# Clone third-party skill arms at pinned commits into bench/arms/.cache/ (git-ignored). Nothing here is vendored:
# licenses stay with the upstream repos, see bench/README.md. Usage: bash bench/arms/fetch.sh [arm ...]
set -euo pipefail
cd "$(dirname "$0")"
CACHE=.cache
mkdir -p "$CACHE"

# name repo sha path-in-repo
ARMS=(
  "szilu https://github.com/szilu/ux-designer-skill c869d32fd8df7bd7fcd1db68e93bd3e89eed5161 ."
  "design-for-ai https://github.com/ryanthedev/design-for-ai 37d7ae63d1afa45eb57ec90bc246cef6dd60c033 references"
  "kortix-genui https://github.com/kortix-ai/suna 04b2abdc9161e1f820f7482c0d22358f416a6a79 packages/starter/templates/managed/skills/kortix-genui"
  "dogfood https://github.com/vercel-labs/agent-browser c830d1b67dc18b754e305859f0ae587f858a1447 skill-data/dogfood"
)

checkout() {  # repo sha path dest: sparse, shallow checkout of one commit
  local repo=$1 sha=$2 path=$3 dest=$4
  rm -rf "$dest.src" && git init -q "$dest.src"
  git -C "$dest.src" remote add origin "$repo"
  if [ "$path" != "." ]; then
    git -C "$dest.src" sparse-checkout set --no-cone "/$path/"
  fi
  git -C "$dest.src" fetch -q --depth 1 origin "$sha"
  git -C "$dest.src" checkout -q FETCH_HEAD
}

frontmatter() {  # name description file: prepend skill frontmatter to a reference file that has none
  printf -- '---\nname: %s\ndescription: %s\n---\n\n' "$1" "$2" | cat - "$3"
}

for line in "${ARMS[@]}"; do
  read -r name repo sha path <<<"$line"
  if [ $# -gt 0 ] && [[ " $* " != *" $name "* ]]; then continue; fi
  dest="$CACHE/$name"
  checkout "$repo" "$sha" "$path" "$dest"
  rm -rf "$dest" && mkdir -p "$dest"
  case $name in
    szilu)
      mkdir "$dest/ux-designer" && cp -r "$dest.src"/SKILL.md "$dest.src"/references "$dest/ux-designer/" ;;
    design-for-ai)  # only the product half: ai-native and journey, each turned into a skill
      for sub in ai-native journey; do
        mkdir -p "$dest/$sub"
        cp -r "$dest.src/references/$sub/references" "$dest/$sub/"
        desc=$(sed -n '1p' "$dest.src/references/$sub/$sub.md" | cut -c1-300 | tr -d '"')
        frontmatter "$sub" "\"$desc\"" "$dest.src/references/$sub/$sub.md" > "$dest/$sub/SKILL.md"
      done ;;
    dogfood)  # Apache-2.0, agent-browser v0.27.0; needs the agent-browser CLI at the same version
      cp -r "$dest.src/$path" "$dest/dogfood" ;;
    kortix-genui)  # Elastic-2.0: used as an external path only, never copied into this repo
      cp -r "$dest.src/$path" "$dest/kortix-genui" ;;
  esac
  rm -rf "$dest.src"
  echo "$name -> bench/arms/$dest ($(find "$dest" -name SKILL.md | wc -l) skills)"
done

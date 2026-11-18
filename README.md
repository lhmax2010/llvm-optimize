# Native Tizen LLVM server verification kit

This release contains the offline profile skill, the product recipe patch, and a paired ARMv7/AArch64 training corpus. The recipe carries placeholder profile assets. A generation job replaces them with qualified offline assets before any production PGO enablement. The skill still requires a complete generation run for qualification.

The corpus contains 23 exact training inputs, 693 original header dependencies and the available license notices. Use DEPENDENCIES.json and LICENSES.md for file owners and SDK versions. Install the matching Tizen SDK on the server. In particular, the target GCC package supplies startup objects for driver discovery. Those binary SDK components are platform prerequisites. The extracted headers are a source dependency closure for inspection and compile-only dependency checking.

## Prepare and verify

1. Clone the release branch. Set RELEASE_REMOTE to the repository URL provided with this kit and configure your SSH identity for the Tizen review service before fetching LLVM.

~~~sh
/usr/bin/git clone --branch server-kit --depth 1 "$RELEASE_REMOTE" /path/to/server-kit
(cd /path/to/server-kit && /usr/bin/sha256sum -c /path/to/server-kit/SHA256SUMS)
~~~

2. Verify any split files, then reassemble them in numeric filename order. The parts are individually covered by SHA256SUMS. For a split training archive, run the following before extracting. For any other split file, use its exact basename from FULL-FILES.sha256.

~~~sh
/usr/bin/cat /path/to/server-kit/training-inputs.tar.xz.part-* > /path/to/server-kit/training-inputs.tar.xz
(cd /path/to/server-kit && /usr/bin/sha256sum -c /path/to/server-kit/FULL-FILES.sha256)
~~~

This release requires no reassembly when FULL-FILES.sha256 is absent. Use binary concatenation. Preserve the direct file checksum and every part checksum when publishing a split release.

3. Obtain the reviewed LLVM revision, apply the product patch and verify the complete tree. Use an empty destination. The spec hunk uses zero context against this exact base, so pass --unidiff-zero to both checks.

~~~sh
/usr/bin/git init /path/to/llvm-source
/usr/bin/git -C /path/to/llvm-source fetch --no-tags --depth 1 ssh://review.tizen.org:29418/platform/upstream/llvm refs/changes/95/361395/5
test "$(/usr/bin/git -C /path/to/llvm-source rev-parse FETCH_HEAD)" = 7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8
/usr/bin/git -C /path/to/llvm-source checkout --detach FETCH_HEAD
/usr/bin/git -C /path/to/llvm-source apply --check --index --unidiff-zero /path/to/server-kit/pgo-recipe.patch
/usr/bin/git -C /path/to/llvm-source apply --index --unidiff-zero /path/to/server-kit/pgo-recipe.patch
test "$(/usr/bin/git -C /path/to/llvm-source write-tree)" = ef9c45fb4f6b01f7ac410271153ff7b08552985a
/usr/bin/git -C /path/to/llvm-source commit -m "Apply the offline profile recipe locally"
~~~

4. Extract the training inputs and validate every file.

~~~sh
/usr/bin/tar -xJf /path/to/server-kit/training-inputs.tar.xz --directory /path/to/server-kit
(cd /path/to/server-kit && /usr/bin/sha256sum -c /path/to/server-kit/training-inputs.sha256)
~~~

5. Copy config.server.template.json to a machine-local JSON file. Keep llvm_base as the recorded source identity. Set source_commit to the commit printed by git rev-parse HEAD after applying and committing the patch locally. Set the source, input, target sysroot, compiler resource, GBS, SDK and output paths to their actual absolute values. The supplied project and snapshot are the Toolchain configuration. Use a fresh output directory and the reviewed job limits. Follow skill/SKILL.md for stage adapters and acceptance gates.

~~~sh
/usr/bin/python3 -B /path/to/server-kit/skill/scripts/pgo_pair.py \
  --config /path/to/profile-server.json --output /path/to/jobs/profile-pair --dry-run
~~~

## File inventory

SHA256SUMS enumerates all tracked files except itself, including this README. Its bytes are authenticated by the release commit. The extracted-file checksum manifest covers each training input, header and notice.

| File | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| DEPENDENCIES.json | Training and header identities, RPM provenance and SDK prerequisites | 348,360 | 5952d8f0348f90c09254558bf80275776f55e626b86c32ef917abda7ae3d507e |
| LICENSES.md | Source package, version and license inventory | 6,755 | 8995a82c86a3a0add2b2845fa117c51bd524b6f803364587357552a825f47417 |
| config.server.template.json | Source identity, project, snapshot and machine-path template | 5,233 | 7ba3bd1bf19bb20f5e1000cedb92b5e00664d8a48a8b03c3b7fb8492a00e1800 |
| pgo-recipe.patch | Product-only change from the reviewed base to the prepared tree | 26,091 | f839010d747f79c93f61cd93d371999f327d5bd81934232c8cf8b8cc2c3723cd |
| skill/SKILL.md | Agent instructions and operating boundaries | 11,741 | 93ad4a5a86448ba5b045ac2c17ac63cbdbf7d33e0d30d82b846f04a2538ab9f8 |
| skill/config.example.json | Standalone skill configuration example | 4,872 | 4beaabbc17fc593e99e1d06e9cf78699c8116c46ca75fc0da8885ae5467ed736 |
| skill/references/gates.md | BOLT and runtime gate formulas and cases | 2,228 | e955062076b6887f874b371e0b657d6f2e62f4dbc252a1f041e22de5df26ee19 |
| skill/references/manifest-schema.md | Manifest format and asset identities | 2,369 | c09a35d4150cf491161a642ca366ea94084b56f9d2a9a840368ab83ad477cc87 |
| skill/references/pgo-match-method.md | Current PGO match measurement status | 1,809 | f2129d2daa5543be8e5560480f32000bcf23b089b7c517c19c52a1aed398c2e5 |
| skill/references/resource-budget.md | Historical measurements and resource tiers | 3,211 | bce709361d1ab0205e0925850710bd2553814e7e2e3a8695c5bb1b461d43cfb4 |
| skill/references/training-set.json | Ordered training input identities and compiler flags | 18,569 | 7547e5b22afbc94c941062b9a2130079c735a6d19d29429747e49a9aac60ec78 |
| skill/references/training-set.md | Training source and reproduction guide | 7,216 | 9c2fc250444d97afeefc0ce8ec8c0c8cb0bc5bb8b92947f3259caef4454856e0 |
| skill/scripts/bolt_stale_gate.py | Validate authenticated BOLT rewrite counts and thresholds | 4,465 | 0ef2283a2d02024403d483170c8be2ea8ca983cba4b72e18b63b314ea6f9156b |
| skill/scripts/generate_synthetic.py | Reproduce the synthetic fixture bytes | 3,859 | d77996302ace91192a3e658a69d8d9083551fa2f6be7d4083fb41ab764c9bd26 |
| skill/scripts/manifest.py | Generate and verify profile manifests | 6,288 | 64954b7fa111655cbea3eea7bb7c4e306685b415cf1dde4b626763a2e81293b5 |
| skill/scripts/pgo_pair.py | Plan or orchestrate offline profile generation | 29,726 | 7df0d289cf4b883ab517ebc0e740549a8ffabd3697edcabd762985bed6f1c6e2 |
| skill/scripts/runtime_dep_check.py | Inspect shipped ELF files and archive members | 3,591 | 9a83f9c2febfdbf12a1d20453adec390b8d531c8d6e66ac30bac9d8ed4ba0511 |
| skill/tests/test_bolt_stale_gate.py | BOLT boundary fixtures | 3,721 | 7b1970b56b9ca0a4f7160f598061a6d687f69ece551f886f57b2c3685be9aaaa |
| skill/tests/test_manifest.py | Manifest behavior fixtures | 3,602 | 5c281470628350e9c7602620913e0bb8501393905cadcefe7433f1a8b110e921 |
| skill/tests/test_pgo_pair.py | Dry-run, input identity and progress fixtures | 4,812 | f29a6e27d181f577faab15db084af32b961aec485587a36440730cc636179b1d |
| skill/tests/test_runtime_dep_check.py | Runtime dependency gate fixtures | 2,800 | ccf755229acd30e31943d22c9a9bacfa18833320b8e2f8f206c3940576bcc74a |
| tizen-llvm-offline-profile.tar.gz | Independent installable copy of the skill | 30,521 | 9ccfb1019850ec57e0cc7f93ab6566955203d3428bf04d5754f3889b3adfc40c |
| training-inputs.sha256 | Checksums for extracted inputs, headers and notices | 122,513 | 9b103428d83fa2777734e334841a175418339c5401cd7d408a0d5b5e5b322c81 |
| training-inputs.tar.xz | Losslessly packed training corpus, header dependencies and notices | 15,945,848 | 8a12c724b43c98e0db6e6d66234d070769d85c91872aa623275032407eeb2962 |

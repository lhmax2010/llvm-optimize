# Profile manifest format 1

The UTF-8 JSON file is named llvm-profiles.manifest. The top-level fields are format (integer 1), status, llvm_version (major.minor.patch), profiles (rows), and provenance. The writer emits UNQUALIFIED. An independently qualified release manifest uses READY. The validator rejects PLACEHOLDER or any other status and requires an explicit opt-in even to check a draft. The product recipe must also compare llvm_version and the matching source/configuration identities.

Each row keys on project (T for Toolchain or D for Base-Dev), pgo (true) and bolt (true or false). A PGO row always has a profdata asset. The bolt=true row also requires its paired bolt_profile. Duplicate keys fail validation. Selecting PGO off returns the Source1200 baseline for BOLT on and no asset when both are off. The profile files referenced by different rows may be shared after their identities are qualified.

Each asset has a local xz basename file, uncompressed bytes and sha256, and compressed xz_bytes and xz_sha256. Sizes are positive integers and SHA-256 values are 64 lowercase hex digits. Files are read relative to the manifest. A SHA or size mismatch, unexpected path, symbolic link, invalid compression stream or PLACEHOLDER payload fails. Written assets and manifests use fresh files.

Provenance holds the source commit/tree, snapshot, recipe and GBS configuration identities, ordered training argv and input hashes, tool versions and SHA-256, the pre-BOLT ELF/runtime identities, instrumentation warning counts, and observed BOLT/PGO match status. Record platform and compiler differences before authorizing a shared asset. Keep exact machine paths only in job evidence as appropriate. Before source distribution, translate absolute host paths to documented logical identities and preserve their actual ordered flags and digests.

To combine project runs, stage the verified assets and merge the distinct T/D rows into a new manifest. Preserve each project-specific provenance record. Run the validator for each intended project and both effective BOLT modes. The validator checks file identity and selection. The release decision also requires package, object and identity qualification.

~~~sh
/usr/bin/python3 -B /path/to/skill/scripts/manifest.py check \
  --manifest /path/to/assets/llvm-profiles.manifest --project T --pgo on --bolt on
~~~

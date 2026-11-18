# 133-D evidence

- A records identities and permissions for backup files, deletion results and space accounting.
- B records the legacy test hooks and fixture diff, suite results, the recorded compiler command, runtime flags and candidate R.
- D records the initial and corrected profile-matching fixture runs.
- N3 records input digests, patch integration, RPM parsing, and in-tree configurations and Ninja graph checks. The full CMake logs and large generated files are retained locally.
- The host used a user service with MemoryMax=4G, MemorySwapMax=0, CPUQuota=200%, Nice=19 and IOSchedulingClass=idle. The N3 CMake project configurations ran sequentially.

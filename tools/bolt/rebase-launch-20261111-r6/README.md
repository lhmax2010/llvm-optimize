# r6 local entry: 2026-11-11

Authorized for one complete night run of fea0fe464d56e17f2c7588c557bfffd9f6ac352b on 2026-11-11, Toolchain first and Base-Dev second, and daytime rehearsal-02 checks. Daytime preparation does not run a full build.

Use ../run-night.sh from a project directory (or run-night.sh at the entry root). It calls each project's own launch.sh. Toolchain uses tizen-base-toolchain_20261030.061318; Base-Dev uses tizen-base-dev_20261030.061217. Build logic, limits, gates and comparisons are unchanged.

The copied night.py is preserved byte-for-byte and must not be used: its legacy coordinator calls the Base-Dev launcher for both projects and monitors different roots/unit names. The old launch.sh night branch remains unchanged for provenance, not as the authorized night command.

run-night.sh SOURCE_SHA --dry-run prints commands/units/roots without creating output directories or starting services. Without --dry-run it creates the summary directory, appends stdout/stderr to night.log, checks both full roots are absent, then waits for each project's controller to finish. A failed T result still proceeds to D. If controller state cannot be read, the queue stops because serial completion cannot be established. No terminal input is read.

Full roots: W/temp/rebase-359934-20261111-r6/{toolchain,basedev}.
Rehearsal roots: W/temp/rebase-359934-20261111-r6/rehearsal/{toolchain,basedev}/retry-02.
Summary: W/temp/night-20261111-r6/night.log.
Source: W/temp/rebase-359934-20261111-r6/source.

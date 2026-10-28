#
# spec file for package build-compare
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           build-compare
VCS:            platform/upstream/build-compare#52349a883ca10f0f8ea7a33fe4f8da6b01eb354f
Summary:        Build Result Compare Script
License:        GPL-2.0+
Group:          Development/Tools/Building
Url:            https://github.com/openSUSE/build-compare
Version:        2023.06.18
Release:        1.4
Source1:        COPYING
Source2:        same-build-result.sh
Source3:        pkg-diff.sh
Source4:        functions.sh
Source5:        srpm-check.sh
Source1001: 	build-compare.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
#!BuildIgnore:  build-compare

%description
This package contains scripts to find out if the build result differs
to a former build.


%prep
%setup -q -c -T
cp %{SOURCE1001} .

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/build/ $RPM_BUILD_ROOT/%_defaultdocdir/%name
install -m 0755 %SOURCE2 %SOURCE3 %SOURCE4 %SOURCE5 $RPM_BUILD_ROOT/usr/lib/build/
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT/%_defaultdocdir/%name/

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc %_defaultdocdir/%name
/usr/lib/build

%changelog
* Sat Jun 17 2023 olaf@aepfle.de
- Filter dune language version in dune-package files
* Wed May  3 2023 Oleg Girko <ol@infoserver.lv>
- Fix filtering compiled Python modules to handle Python >= 3.7
* Fri Apr 28 2023 olaf@aepfle.de
- remove timestamps from png files
* Sat Apr  8 2023 Oleg Girko <ol@infoserver.lv>
- Ignore more sections when comparing ELF executable files
* Fri Nov 25 2022 Stefan Brüns <stefan.bruens@rwth-aachen.de>
- Trim "PROVIDES" from source rpms (#59, bsc#1205998)
* Mon Sep 19 2022 Dirk Müller <dmueller@suse.com>
- move license to licensedir
- spec file cleanups
* Fri Sep  2 2022 Martin Kampas <martin.kampas@jolla.com>
- fix compatibility with older sed (#55)
* Tue Aug 23 2022 Martin Kampas <martin.kampas@jolla.com>
- handle more setuid/setgid ELF variants (#54)
* Mon Jun 20 2022 olaf@aepfle.de
- fix objdump parsing for non-executable sections (#53)
* Mon Jun 13 2022 olaf@aepfle.de
- fix objdump parsing (#52)
* Fri Mar  4 2022 olaf@aepfle.de
- handle -a also in same-build-result.sh
- Find rpmlint.log in more places
- fix logic error in appstream comparison
- rework exit handling in same-build-result.sh
- Fix result in case no rpmlint.log exist
- remove count of checks and packages from rpmlint.log
- remove Check time report from rpmlint.log
- ELF diffing performance improvements
- unpack packages in parallel
- Add zstd handling
* Wed Feb 23 2022 Stefan Seyfried <seife+obs@b1-systems.com>
- Add extra handling for KMP versions
* Tue Sep 21 2021 Stephan Kulow <coolo@suse.de>
- Fix build-compare for shadow package
* Mon Sep 20 2021 Andreas Schwab <schwab@suse.de>
- Properly drop another duration from rpmlint.log
* Mon Sep  6 2021 bwiedemann@suse.de
- Drop another duration from rpmlint.log
* Wed Aug 11 2021 olaf@aepfle.de
- Handle another Date: variant in DocBook generated man pages
* Mon Jul 27 2020 bwiedemann@suse.de
- Make output more diffable and readable
- Fix regression in compare_archive
- Fix unit tests
* Fri May 29 2020 olaf@aepfle.de
- Remove usage of readarray to remain compatible with bash3
* Fri May 29 2020 olaf@aepfle.de
- Colltect a list of known rpm tags and use it to build the
  queryformat string for the tags listed below (bsc#1172232)
  conflict obsolete oldsuggests provide recommend require suggest supplement
* Thu May 14 2020 olaf@aepfle.de
- Trim first line of man page to catch overly verbose tools (now Pandoc)
* Wed May 13 2020 olaf@aepfle.de
- compare also posttrans scripts, and pretrans + verifyscript
* Tue May  5 2020 olaf@aepfle.de
- handle oddly named ZIP archives
- touch watchdog every 15 instead of 57 minutes
* Tue Mar 31 2020 olaf@aepfle.de
- gtk-doc: filter version info from html files
* Fri Jan 10 2020 olaf@aepfle.de
- compare archives in separate directory to preserve existing files
- consider only files and symlinks in verify_before_processing
* Tue Jan  7 2020 olaf@aepfle.de
- this new decade must be handled in man pages created by docbook.xml
- use bash Process Substitution in diff_two_files
- use bash Process Substitution when processing ELF files
- move normalizing code from check_single_file into separate function
- better input verification in check_single_file
- split verification from diff_two_files into separate function
- move check for ignored files out of check_single_file
- separate helper functions from code in pkg-diff
- touch host watchdog when producing output and in loops (issue#35)
- add functions to touch host watchdog
- always run cleanup in check_compressed_file
- use EXIT handler in pkg-diff to remove tmpfiles
* Wed Aug 14 2019 John Vandenberg <jayvdb@gmail.com>
- pkg-diff.sh: Ignore R build timestamp & temp paths
  https://github.com/openSUSE/build-compare/pull/34
* Tue Feb 19 2019 olaf@aepfle.de
- javadoc: filter dc.created
- Support filenames with spaces
- jar: always list files without date+size
- Fix differing jars reported as identical
* Tue Aug 28 2018 ol@infoserver.lv
- Ignore value of Release header when comparing spec files
* Fri Jul  6 2018 olaf@aepfle.de
- pkg-diff: fix diff returning 0
* Wed Jul  4 2018 olaf@aepfle.de
- Match also ELF pie executable (bsc#1097339)
* Wed Jul  4 2018 olaf@aepfle.de
- Remove trailing space from two match patterns
* Tue Jun 26 2018 olaf@aepfle.de
- Recognize "setuid ELF nn-bit xSB shared object" ELF binaries
* Mon May 28 2018 olaf@aepfle.de
- Avoid large temporary files from hexdump output and avoid
  diff(1) runing OOM by using a fifo (issue#24)
* Fri Apr 13 2018 olaf@aepfle.de
- check rpm capabilities for recommends/suggests
* Fri Dec  8 2017 ol@infoserver.lv
- Ignore /usr/lib/.build-id differences in package filelist
* Mon Dec  4 2017 olaf@aepfle.de
- Treat .egg files as zip
* Wed Nov  8 2017 olaf@aepfle.de
- srpm check requires cpio
* Mon Nov  6 2017 olaf@aepfle.de
- Fix usage of cmp_spec and unrpm in srpm-check.sh
* Fri Nov  3 2017 olaf@aepfle.de
- Catch empty rpm -qp --qf output for tags not understood by rpm
* Fri Oct 20 2017 olaf@aepfle.de
- Remove newly introduced files-duplicate check from rpmlint
  In case files are hardlinked, the source and destination is
  scrambled in rpm output: the pkg will be republished.
  In case files are not hardlinked, the source and destination
  is scrambled in rpmlint output: the pkg will be republished
* Thu Jul 27 2017 olaf@aepfle.de
- Compare also supplements and recomments (issue#18)
* Fri Mar 31 2017 olaf@aepfle.de
- Handle timestamp and checksum in xen.efi
* Wed Mar 22 2017 olaf@aepfle.de
- Handle _kf5_htmldir, it HAD to be different...
* Tue Mar 21 2017 olaf@aepfle.de
- Handle /usr/share/vdr/locale/
* Sun Feb 12 2017 olaf@aepfle.de
- Remove warning file-contains-date-and-time from rpmlint.log
* Thu Jan  5 2017 olaf@aepfle.de
- Fix name-version-release regex for release without dots
* Wed Dec 14 2016 olaf@aepfle.de
- Remove warning about python mtime mismatch, a republish will not help (bsc#915948)
- Handle yet another variant of numbered anchor in html file
* Wed Nov  9 2016 olaf@aepfle.de
- Ignore /etc/ld.so.cache
- Ignore /etc/machine-id
* Tue Nov  8 2016 olaf@aepfle.de
- Ignore /etc/hosts
- Handle every path matching /share/man/ as man page
* Mon Nov  7 2016 ol@infoserver.lv
- Ignore .gnu_debugdata section when comparing ELF files.
* Wed Oct 12 2016 ro@suse.de
- pkg-diff.sh: use option --speed-large-files for diffing
  disassembler output (bsc#1003528)
* Wed Sep 21 2016 olaf@aepfle.de
- Handle broken symlinks
* Thu Aug 25 2016 olaf@aepfle.de
- Update strip_numbered_anchors to catch more random identifiers
* Wed Aug 24 2016 liezhi.yang@windriver.com
- functions.sh: improve deb and ipk checking
- Add support for deb and ipk packaging
- pkg-diff.sh: check for fifo (named fifo)
- pkg-diff.sh: remove space in the end for ftype
- pkg-diff.sh: check_single_file(): return at once when same
- functions.sh: run rpm once to make it faster
* Fri Aug  5 2016 olaf@aepfle.de
- Handle unknown ELF files as different.
* Wed Apr  6 2016 olaf@aepfle.de
- add used utilities to Requires
* Tue Mar  8 2016 olaf@aepfle.de
- Remove hacks from /var/adm/update-scripts|messages case
* Tue Mar  8 2016 olaf@aepfle.de
- Handle /var/adm/update-messages in scripts and filelist
* Mon Mar  7 2016 olaf@aepfle.de
- Whitespace in javadoc case
- Whitespace changes in html case
- Move case kde/gtk html up in the case list
- Move case rdoc html up in the case list
- Add option -a to same-build-result.sh and loop through all rpms
- Rework sorting of rpm files in same-build-result.sh
- Better diagnostic if number of subpackages changes
- Create tmpfiles earlier in same-build-result.sh
- Handle all javadoc html files
* Fri Mar  4 2016 olaf@aepfle.de
- Handle yet another variant of elc timestamps
* Thu Mar  3 2016 olaf@aepfle.de
- Handle timestamp in dvi files
- Handle Last-modified HTML META tag
- Handle yet another variant of javadoc timestamps
* Fri Jan  1 2016 schwab@suse.de
- Fix quoting in find expression
* Thu Oct 22 2015 olaf@aepfle.de
- Remove filename-too-long-for-joliet from rpmlint.log
* Mon Oct 12 2015 olaf@aepfle.de
- Filter out durations from rpmlint progress report
* Fri Oct  2 2015 olaf@aepfle.de
- Handle texi2html 5.0 timestamps
* Fri Aug 21 2015 seife+obs@b1-systems.com
- avoid -kmp packages with "filename-too-long-for-joliet"
  triggering constant republishing
* Wed Jul 15 2015 olaf@aepfle.de
- 2015.07.15
- Handle more texi2html generated files and patterns
* Wed Jun 17 2015 olaf@aepfle.de
- 2015.06.17
- Fix regex to handle /lib/(modules|firmware)/version-release-any properly
* Tue Apr 28 2015 olaf@aepfle.de
- 2015.04.28
- Filter InitrdID in /linuxrc.config
- Hexdump old and new file in parallel
- Sort cpio file list with files to compare
- Extract old and new files in parallel
- Ignore block device nodes
- Ignore character device nodes
- Always clean tmpdir on exit in pkg-diff.sh
- Handle squashfs files
* Mon Apr 13 2015 olaf@aepfle.de
- 2015.04.13
- Show hint if pkg-diff.sh returns non-zero
- Adjust intending in same-build-result.sh
- Handle /usr/src/packages/OTHER
- Handle "setuid directory"
* Fri Mar 20 2015 olaf@aepfle.de
- 2015.03.20
- Convert correct png file before comparison
- Avoid name clashes when comparing png files
- Handle filename changes gracefully when comparing unknown filetypes
- Use generic helper to compare png files
* Thu Feb 12 2015 olaf@aepfle.de
- Handle also .o files as ELF relocatable objects
* Thu Feb 12 2015 randy.e.witt@linux.intel.com
- Rename rpm-check.sh to pkg-diff.sh
* Tue Feb 10 2015 olaf@aepfle.de
- 2015.02.10
- Trim objdump output properly
- Trim .TH also in localized man pages (bnc#915941)
- Remove also DVIPSSource from .ps files
* Tue Feb 10 2015 randy.e.witt@linux.intel.com
- Print section differences even if assembly has differences.
- Add support for nested rpms.
- Make rpm-check work for "packages" other than rpm.
- Tell which section was different when doing ELF comparisons.
- Error when one of the rpms is not found
* Fri Feb  6 2015 olaf@aepfle.de
- 2015.02.06
- Remove more javadoc references (bnc#916161)
- Handle *.war files like *.jar files
- Trim name-version-release string in update-scripts
* Wed Feb  4 2015 olaf@aepfle.de
- 2015.02.04
- Handle ruby gem files, they are tar archives (bnc#916047)
- Remove Creator: and CreationDate: tags from .ps files (bnc#915952)
- Correct regex for hostname in libtool (bnc#916268)
* Tue Feb  3 2015 olaf@aepfle.de
- 2015.02.03
- Trim .TH also in perl man pages (bnc#915941)
- Trim first line of man page to catch overly verbose tools
- Use correct offset for patching mtime out of .pyc files
- Add BuildIgnore to allow bootstrap in sle11
* Mon Feb  2 2015 olaf@aepfle.de
- 2015.02.02
- Trim VERSION-RELEASE also in rpmlint log
- Adjust regex for spec comparing in src.rpm
- handle also stick and setuid directory from file(1) output
* Wed Jan 21 2015 olaf@aepfle.de
- 2015.01.21
- Remove leading spaces from file(1) output
- Force removal of tmpdir to handle files marked as read-only
* Fri Jan  9 2015 olaf@aepfle.de
- 2015.01.14
- Trim VERSION-RELEASE instead of RELEASE because the release number
  will match other substrings.
- Use regex instead  in sed /regex/ to match dots properly
- Handle plain cpio archives from gfxboot
- Add patterns for .TH header in man pages to handle all cases
* Wed Nov 26 2014 ohering@suse.de
- 2014.11.25
- correctly handle cmp_spec return code if file checksum differs
- handle also bz2 and xz compressed files with odd name
* Tue Nov 18 2014 ohering@suse.de
- 2014.11.15
- show sorted differences of rpmlint log (bnc#904092)
- handle kernel and kmp packages, but support for kernel* is disabled
- minor style fixes
- handle cpio archives
- handle absolute symlinks correctly
- handle all ELF sections, not only the ones starting with dot
* Wed Nov 12 2014 schwab@suse.de
- Use $(...) instead of `...` to avoid losing backslash quoting
* Fri Nov  7 2014 ohering@suse.de
- Update check-all option to really keep going and check all files
- Add check to recursively look into gzip files with odd suffix
  to properly handle /usr/share/vlc/skins2/default.vlt
* Sat Aug  2 2014 johannesobermayr@gmx.de
- Fix quoting .
* Tue Jul 29 2014 johannesobermayr@gmx.de
- Remove numbered anchors from all Docbook / HTML files (bnc#889629).
* Tue Jul 22 2014 meissner@suse.com
- if all ELF sections except build-id and .gnu_debuglink compare equal,
  this is the same binary.
* Thu Jul 17 2014 meissner@suse.com
- Allow file list changes where the release number is encoded
  in the filename.
- compare post-update message and scripts (fixes fetchmsttfonts
  constant republish) as they have the release number hardcoded.
* Tue Jul 15 2014 ohering@suse.de
- Fix shell syntax error in rpm-check.sh
- 2014.07.15
* Mon Jul  7 2014 aj@suse.com
- Fix last patch to not use non-existant file (bnc#877078).
* Fri May  9 2014 johannesobermayr@gmx.de
- Don't compare .note.gnu.build-id and .gnu_debuglink sections in ELF
  binaries (bnc#877078).
- Don't compare debuginfo packages.
* Thu Oct 17 2013 schwab@suse.de
- Also look into MSB shared objects
* Thu May 24 2012 aj@suse.de
- Only handle files, not directories when searching for packages.
  Patch by Matthieu Tanguay-Carel <mtanguay@thoughtworks.com>.
* Tue May  8 2012 aj@suse.de
- Further handling of pdf files (bnc#760867), patch by
  David Haller <david@dhaller.de>.
* Mon May  7 2012 aj@suse.de
- Further handling of pdf files (bnc#760867).
* Mon May  7 2012 aj@suse.de
- Handle /ID in pdf files (bnc#760867).
* Wed Apr  4 2012 reddwarf@opensuse.org
- Handle gtk-doc documentation
* Thu Mar  8 2012 reddwarf@opensuse.org
- Improve kde index.cache handling
* Wed Feb 22 2012 aj@suse.de
- Remove release from pre/post scripts.
* Wed Feb 22 2012 coolo@suse.com
- I changed my mind, appdata.xml is too hard to get right. So
  we need to support variable binary names for the appdata
* Sat Feb 18 2012 aj@suse.de
- Quote dot in release to not have false matches.
* Thu Feb 16 2012 coolo@suse.com
- fix missing test in shell script
* Thu Feb 16 2012 coolo@suse.com
- !unchanged if rpmlint.log was new created
- !unchanged if appdata.xml was new or updated
* Mon Feb  6 2012 aj@suse.de
- Fix off-by-one error in rpmlint processing that hit packages with
  just one binary package.
* Sun Feb  5 2012 aj@suse.de
- Improve rpmlint check.
* Sun Feb  5 2012 aj@suse.de
- Take care of date format change of unzip.
* Sun Feb  5 2012 aj@suse.de
- Replace all occurences of release in rpmlint, take care of
  temporary files in rpmlint
* Sun Feb  5 2012 aj@suse.de
- Use separate invocation lines for .TH lines to catch
  some better.
* Thu Jan 26 2012 aj@suse.de
- Remove release from rpmlint.log before comparing.
* Fri Jan 20 2012 aj@suse.de
- Sort rpmlint.log files first since the order is non-deterministic.
* Thu Jan 12 2012 aj@suse.de
- Fix syntax in same-build-result.sh.
* Mon Jan  9 2012 aj@suse.de
- Compare rpmlint.log if it exists.
* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
* Wed Aug 31 2011 coolo@suse.com
- comparing fileclass was no good idea after all
* Mon Jul 11 2011 dmueller@suse.de
- also compare fileclass
* Fri May 20 2011 aj@suse.de
- Remove debug echo output.
* Tue Apr 19 2011 aj@suse.de
- Handle libreoffice-bootstrap.
* Tue Mar 15 2011 aj@suse.de
- Use perl -e instead of -E (bnc#679562).
* Mon Feb 28 2011 aj@suse.de
- Increase version.
* Mon Feb 28 2011 mls@suse.de
- Check also the first part of the release to e.g. handle rebuild of complete
  distribution (bnc#674991).
* Thu Oct 28 2010 aj@suse.de
- If source file is different, do not compare binaries with check-all.
* Wed Oct 27 2010 aj@suse.de
- Handle /usr/lib/texmf/doc/man as well
* Tue Oct 26 2010 aj@suse.de
- Ignore metafont formats.
* Tue Oct 26 2010 aj@suse.de
- Enable check-all to check for all differences in all packages.
* Fri Oct 22 2010 aj@suse.de
- Handle new zip date.
- Handle heartbeat man page.
* Sun Sep 26 2010 aj@suse.de
- Fix man regex.
* Wed Sep 22 2010 coolo@novell.com
- ignore texlive's fmt files as discussed with werner
* Mon Sep 20 2010 aj@suse.de
- Handle man pages generated from docbook.
- Handle rubygem documentation.
* Mon Sep 20 2010 aj@suse.de
- Create common file functions.sh and cleanup code.
* Mon Sep 20 2010 lnussel@suse.de
- exclude delta rpms
* Mon Sep 20 2010 aj@suse.de
- Create script for just checking source rpms.
* Thu Sep  9 2010 aj@suse.de
- Handle another date format for man pages found in coreutils.
- Handle more html files, e.g. kdelibs4 and libvdpau.
* Thu Sep  9 2010 aj@suse.de
- Handle weekday in man page.
* Tue Aug 31 2010 aj@suse.de
- Refine texi2html rule (found in zsh)
* Fri Aug 27 2010 aj@suse.de
- Handle png files with timestamp if convert is installed.
* Fri Aug 27 2010 aj@suse.de
- Handle one more doxygen variation.
* Sun May 23 2010 aj@suse.de
- Release is at end of line, avoid wrong matches.
* Fri May 21 2010 cmorve69@yahoo.es
- Improved ELF executable detection (bnc#604049).
* Thu May 20 2010 aj@suse.de
- Don't skip cross-x86_64-gcc-icecream-backend binary rpms: tighten
  the checks for -32bit packages.
* Sun May 16 2010 aj@suse.de
- Further man pages tweek.
* Sun May 16 2010 aj@suse.de
- further kde meinproc tuning.
* Thu May 13 2010 aj@suse.de
- Further fixes for kde meinproc (bnc#604049).
* Wed May 12 2010 aj@suse.de
- Fix doxygen docu handling.
* Wed May 12 2010 aj@suse.de
- Handle one more GNU Classpath version.
- Further improve man page regexp.
* Tue May 11 2010 aj@suse.de
- Improve man page regexp.
* Tue May 11 2010 aj@suse.de
- Improve kde index.cache handling as suggested by Cristian Morales
  Vega in bnc#604049.
* Tue May 11 2010 aj@suse.de
- Handle deprecated-list.html generated by javadoc.
- Handle doxygen docu.
- Handle /etc/sendmail.cf as well.
- Improve texi2html regexp to handle qemu.
* Mon May 10 2010 aj@suse.de
- Handle kde index.cache files (bnc#604049).
- Fix for handling of man pages and javadoc files.
* Mon May 10 2010 aj@suse.de
- Handle kdelibs4
* Sat May  8 2010 aj@suse.de
- Fix typo in last change - thanks Dirk Müller.
* Fri May  7 2010 aj@suse.de
- Handle sendmail .cf files.
* Tue Mar 23 2010 aj@suse.de
- Handle mono files.
- Mount /proc if it's not mounted already to work around bug in
  build script.
* Sun Mar 14 2010 aj@suse.de
- Improve last regexp to fix virt-utils.
* Sat Mar  6 2010 aj@suse.de
- Improve regexp for last change.
* Fri Mar  5 2010 aj@suse.de
- Handle more man files.
* Sun Dec 13 2009 aj@suse.de
- Handle libtool writing the hostname
* Wed Nov 18 2009 aj@suse.de
- Some more gjdoc dates (found in ant-antlr).
* Thu Oct 22 2009 coolo@novell.com
- take out debugging code
* Wed Oct 14 2009 aj@suse.de
- Replace external /usr/bin/unrpm by small function to get
  rid of dependency of build.rpm.
* Thu Sep 24 2009 aj@suse.de
- Add comments.
* Wed Sep 23 2009 aj@suse.de
- Handle noarch subpackage in sort correctly.
* Tue Aug 25 2009 mls@suse.de
- the COPYRIGHT tag does not exist, map it back to LICENSE to
  be backward compatible
* Mon Aug 17 2009 aj@suse.de
- Handle texi2html output.
* Thu Aug  6 2009 aj@suse.de
- adjust gjdoc sed to match "August 1" and similar one-digit days.
* Tue Aug  4 2009 aj@suse.de
- Compare mono files with cmp, just in case (handles rfc).
* Sun Aug  2 2009 aj@suse.de
- Sort jar filelists before compare.
* Mon Jul 27 2009 aj@suse.de
- Fail rpm-check if unrpm does not exist (noticed with package
  build).
* Sun Jul 26 2009 aj@suse.de
- Fix problem found with building gettext-tools: tar packages
  directories.
* Thu Jul 23 2009 aj@suse.de
- Update version number.
* Tue Jul 21 2009 aj@suse.de
- Handle emacs bytecompiled files.
- Handle /usr/share/man/man3/*3pm perl man pages.
- Handle /var/adm/perl-modules/*.
- Handle fonts.dir, fonts.scale and encoding.dir.
* Tue Jul 21 2009 aj@suse.de
- Add return value for .a case so that it can succeed.
* Mon Jul 20 2009 aj@suse.de
- Fix typo in same-build-results.sh
- Ignore javadoc build stamp in javadoc html files.
- Use jar,fastjar or unzip to extract jar files.
* Wed Jul 15 2009 coolo@novell.com
- overwrite duplicated files in zip files
* Tue Jul 14 2009 coolo@novell.com
- support .jar and .zip files
- fix support of gzipped files
* Mon May  4 2009 coolo@suse.de
- compare content of *.tar too
* Mon May  4 2009 coolo@suse.de
- if objdump fails, fall back to hexdump (bnc#489965)
* Mon May  4 2009 coolo@suse.de
- ignore dates in mo files (bnc#489198)
* Tue Apr 28 2009 mmarek@suse.cz
- rpm-check.sh: add option --check-all to check all packaged files
  (useful for debugging)
* Sun Feb  8 2009 coolo@suse.de
- fix handling of hardlinks to compressed files
* Sat Feb  7 2009 coolo@suse.de
- fix handling of -32bit and -64bit
* Sat Feb  7 2009 coolo@suse.de
- fix command line order
* Fri Feb  6 2009 coolo@suse.de
- use --no-show-raw-insn for objdump -d
* Fri Feb  6 2009 coolo@suse.de
- hopefully fixed shell quoting for rpm command line
* Thu Feb  5 2009 coolo@suse.de
- fix 2 bugs
- don't ignore source rpms - changed sources should output
  changed source rpms, no matter if they create the same binaries
  (think of changed copyright header in spec files)
* Tue Jan 27 2009 adrian@suse.de
- Create initial package based on the work of Matz and Coolo
  This package provides script for the main build script to be able
  to check if a new build has the same result than the former one.
  The Build Service is able to skip the new build than.
- changes in source rpms are currently ignored, is that okay ?

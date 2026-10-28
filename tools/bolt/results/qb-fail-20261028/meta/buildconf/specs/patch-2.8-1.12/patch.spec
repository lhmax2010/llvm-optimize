Name:           patch
VCS:            platform/upstream/patch#be96ad5f238fdbb40629c26efe9588cfba25ecd9
Version:        2.8
Release:        1.12
License:        GPL-3.0-or-later
Summary:        The GNU patch command, for modifying/upgrading files
URL:            http://www.gnu.org/software/patch/patch.html
Group:          Development/Tools
Source0:        ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz
Source1001:     patch.manifest

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q

%build
cp %{SOURCE1001} .
export CFLAGS="$CFLAGS -D_GNU_SOURCE -fPIC"
export LDFLAGS="$LDFLAGS -pie"

autoreconf -fi
%configure
make %{?_smp_mflags}

%install
%make_install
%remove_docs

%files
%license COPYING
%manifest patch.manifest
%{_bindir}/*

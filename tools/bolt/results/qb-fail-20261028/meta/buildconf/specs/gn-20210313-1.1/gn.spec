#
# spec file for package gn
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Name:           gn
VCS:            platform/upstream/gn#f2384c76d5439ecf42e29db3a93026d892b6ff8d
Version:        20210313
Release:        1.1
Summary:        A meta-build system that generates build files for Ninja
License:        BSD-3-Clause
URL:            https://gn.googlesource.com/
#Source:         https://dev.gentoo.org/~floppym/dist/%{name}-%{version}.tar.xz
Source0:    %{name}-%{version}.tar.gz
Source1001:     gn.manifest
BuildRequires:  gcc-c++
BuildRequires:  ninja
BuildRequires:  python3-base
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
GN is a meta-build system that generates build files for Ninja.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export AR=%{__ar} RANLIB=%{__ranlib} CC=%{__cc} CXX=%{__cxx}

# bootstrap
python3 build/gen.py \
  --no-strip \
  --no-last-commit-position \
  --no-static-libstdc++
PV=%{version}
cat >out/last_commit_position.h <<-EOF
	#ifndef OUT_LAST_COMMIT_POSITION_H_
	#define OUT_LAST_COMMIT_POSITION_H_
	#define LAST_COMMIT_POSITION_NUM ${PV##0.}
	#define LAST_COMMIT_POSITION "${PV}"
	#endif  // OUT_LAST_COMMIT_POSITION_H_
EOF

ninja -C out %{?_smp_mflags} gn

%check
ninja -C out %{?_smp_mflags} gn_unittests
./out/gn_unittests

%install
install -Dm 0755 out/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog

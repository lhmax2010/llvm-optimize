Name:           ed
VCS:            platform/upstream/ed#b13c6b41000af4d2cb57fee8fefe0365d29fc8e5
Version:        1.22.3
Release:        1.1
License:        GPL-3.0+
Summary:        Standard UNIX Line Editor
Url:            http://www.gnu.org/software/ed/
Group:          Productivity/Editors/Other
Source:         %{name}-%{version}.tar.gz
Source1001: 	ed.manifest

%description
The standard, old Unix line editor.

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS="${CFLAGS} -fPIC"
LDFLAGS="${LDFLAGS} -pie"
%{configure} CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" CC=%__cc
%{__make} %{?_smp_mflags} CC="%{__cc}"

# %check
# make check

%install
%{makeinstall}
%{remove_docs}

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/%{name}
%{_bindir}/r%{name}


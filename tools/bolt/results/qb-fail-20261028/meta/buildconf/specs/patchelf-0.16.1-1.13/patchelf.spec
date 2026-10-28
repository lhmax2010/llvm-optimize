Name:           patchelf
VCS:            platform/upstream/patchelf#c3c65fdd0e57a845cdef3b0c6dc74c5288130aa4
Version:        0.16.1
Release:        1.13
License:        GPL-3.0
Summary:        A utility for patching ELF binaries
Url:            http://nixos.org/patchelf.html
Group:          Development/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Source1001: 	patchelf.manifest
BuildRequires:  gcc-c++
# not working here
ExcludeArch:    ppc ppc64

%description
PatchELF is a simple utility for modifing existing ELF executables and
libraries.  It can change the dynamic loader ("ELF interpreter") of
executables and change the RPATH of executables and libraries.

%prep
%setup -q
cp %{SOURCE1001} .

%build
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e "s/--param=ssp-buffer-size=4//g" )
CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -fPIC"
LDFLAGS="$LDFLAGS -pie"
%reconfigure
make

%check
%ifnarch %arm aarch64
# fixme: x86 specific parts in checks
#make check
%endif

%install
%make_install

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}/README.md
%{_bindir}/patchelf
%{_mandir}/man*/patchelf.*

Name:           tolua++
Version:        1.0.93
Release:        0
Summary:        C/C++ with Lua Integration Tool
Source:         http://www.codenix.com/~tolua/tolua++-%{version}.tar.bz2
Source1001: 	tolua++.manifest
Url:            http://www.codenix.com/~tolua/
Group:          Development/Libraries
License:        MIT
BuildRequires:  python3
BuildRequires:  scons
BuildRequires:  lua-devel
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

%description
tolua++ is an extended version of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to c++ such as:
* support for std::string as a basic type (this can be turned off by a command
  line option)
* support for class templates
as well as other features and bugfixes. 

%prep
%setup -q
cp %{SOURCE1001} .

%build
cat <<'EOF' > config_linux.py
import re,os

CCFLAGS = re.split(r"\s+", os.environ['CCFLAGS'])
LIBS = re.split(r"\s+", os.environ['LIBS'])
prefix = "%{_prefix}"
EOF

CCFLAGS="%{optflags} `pkg-config lua --cflags` -fPIC" \
LIBS="`pkg-config lua --libs-only-l`" \
scons %{?_smp_flags} \
    prefix="%{_prefix}" \
    libdir="%{_libdir}" \
    all

%install
CCFLAGS="%{optflags} `pkg-config lua --cflags` -fPIC" \
LIBS="`pkg-config lua --libs-only-l`" \
scons %{?_smp_flags} \
    prefix="%{buildroot}%{_prefix}" \
    libdir="%{buildroot}%{_libdir}" \
    install

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYRIGHT 
%{_bindir}/tolua++
%{_includedir}/tolua++.h
%{_libdir}/libtolua++.a

%changelog

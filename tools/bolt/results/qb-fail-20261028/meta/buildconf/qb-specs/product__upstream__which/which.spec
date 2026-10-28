Name:           which
Version:        2.17
Release:        11
License:        GPL-2.0
Summary:        Displays where a particular program in your path is located
Url:            http://savannah.gnu.org/projects/which
Group:          Applications/System
Source0:        http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
Source1001: 	which.manifest
BuildRequires:  readline-devel
Requires:       toybox

%description
which is provided by toybox; /usr/bin/which here is a symlink to it.
The complete GNU implementation remains available under the gnu_ name
prefix (/usr/bin/gnu_which).

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wno-error=implicit-function-declaration -std=c99"
%configure --program-prefix=gnu_

make %{?_smp_mflags}

%install
%make_install

# identical to the symlink toybox owns, so rpm treats it as shared
# rather than conflicting; keeps which usable with any toybox version
ln -s toybox %{buildroot}%{_bindir}/which

%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/which
%{_bindir}/gnu_which

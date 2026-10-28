%define rc_version 0

%if 0%{?rc_version}
%define release_prefix 0.rc%{rc_version}.
%endif

Name:       mic
Summary:    Image Creator for Linux Distributions
Version:    2.1.0
Release:    0
Group:      Development/Tools
License:    GPLv2
BuildArch:  noarch
URL:        http://www.tizen.org
Source0:    %{name}_%{version}.tar.gz
%if 0%{?tizen_version:1}
Source1001: mic.manifest
%endif

Requires:   python3 >= 3.2

#for mic in mic-bootstrap, we don't need the below three dependency packages.
#what is more, thre is no python3.x version currently in tizne platform.
#Requires:   python3-urlgrabber >= 3.9.0
#Requires:   yum
#Requires:   python3-requests
Requires:   python3-py

#xml module has been exist in python3 path once installing python3 package.
%if 0%{?suse_version}
Requires:   python3-xml
%endif

%if 0%{?tizen_version:1}
Requires:   python3-rpm
%else
Requires:   rpm-python3
%endif

Requires:   python3-pycurl
Requires:   python3-distro
Requires:   cpio
# not neccessary
Requires:   gzip
Requires:   bzip2

%if 0%{?tizen_version:1}
Requires:   qemu-linux-user
%else
Requires:   qemu-arm-static
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if ! 0%{?tizen_version:1}
BuildRequires:  python3-docutils
%endif

%if ! 0%{?centos_version}
BuildRequires:fdupes
%endif

%description
The tool mic is used to create and manipulate images for Linux distributions.
It is composed of three subcommand\: create, convert, chroot. Subcommand create
is used to create images with different types; subcommand convert is used to
convert an image to a specified type; subcommand chroot is used to chroot into
an image.

%prep
%setup -q -n %{name}-%{version}
%if 0%{?tizen_version:1}
cp %{SOURCE1001} .
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" python3 setup.py build
%if ! 0%{?tizen_version:1}
 make man
%endif

%install
rm -rf %{buildroot}
%if 0%{?suse_version}
python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}
%else
python3 setup.py install --root=%{buildroot} -O1
%endif

# install man page
mkdir -p %{buildroot}/%{_prefix}/share/man/man1
%if ! 0%{?tizen_version:1}
install -m644 doc/mic.1 %{buildroot}/%{_prefix}/share/man/man1
%endif

# install bash completion
install -d -m0755 %{buildroot}/%{_sysconfdir}/bash_completion.d/
install -Dp -m0755 etc/bash_completion.d/%{name}.sh %{buildroot}/%{_sysconfdir}/bash_completion.d/

# install zsh completion
install -d -m0755 %{buildroot}/%{_sysconfdir}/zsh_completion.d/
install -Dp -m0755 etc/zsh_completion.d/_%{name} %{buildroot}/%{_sysconfdir}/zsh_completion.d/

%if ! 0%{?centos_version}
%fdupes %{buildroot}
%endif


%files
%if 0%{?tizen_version:1}
%manifest %{name}.manifest
%endif
%defattr(-,root,root,-)
%if ! (0%{?suse_version} || 0%{?centos_version})
%license COPYING
%endif
%doc doc/*
%doc README.rst AUTHORS ChangeLog
%if ! 0%{?tizen_version:1}
%{_mandir}/man1/*
%endif
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{python3_sitelib}/*
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/*
%{_bindir}/mic
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/zsh_completion.d


Name:           zypper

License:        GPL-2.0+
Group:          System/Package Management
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        Command line software manager using libzypp
Version:        1.14.38
Release:        0
URL:            http://en.opensuse.org/Zypper
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}-rpmlintrc
Source10:       Exclude_subdirectory.patch
Source11:       add_pie_compile_option.patch
Source12:	    add_cstdint_to_fix_build_error.patch
Source1001: 	zypper.manifest
Source10001:	tizenbase.repo
Source10002:	tizenunified.repo
Source10003:	tizen.zypper.conf.sh

BuildRequires:  asciidoc
BuildRequires:  libxslt-tools
BuildRequires:  libzypp-devel
BuildRequires:  boost-devel
BuildRequires:  gettext-devel
BuildRequires:  readline-devel
BuildRequires:  augeas-devel
BuildRequires:  gcc-c++
BuildRequires:  cmake

Requires:       procps
Requires:       libzypp


%description
Zypper is a command line tool for managing software. It can be used to add
package repositories, search for packages, install, remove, or update packages,
install patches, hardware drivers, verify dependencies, and more.

Zypper can be used interactively or non-interactively by user, from scripts,
or front-ends.

Authors:
--------
    Jan Kupec <jkupec@suse.cz>
    Duncan Mac-Vicar <dmacvicar@suse.de>
    Martin Vidner <mvidner@suse.cz>
    Josef Reidinger <jreidinger@suse.cz>

%package log
Requires:       python >= 2.7
BuildArch:      noarch
Summary:        CLI for accessing the zypper logfile
License:        GPL-2.0+
Group:          System/Packages
%description log
CLI for accessing the zypper logfile

%package tizen-config
Requires:	zypper
BuildArch:	noarch
Summary:	zypper repo configuration for Tizen:Unified developers
Group:		System/Packages
%description tizen-config
Zypper repo configuration for Tizen:Unified developers.
This is for Tizen device and platform development.

%package aptitude
Summary:        aptitude compatibility with zypper
Group:          System/Packages
Requires:       perl
Requires:       zypper
BuildArch:      noarch

%description aptitude
provides compatibility to Debian's aptitude command using zypper

%package needs-restarting
Summary:        needs-restarting compatibility with zypper
Group:          System/Packages
Requires:       zypper
BuildArch:      noarch

%description needs-restarting
provides compatibility to YUM needs-restarting command using zypper

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}
%{__patch} -p1 < %{SOURCE11}
%{__patch} -p1 < %{SOURCE12}

%build
CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CXXFLAGS -std=c++14 -fPIC"
mkdir build
cd build

# The code base is the same, but SLES11-SP1 (suse_version == 1110)
# may use it's own set of .po files from po/sle-zypper-po.tar.bz2.
unset TRANSLATION_SET

cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DSYSCONFDIR=%{_sysconfdir} \
      -DMANDIR=%{_mandir} \
      -DCMAKE_VERBOSE_MAKEFILE=TRUE \
      -DCMAKE_C_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
      -DCMAKE_BUILD_TYPE=Release \
      -DUSE_TRANSLATION_SET=${TRANSLATION_SET:-zypper} \
      ..

#gettextize -f
make %{?_smp_mflags}
make -C po %{?_smp_mflags} translations

%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT
make -C po install DESTDIR=$RPM_BUILD_ROOT

# Create filelist with translations
cd ..
%{find_lang} zypper
%{__install} -d -m755 $RPM_BUILD_ROOT%{_var}/log
touch $RPM_BUILD_ROOT%{_var}/log/zypper.log

mkdir -p %{buildroot}%{_sysconfdir}/zypp/repos.d
mkdir -p %{buildroot}%{_bindir}
install -m 0644 %{SOURCE10001} %{buildroot}%{_sysconfdir}/zypp/repos.d/
install -m 0644 %{SOURCE10002} %{buildroot}%{_sysconfdir}/zypp/repos.d/
install -m 0755 %{SOURCE10003} %{buildroot}%{_sbindir}/

%{remove_docs}

%lang_package

%files
%manifest %{name}.manifest
%license COPYING
%config(noreplace) %{_sysconfdir}/zypp/zypper.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zypper.lr
%config(noreplace) %{_sysconfdir}/logrotate.d/zypp-refresh.lr
%{_sysconfdir}/bash_completion.d/zypper.sh
%{_bindir}/zypper
%{_bindir}/installation_sources
%{_sbindir}/zypp-refresh
%dir %{_datadir}/zypper
%{_datadir}/zypper/zypper.aug
%dir %{_datadir}/zypper/xml
%{_datadir}/zypper/xml/xmlout.rnc
# declare ownership of the log file but prevent
# it from being erased by rpm -e
%ghost %config(noreplace) %{_var}/log/zypper.log

%files log
%manifest %{name}.manifest
%{_sbindir}/zypper-log

%files aptitude
%manifest %{name}.manifest
%{_bindir}/aptitude
%{_bindir}/apt-get
%{_bindir}/apt
%dir %{_sysconfdir}/zypp/apt-packagemap.d/
%config(noreplace) %{_sysconfdir}/zypp/apt-packagemap.d/*

%files tizen-config
%manifest %{name}.manifest
%{_sbindir}/tizen.zypper.conf.sh
%config %{_sysconfdir}/zypp/repos.d/*

%files needs-restarting
%manifest %{name}.manifest
%{_bindir}/needs-restarting

%changelog

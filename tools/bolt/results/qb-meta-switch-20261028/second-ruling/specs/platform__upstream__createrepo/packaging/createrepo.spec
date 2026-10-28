Name:           createrepo
Version:        0.9.9
Release:        1
License:        GPL-2.0
Summary:        Creates a common metadata repository
Url:            http://createrepo.baseurl.org/
Group:          System/Base
Source:         %{name}-%{version}.tar.gz
Source1001: 	createrepo.manifest
BuildRequires:  python
Requires:       deltarpm
Requires:       python >= 2.7
Requires:       rpm >= 4.11.0
Requires:       python-rpm
Requires:       python-deltarpm
Requires:       python-libxml2
Requires:       yum >= 3.4.3
Requires:       yum-metadata-parser
BuildArch: noarch

%description
This utility will generate a common metadata repository from a directory of rpm
packages.

%prep
%setup -q
cp %{SOURCE1001} .

%build

%install
make DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} install

%files
%manifest %{name}.manifest
%defattr(-, root, root,-)
%license COPYING COPYING.lib
%{_sysconfdir}/bash_completion.d/
%{_datadir}/%{name}/
%{_bindir}/createrepo
%{_bindir}/modifyrepo
%{_bindir}/mergerepo
%{_mandir}/*/*
%{python_sitelib}/createrepo

%changelog

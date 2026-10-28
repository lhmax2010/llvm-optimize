Name:           perl-HTML-Tagset
VCS:            platform/upstream/perl-HTML-Tagset#d7b3f8f111e3fc472b469aa6c8fea327d2830665
Version:        3.24
Release:        1.1
License:        GPL-2.0+ or Artistic
Summary:        HTML::Tagset - data tables useful in parsing HTML
Url:            http://search.cpan.org/dist/HTML-Tagset/
Group:          Development/Libraries
Source0:        HTML-Tagset-%{version}.tar.gz
Source1001: 	perl-HTML-Tagset.manifest
BuildRequires:  perl

%description
This module contains several data tables useful in various kinds of
HTML parsing operations, such as tag and entity names.

%prep
%setup -q -n HTML-Tagset-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%changelog
* Mon Mar 11 2013 Patrick McCarty <patrick.mccarty@linux.intel.com> upstream/3.20@d68d071
- Add packaging
- Imported Upstream version 3.20

Name:           perl-libwww-perl
VCS:            platform/upstream/perl-libwww-perl#18ee080f1b56e8e75d77a08a07e66d1218d67950
Version:        6.81
Release:        1.1
License:        GPL-1.0 or Artistic
Summary:        A Perl interface to the World-Wide Web
Url:            http://search.cpan.org/dist/libwww-perl/
Group:          Development/Libraries
Source0:        libwww-perl-%{version}.tar.gz
Source1001: 	%{name}.manifest

BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(URI)
Requires:       perl(Compress::Zlib)
Requires:       perl-HTML-Parser >= 3.33

%description
The libwww-perl collection is a set of Perl modules which provides a
simple and consistent application programming interface to the
World-Wide Web.  The main focus of the library is to provide classes
and functions that allow you to write WWW clients. The library also
contain modules that are of more general use and even classes that
help you implement simple HTTP servers.

%prep
%setup -q -n libwww-perl-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

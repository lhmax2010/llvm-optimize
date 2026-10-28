Name:           perl-URI
VCS:            platform/upstream/perl-URI#aa01637c2cde4f7ed2a86d385be46172877f8d19
Version:        5.34
Release:        1.1
License:        GPL-1.0 or Artistic-1.0
Summary:        A Perl module implementing URI parsing and manipulation
Url:            http://search.cpan.org/dist/URI/
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-URI.manifest


BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).

%prep
%setup -q -n URI-%{version}
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

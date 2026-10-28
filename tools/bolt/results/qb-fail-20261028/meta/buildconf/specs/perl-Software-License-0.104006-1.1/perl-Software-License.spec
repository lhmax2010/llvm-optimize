Name:           perl-Software-License
VCS:            platform/upstream/perl-Software-License#d2171c1817cba691b65f72209d24bfd8f6057fe7
Version:        0.104006
Release:        1.1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Software::License - packages that provide templated software licenses
Url:            https://metacpan.org/pod/Software::License
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Software-License.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This module is part of CPAN toolchain, or is treated as such. 
As such, it follows the agreement of the Perl Toolchain Gang to require no newer version 
of perl than one released in the last ten years. This version may change by agreement 
of the Toolchain Gang, but for now is governed by the Lancaster Consensus of 2013 
and the Lyon Amendment of 2023 (described at the linked-to document).

Although it may work on older versions of perl, no guarantee is made that 
the minimum required version will not be increased. The version may 
be increased for any reason, and there is no promise that patches 
will be accepted to lower the minimum required perl.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%license LICENSE

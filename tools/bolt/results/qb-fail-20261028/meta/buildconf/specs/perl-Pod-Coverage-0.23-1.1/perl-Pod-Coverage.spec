Name:           perl-Pod-Coverage
VCS:            platform/upstream/perl-Pod-Coverage#75fadbf9d3d416bbbceb5ef538017100d09e4aea
Version:        0.23
Release:        1.1
License:        GPL-1.0 or Artistic-1.0
%define cpan_name Pod-Coverage
Summary:        Checks if the documentation of a module is comprehensive
Url:            http://search.cpan.org/dist/Pod-Coverage/
Group:          Development/Libraries/Perl
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-Pod-Coverage.manifest
Source1002: 	LICENSE
BuildRequires:  perl
BuildRequires:  perl(Devel::Symdump) >= 2.01
BuildRequires:  perl-macros
Requires:       perl(Devel::Symdump) >= 2.01

%description
Developers hate writing documentation. They'd hate it even more if their
computer tattled on them, but maybe they'll be even more thankful in the
long run. Even if not, _perlmodstyle_ tells you to, so you must obey.

This module provides a mechanism for determining if the pod for a given
module is comprehensive.

It expects to find either a '=head(n>1)' or an '=item' block documenting a
subroutine.

Consider: # an imaginary Foo.pm package Foo;

 =item foo

 The foo sub

 = cut

 sub foo {}
 sub bar {}

 1;
 __END__

In this example 'Foo::foo' is covered, but 'Foo::bar' is not, so the 'Foo'
package is only 50% (0.5) covered

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

%changelog

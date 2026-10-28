Name:           perl-Error
Version:        0.17030
Release:        0
License:        GPL-1.0 or Artistic-1.0
Summary:        Error/exception handling in an OO-ish way
Url:            http://search.cpan.org/dist/Error/
Group:          Development/Libraries/Perl
Source:         %{name}-%{version}.tar.gz
Source1001: 	perl-Error.manifest

BuildRequires:  perl
BuildRequires:  perl(Module::Build)
BuildRequires:  perl-macros
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(warnings)

BuildArch:      noarch

Requires:       perl(Scalar::Util)
Requires:       perl(warnings)

%description
The 'Error' package provides two interfaces. Firstly 'Error' provides a
procedural interface to exception handling. Secondly 'Error' is a base
class for errors/exceptions that can either be thrown, for subsequent
catch, or can simply be recorded.

Errors in the class 'Error' should not be thrown directly, but the user
should throw errors from a sub-class of 'Error'.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Build.PL installdirs=vendor
./Build build flags=%{?_smp_mflags}

%check
./Build test

%install
./Build install destdir=%{buildroot} create_packlist=0
%remove_docs
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

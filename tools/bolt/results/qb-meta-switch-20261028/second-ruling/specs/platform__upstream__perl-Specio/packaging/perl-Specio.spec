Name:           perl-Specio
Version:        0.48
Release:        1
License:        Artistic-2.0
Summary:        Base class for type libraries
Url:            https://metacpan.org/pod/Specio::Exporter
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Specio.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Inheriting from this package makes your package a type exporter. 
By default, types defined in a package are never visible outside 
of the package. When you inherit from this package, all the types
you define internally become available via exports.

The exported types are available through the importing package's t subroutine.

By default, types your package imports are not re-exported:

 package MyApp::Type::Library;

 use parent 'Specio::Exporter';

 use Specio::Declare;
 use Specio::Library::Builtins;

In this case, the types provided by Specio::Library::Builtins are not 
exported to packages which use MyApp::Type::Library.

You can explicitly ask for types to be re-exported:

  package MyApp::Type::Library;

  use parent 'Specio::Exporter';

  use Specio::Declare;
  use Specio::Library::Builtins -reexport;

In this case, packages which use MyApp::Type::Library will get 
all the types from Specio::Library::Builtins as well as any 
types defined in MyApp::Type::Library.

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

Name:           perl-Sub-Exporter-Progressive
Version:        0.001013
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Only use Sub::Exporter if you need it
Url:            https://metacpan.org/pod/Sub::Exporter::Progressive
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Sub-Exporter-Progressive.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Sub::Exporter is an incredibly powerful module, but with that power
comes great responsibility, er- as well as some runtime penalties. 
This module is a Sub::Exporter wrapper that will let your users just 
use Exporter if all they are doing is picking exports, but use Sub::Exporter 
if your users try to use Sub::Exporter's more advanced features, 
like renaming exports, if they try to use them.

Note that this module will export @EXPORT, @EXPORT_OK and %EXPORT_TAGS 
package variables for Exporter to work. Additionally, if your package 
uses advanced Sub::Exporter features like currying, this module will 
only ever use Sub::Exporter, so you might as well use it directly.

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

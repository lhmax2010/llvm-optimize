Name:           perl-inc-latest
VCS:            platform/upstream/perl-inc-latest#93b1841f698690b73365157dbf5cf00daec847ad
Version:        0.500
Release:        1.1
License:        Apache 2.0
Summary:        inc::latest - use modules bundled in inc/ if they are newer than installed ones
Url:            https://metacpan.org/pod/inc::latest
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-inc-latest.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
WARNING -- THIS IS AN EXPERIMENTAL MODULE. 
It was originally bundled (as an experiment) with Module::Build
and has been split out for more general use.

The inc::latest module helps bootstrap configure-time dependencies
for CPAN distributions. These dependencies get bundled into the inc
directory within a distribution and are used by Makefile.PL or Build.PL.

Arguments to inc::latest are module names that are checked agains
t both the current @INC array and against specially-named directories in inc.
If the bundled version is newer than the installed one (or the module isn't
installed, then, the bundled directory is added to the start of @INC
and the module is loaded from there.

There are actually two variations of inc::latest -- one for authors
and one for the inc directory. For distribution authors, the inc::latest
installed in the system will record modules loaded via inc::latest and 
can be used to create the bundled files in inc, including writing
the second variation as inc/latest.pm.

This second inc::latest is the one that is loaded in a distribution
being installed (e.g. from Makefile.PL or Build.PL). This bundled
inc::latest is the one that determines which module to load.

Special notes on bundling
The inc::latest module creates bundled directories based on the packlist file 
of an installed distribution. Even though inc::latest takes module name arguments,
it is better to think of it as bundling and making available entire distributions.
When a module is loaded through inc::latest, it looks in all bundled distributions 
in inc/ for a newer module than can be found in the existing @INC array.

Thus, the module-name provided should usually be the "top-level" module name 
of a distribution, though this is not strictly required. inc::latest has 
a number of heuristics to discover module names, allowing users to do things 
like this:

use inc::latest 'Devel::AssertOS::Unix';
even though Devel::AssertOS::Unix is contained within the Devel-CheckOS 
distribution.

At the current time, packlists are required. Thus, bundling dual-core modules
may require a 'forced install' over versions in the latest version of perl 
in order to create the necessary packlist for bundling.

Managing dependency chains
Before bundling a distribution you must ensure that all prerequisites 
are also bundled and load in the correct order.

For example, if you need Wibble, but Wibble depends on Wobble, and 
you have bundled Module::Build, your Build.PL might look like this:

use inc::latest 'Wobble';
use inc::latest 'Wibble';
use inc::latest 'Module::Build';

 Module::Build->new(
   module_name => 'Foo::Bar',
   license => 'perl',
 )->create_build_script;

Authors are strongly suggested to limit the bundling of additional 
dependencies if at all possible and to carefully test their distribution
tarballs before uploading to CPAN.

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

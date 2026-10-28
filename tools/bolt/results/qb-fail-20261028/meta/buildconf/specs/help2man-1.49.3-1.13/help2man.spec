Name:           help2man
VCS:            platform/upstream/help2man#8346ee882eba5438177f82f1615eb736dc865b2e
Version:        1.49.3
Release:        1.13
License:        GPL-3.0+
Summary:        Create Simple Man Pages from --help Output
Url:            https://www.gnu.org/software/help2man/
Group:          Development/Tools/Doc Generators
Source:         %{name}-%{version}.tar.gz
Source1001: 	help2man.manifest
BuildRequires:  gettext-tools
BuildRequires:  perl-gettext
Requires:       perl-gettext

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a way
to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --enable-nls
%{__make} %{?_smp_mflags}

%install
%make_install

%remove_docs
%find_lang %{name} --with-man

%files -f %{name}.lang
%manifest %{name}.manifest
%license COPYING
%{_bindir}/help2man
%{_libdir}/help2man/

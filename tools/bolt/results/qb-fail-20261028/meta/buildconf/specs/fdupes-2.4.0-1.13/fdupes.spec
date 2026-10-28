Name:           fdupes
VCS:            platform/upstream/fdupes#ea990c402be2ddd6653782c4752b5cfe46bbe4fc
Version:        2.4.0
Release:        1.13
License:        MIT
Summary:        Identifying or deleting duplicate files
URL:            http://premium.caribe.net/~adrian2/fdupes.html
Group:          Base/Compression
Source0:        %{name}-%{version}.tar.bz2
Source1:        macros.fdupes
Source1001:     fdupes.manifest

%description
FDUPES is a program for identifying or deleting duplicate files
residing within specified directories. It supports various features
including ncurses interface, SQLite database storage, and PCRE2
pattern matching.

%prep
%setup -q
cp %{SOURCE1001} .

%build
# Reconfigure to pick up Tizen-specific settings
%{reconfigure} --without-ncurses --without-sqlite
%{__make} %{?_smp_mflags} CFLAGS="%{optflags} -fPIC -pie"

%install
# Install main binary
install -D -m 755 fdupes %{buildroot}%{_bindir}/fdupes

# Install RPM macros
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.fdupes

# Remove documentation and man pages as per Tizen guidelines
%{remove_docs}

%files
%manifest %{name}.manifest
%license README
%{_bindir}/fdupes
%config %{_sysconfdir}/rpm/macros.fdupes

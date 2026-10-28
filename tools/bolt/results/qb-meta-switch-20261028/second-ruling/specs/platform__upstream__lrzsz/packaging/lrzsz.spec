Summary: Serial file transfer protocols
Name: lrzsz
Version: 0.12.20
Release: 2
License: GPL-2.0
Group: Network & Connectivity/Utilities
Source: %{name}-%{version}.tar.gz
Summary(de): Seriendateiübertragungsprotokolle
Summary(fr): Protocoles de transfert de fichiers de série
Summary(tr): Modem protokolleri
BuildRequires: gettext-tools

%description
This collection of commands can be used to download and upload
files using the Z, X, and Y protocols.  Many terminal programs
(like minicom) make use of these programs to transfer files.

%description -l de
Diese Sammlung von Befehlen läßt sich zum Herunter- und
Aufwärtsladen von Dateien anhand der Z-, X- und Y-Protokolle benutzen.
Viele Terminalprogramme (wie Minicom) setzen diese Programme für die
Übertragung von Dateien ein.

%description -l fr
Cet ensemble de commande sert à télécharger des fichiers en utilisant
les protocoles Z, X et Y. De nombreux programmes de terminal (comme
minicom) utilisent ces programmes pour transférer les fichiers.

%description -l tr
Bu komutlar topluluðu Z, X ve Y protokollerini kullanarak dosya aktarýmý
için kullanýlabilir. Pek çok uç birim programý (örneðin minicom) dosya
taþýmak için bu programlarý kullanýr.

%prep
%setup -q

%build
export CFLAGS+=" -fPIE -Wno-error=implicit-int -Wno-error=implicit-function-declaration -Wno-error=incompatible-pointer-types"
export LDFLAGS+=" -pie"
%configure --program-transform-name=s/l//
make

%install
%makeinstall

%files
%license COPYING
%defattr(-,root,root)
#%doc AUTHORS COMPATABILITY ChangeLog NEWS README README.gettext TODO THANKS README.cvs README.isdn4linux README.tests
%{_bindir}/sz
%{_bindir}/sb
%{_bindir}/sx
%{_bindir}/rz
%{_bindir}/rb
%{_bindir}/rx
%exclude %{_mandir}/man1/sz.1.gz
%exclude %{_mandir}/man1/rz.1.gz
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/lrzsz.mo


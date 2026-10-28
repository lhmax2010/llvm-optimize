Name: prebuilt-tizensdk
Summary: Tizen Application Development Environment
Version: 0.0.1
Release: 1
Group: Development/Tools
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
AutoReqProv: no

Requires: jdk
Requires: native-dev-rootstrap

%define debug_package %{nil}

%description
%{summary} for Tizen Application Build.

%prep
%setup -q

%build
#Nothing to build. Just copy files.

%clean
rm -rf %{buildroot}

%install
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/usr/tizen-studio
install -d %{buildroot}/usr/tizen-studio-data
cp -rf tizen-studio/* %{buildroot}/usr/tizen-studio
cp -rf tizen-studio-data/* %{buildroot}/usr/tizen-studio-data
ln -sf /usr/tizen-studio/tools/ide/bin/tizen %{buildroot}/%{_bindir}
ln -sf /usr/tizen-studio/tools/ide/bin/tizen.sh %{buildroot}/%{_bindir}
#ln -sf /usr/tizen-studio/jdk/bin/java %{buildroot}/%{_bindir}

%files
%attr(755,root,root)
#%{_bindir}/java
%{_bindir}/tizen
%{_bindir}/tizen.sh
/usr/tizen-studio
/usr/tizen-studio-data
%exclude /usr/lib/debug/usr/tizen-studio/jdk/bin/*.debug
%attr(777,root,root) /usr/tizen-studio-data/cli/logs
%attr(777,root,root) /usr/tizen-studio/tools/.tizen-cli-config

%post
ln -sf ../../opt/usr/data/platforms /usr/tizen-studio/platforms
cp ../../opt/usr/data/tools/smart-build-interface/plugins/* /usr/tizen-studio/tools/smart-build-interface/plugins/


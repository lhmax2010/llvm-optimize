Name:           wireless-regdb
Version:        2013.01.11
Release:        0
License:        ISC
Summary:        Linux wireless regulatory database
Url:            http://wireless.kernel.org/en/developers/Regulatory/
Group:          System/Base
Source:         http://wireless.kernel.org/download/wireless-regdb/wireless-regdb-%{version}.tar.xz
Source1001: 	wireless-regdb.manifest

%define crda_lib /usr/lib/crda

%description
This package contains the wireless regulatory database used by all
cfg80211 based Linux wireless drivers. The wireless database being
used is maintained by John Linville, the Linux wireless kernel maintainer
http://wireless.kernel.org/en/developers/Regulatory/

%prep
%setup -q
cp %{SOURCE1001} .

%build

%install
install -m 755 -d %{buildroot}/%crda_lib
install -m 644 regulatory.bin %{buildroot}/%{crda_lib}/regulatory.bin
%files
%manifest %{name}.manifest
%crda_lib/regulatory.bin
%license LICENSE

%changelog

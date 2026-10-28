Name:       	firmware-update-system-ui
Summary:    	firmware-update-system-ui
ExclusiveArch:	%{arm} aarch64 riscv64
Version:    	1.2.15
Release:    	0
Group:      	System
License:    	Apache-2.0
Source0:    	%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest

BuildRequires:	cmake
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(libtdm)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(cairo)

%description
Fota update app


##### pkg-wearable
%package wearable
Summary: TOTA update GUI for wearable targets
Requires: %{name} = %{version}-%{release}
Conflicts: %{name}-common
%description wearable
TOTA update GUI for wearable targets


%package common
Summary: TOTA update GUI for common targets
Requires: %{name} = %{version}-%{release}
Conflicts: %{name}-wearable
%description common
TOTA update GUI for common targets, ex. rpi3


%prep
%setup -q
cp %{SOURCE1001} .

%build
export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_prefix}/lib -Wl,--as-needed"
LDFLAGS="$LDFLAGS"

%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DHAL_LIBDIR=%{_hal_libdir}

make %{?jobs:-j%jobs}

%install
%make_install
mkdir -p %{buildroot}%{_datadir}/initrd-recovery/initrd.list.d
cp 42-tota-gui-wearable.list %{buildroot}%{_datadir}/initrd-recovery/initrd.list.d/
cp 42-tota-gui-common.list %{buildroot}%{_datadir}/initrd-recovery/initrd.list.d/

%post wearable
mv %{_bindir}/fota_gui_wearable %{_bindir}/fota_gui
mv %{_bindir}/rw-update-ani-wearable %{_bindir}/rw-update-ani
mv %{_datadir}/fota/res/images_wearable/images %{_datadir}/fota/res/images
mv %{_prefix}/share/rw-updater/res/images_wearable/images %{_prefix}/share/rw-updater/res/images
mv %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-wearable.list %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui.list

%post common
mv %{_bindir}/fota_gui_common %{_bindir}/fota_gui
mv %{_bindir}/rw-update-ani-common %{_bindir}/rw-update-ani
mv %{_bindir}/recovery_gui_common %{_bindir}/system-recovery_gui
mkdir -p %{_datadir}/res
mv %{_datadir}/fota/res/images_common/images %{_datadir}/res/images
mv %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-common.list %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui.list


%preun wearable
mv %{_bindir}/fota_gui %{_bindir}/fota_gui_wearable
mv %{_bindir}/rw-update-ani %{_bindir}/rw-update-ani-wearable
mv %{_datadir}/fota/res/images %{_datadir}/fota/res/images_wearable
mv %{_prefix}/share/rw-updater/res/images %{_prefix}/share/rw-updater/res/images_wearable
mv %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui.list %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-wearable.list

%preun common
mv %{_bindir}/fota_gui %{_bindir}/fota_gui_common
mv %{_bindir}/rw-update-ani %{_bindir}/rw-update-ani-common
mv %{_bindir}/system-recovery_gui %{_bindir}/recovery_gui_common
mv %{_datadir}/res/images %{_datadir}/fota/res/images_common
mv %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui.list %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-common.list


%files
%license LICENSE.APLv2
%manifest firmware-update-system-ui.manifest
%defattr(-,root,root,-)

%files wearable
%license LICENSE.APLv2
%manifest firmware-update-system-ui.manifest
%defattr(-,root,root,-)
%attr(700,-,-) %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-wearable.list
%{_datadir}/fota/res/images_wearable
%{_bindir}/fota_gui_wearable
%attr(550,system,system_share) %{_bindir}/rw-update-ani-wearable
%{_prefix}/share/rw-updater/res/images_wearable

%files common
%license LICENSE.APLv2
%manifest firmware-update-system-ui.manifest
%defattr(-,root,root,-)
%attr(700,-,-) %{_datadir}/initrd-recovery/initrd.list.d/42-tota-gui-common.list
%{_datadir}/fota/res/images_common
%{_bindir}/fota_gui_common
%{_bindir}/recovery_gui_common
%attr(550,system,system_share) %{_bindir}/rw-update-ani-common

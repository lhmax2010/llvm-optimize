%define TARGET_VIM3 tizen-khadas-vim3
%define TARGET_VIM3L tizen-khadas-vim3l
%define TARGET_ODROID_N2 tizen-odroid-n2
%define TARGET_ODROID_C4 tizen-odroid-c4

Name: u-boot-amlogic
Version: 2025.10
Release: 0
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
ExclusiveArch: aarch64
URL: https://source.denx.de/u-boot/u-boot.git
Source0: u-boot-%{version}.tar.bz2
Source1001: u_boot_amlogic.manifest

BuildRequires: gcc >= 6.0
BuildRequires: bc
BuildRequires: flex
BuildRequires: bison
BuildRequires: pkgconfig(openssl3)

%description
u-boot - Tizen bootloader for Embedded boards based on ARM processor

%package -n u-boot-amlogic-common
Summary: U-boot Amlogic Common Files
Group: System/Kernel
License: GPL-2.0+

%description -n u-boot-amlogic-common
u-boot-amlogic-common - Tizen Amlogic Boot Script, Tizen Logo Image, and common files

%package -n u-boot-c4
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
Requires: u-boot-amlogic-common

%description -n u-boot-c4
u-boot-c4 - Tizen bootloader for Embedded boards based on ARM processor

%package -n u-boot-n2
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
Requires: u-boot-amlogic-common

%description -n u-boot-n2
u-boot-n2 - Tizen bootloader for Embedded boards based on ARM processor

%package -n u-boot-vim3
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
Requires: u-boot-amlogic-common

%description -n u-boot-vim3
u-boot-vim3 - Tizen bootloader for Embedded boards based on ARM processor

%package -n u-boot-vim3l
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
Requires: u-boot-amlogic-common

%description -n u-boot-vim3l
u-boot-vim3l - Tizen bootloader for Embedded boards based on ARM processor

%define TARGETS %{TARGET_VIM3} %{TARGET_VIM3L} %{TARGET_ODROID_N2} %{TARGET_ODROID_C4}

%prep
%setup -q -n u-boot-%{version}

%build
%{?asan:/usr/bin/gcc-unforce-options}
cp %{SOURCE1001} .

for i in %{TARGETS}; do
	target=$i
	case $target in
	tizen-odroid-n2)
		FIP=fip/n2
		ENCRYPT=fip/aml_encrypt_g12b
		OUTPUT_BIN=u-boot-n2.bin
		PARAMS=params-n2.bin
	;;
	tizen-odroid-c4)
		FIP=fip/c4
		ENCRYPT=fip/aml_encrypt_g12a
		OUTPUT_BIN=u-boot-c4.bin
		PARAMS=params-c4.bin
	;;
	tizen-khadas-vim3)
		FIP=fip/kvim3
		ENCRYPT=fip/aml_encrypt_g12b
		OUTPUT_BIN=u-boot-vim3.bin
		PARAMS=params-vim3.bin
	;;
	tizen-khadas-vim3l)
		FIP=fip/kvim3l
		ENCRYPT=fip/aml_encrypt_g12a
		OUTPUT_BIN=u-boot-vim3l.bin
		PARAMS=params-vim3l.bin
	;;
	esac
	# Make directory
	mkdir -p %{_builddir}/${target}

	## 1. Build ##
	# 1-0. Clean
	make mrproper

	# 1-2. Set configuration
	make ${target}_defconfig

	# 1-3. Build tools
	make %{?_smp_mflags} HOSTCC="%{__cc} $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true tools

	make HOSTCC="%{__cc} $RPM_OPT_FLAGS" envtools

	# 1-4. Build u-boot
	export PATH="$PATH:tools:"
	make %{?_smp_mflags} EXTRAVERSION=`echo %{vcs} | sed 's/.*u-boot.*#\(.\{9\}\).*/-g\1-TIZEN.org/'`

	# 1-5. Encryption
	chmod +x ${ENCRYPT}
	${ENCRYPT} --bl3sig --input u-boot.bin --compress lz4 \
					--output ${FIP}/bl33.bin.enc \
					--level v3 --type bl33 --compress lz4
	${ENCRYPT} --bootmk \
		--output %{_builddir}/${target}/${OUTPUT_BIN} \
		--bl2 ${FIP}/bl2.n.bin.sig \
		--bl30 ${FIP}/bl30_new.bin.enc \
		--bl31 ${FIP}/bl31.img.enc \
		--bl33 ${FIP}/bl33.bin.enc \
		--ddrfw1 ${FIP}/ddr4_1d.fw \
		--ddrfw2 ${FIP}/ddr4_2d.fw \
		--ddrfw3 ${FIP}/ddr3_1d.fw \
		--ddrfw4 ${FIP}/piei.fw \
		--ddrfw5 ${FIP}/lpddr4_1d.fw \
		--ddrfw6 ${FIP}/lpddr4_2d.fw \
		--ddrfw7 ${FIP}/diag_lpddr4.fw \
		--ddrfw8 ${FIP}/aml_ddr.fw \
		--level v3

	# 1-6. Generate params.bin
	./scripts/get_default_envs.sh > default_envs.txt
	mkenvimage -s 16384 -o ${PARAMS} default_envs.txt
	rm default_envs.txt
done

# 1-7. Build Boot script
mkimage -A arm64 -T script -C none -n "Tizen Amlogic u-boot helper" -d ./tizen/bootscript/tizen-boot-amlogic-64b.scr ./boot.scr.uimg

%install
rm -rf %{buildroot}

# 2. u-boot installation

mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/var/tmp/u-boot-amlogic
install -d %{buildroot}/var/tmp/u-boot-amlogic

for i in %{TARGETS}; do
	target=$i
	case $target in
	tizen-odroid-n2)
		OUTPUT_BIN=u-boot-n2.bin
		PARAMS=params-n2.bin
	;;
	tizen-odroid-c4)
		OUTPUT_BIN=u-boot-c4.bin
		PARAMS=params-c4.bin
	;;
	tizen-khadas-vim3)
		OUTPUT_BIN=u-boot-vim3.bin
		PARAMS=params-vim3.bin
	;;
	tizen-khadas-vim3l)
		OUTPUT_BIN=u-boot-vim3l.bin
		PARAMS=params-vim3l.bin
	;;
	esac

	install -m 755 %{_builddir}/$target/$OUTPUT_BIN %{buildroot}/var/tmp/u-boot-amlogic
	install -m 755 $PARAMS %{buildroot}/boot
done

install -m 755 boot.scr.uimg %{buildroot}/boot
install -m 755 images/tizen_logo.bmp.gz %{buildroot}/boot

%clean
rm -rf %{_builddir}

%files -n u-boot-amlogic-common
%manifest u_boot_amlogic.manifest
%defattr(-,root,root,-)
/boot/boot.scr.uimg
/boot/tizen_logo.bmp.gz

%files -n u-boot-c4
%manifest u_boot_amlogic.manifest
%defattr(-,root,root,-)
/var/tmp/u-boot-amlogic/u-boot-c4.bin
/boot/params-c4.bin

%files -n u-boot-n2
%manifest u_boot_amlogic.manifest
%defattr(-,root,root,-)
/var/tmp/u-boot-amlogic/u-boot-n2.bin
/boot/params-n2.bin

%files -n u-boot-vim3
%manifest u_boot_amlogic.manifest
%defattr(-,root,root,-)
/var/tmp/u-boot-amlogic/u-boot-vim3.bin
/boot/params-vim3.bin

%files -n u-boot-vim3l
%manifest u_boot_amlogic.manifest
%defattr(-,root,root,-)
/var/tmp/u-boot-amlogic/u-boot-vim3l.bin
/boot/params-vim3l.bin

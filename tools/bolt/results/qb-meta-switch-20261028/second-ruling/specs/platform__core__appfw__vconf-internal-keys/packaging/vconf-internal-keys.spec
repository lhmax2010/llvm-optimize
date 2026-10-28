Name:       vconf-internal-keys
Summary:    Internal shared keys for vconf
Version:    0.0.203
Release:    0
Group:      Application Framework/Configuration
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  xsltproc
BuildRequires:  libxml2-tools
Requires:  vconf
Requires:  coreutils
Requires: tizen-platform-config
Requires: tizen-platform-config-tools

#Requires:  findutils
Requires:  vconf-internal-keys-config

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
configuration internal shared keys

%package devel
Summary:    Vconf internal keys (devel)
Group:      Application Framework/Configuration

%description devel
Vconf internal key header files (devel)

%package config-profile_common
Summary:    Configure vconf internal shared keys for common
Group:      Application Framework/Configuration
Provides:   vconf-internal-keys-config

%description config-profile_common
The vconf-internal-keys configurator for common
Vconf-internal-keys requires one of config-profile_* packages
installed to execute vconf configuration for buxton2.

%package config-profile_tv
Summary:    Configure vconf internal shared keys for tv
Group:      Application Framework/Configuration
Provides:   vconf-internal-keys-config

%description config-profile_tv
The vconf-internal-keys configurator for tv
Vconf-internal-keys requires one of config-profile_* packages
installed to execute vconf configuration for buxton2.

%prep
%setup -q -n %{name}-%{version}

%build

make check

mkdir -p scripts_common
mkdir -p scripts_tv

%ifarch %arm aarch64
make profile=tv model=tv
awk '{ if ($5 == "\"memory\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_memory.txt
awk '{ if ($5 == "\"system\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_system.txt
cp scripts/*.sh scripts_tv/
cp remove_keys.sh scripts_tv/
cp scripts/*.txt scripts_tv/
make clean
make profile=common model=common
awk '{ if ($5 == "\"memory\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_memory.txt
awk '{ if ($5 == "\"system\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_system.txt
cp scripts/*.sh scripts_common/
cp remove_keys.sh scripts_common/
cp scripts/*.txt scripts_common/

%else
make profile=tv model=tv/emulator
awk '{ if ($5 == "\"memory\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_memory.txt
awk '{ if ($5 == "\"system\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_system.txt
cp scripts/*.sh scripts_tv/
cp remove_keys.sh scripts_tv/
cp scripts/*.txt scripts_tv/
make clean
make profile=common model=common/emulator
awk '{ if ($5 == "\"memory\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_memory.txt
awk '{ if ($5 == "\"system\"" ) print $LR }' ./scripts/all.sh | awk '{ print $6}' | sed -e 's/^"//' -e 's/"$//' | sort > ./scripts/vk_system.txt
cp scripts/*.sh scripts_common/
cp remove_keys.sh scripts_common/
cp scripts/*.txt scripts_common/
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DCMAKE_LIBDIR=%{_libdir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}
mkdir -p %{buildroot}/opt/usr
mkdir -p %{buildroot}/opt/usr/vconf-internal-keys_scripts_common
mkdir -p %{buildroot}/opt/usr/vconf-internal-keys_scripts_tv
install -m 755 scripts_tv/*.sh %{buildroot}/opt/usr/vconf-internal-keys_scripts_tv
install scripts_tv/*.txt %{buildroot}/opt/usr/vconf-internal-keys_scripts_tv
install -m 755 scripts_common/*.sh %{buildroot}/opt/usr/vconf-internal-keys_scripts_common
install scripts_common/*.txt %{buildroot}/opt/usr/vconf-internal-keys_scripts_common

mkdir -p %{buildroot}/usr/include/vconf
install -m 644 include/*.h %{buildroot}/usr/include/vconf

%make_install

%post
/sbin/ldconfig

TMP=/opt/.installing_vconf_internal_keys
TMP_AFTER=/opt/.runtime_vconf_internal_keys

touch $TMP

filelist="/opt/usr/all.sh"
for file in $filelist ; do
	echo "running ---------------------------------------------------- $file"
	if [ -e $file ]
	then
		chmod a+x $file
		. $file
		rm $file
	fi
done

#filelist=`find /opt/usr -name "vconf-internal-*.sh"`
filelist=`ls /opt/usr/vconf-internal-*.sh 2>/dev/null`
for file in $filelist
do
	chmod a+x "$file"
	#/bin/sh "$file"
	echo "running ---------------------------------------------------- $file"
	. "$file"
	rm "$file"
done

rm $TMP

%postun -p /sbin/ldconfig

%post config-profile_common
cp /opt/usr/vconf-internal-keys_scripts_common/*.sh /opt/usr/
cp /opt/usr/vconf-internal-keys_scripts_common/*.txt /opt/usr/
rm -rf /opt/usr/vconf-internal-keys_scripts_common

%post config-profile_tv
cp /opt/usr/vconf-internal-keys_scripts_tv/*.sh /opt/usr/
cp /opt/usr/vconf-internal-keys_scripts_tv/*.txt /opt/usr/
rm -rf /opt/usr/vconf-internal-keys_scripts_tv

%posttrans config-profile_common
TMP_AFTER=/opt/.runtime_vconf_internal_keys
echo "running -------------------- DISABLE remove_keys.sh"
. /opt/usr/remove_keys.sh msg		# just print out messages
#. /opt/usr/remove_keys.sh del		# remove the actual keys
touch $TMP_AFTER

# remove script remove_keys.sh and intermediate files created during the script
rm /opt/usr/remove_keys.sh
rm /opt/usr/bk_memory.txt
rm /opt/usr/bk_system.txt
rm /opt/usr/vk_memory.txt
rm /opt/usr/vk_system.txt

%posttrans config-profile_tv
TMP_AFTER=/opt/.runtime_vconf_internal_keys
echo "running -------------------- DISABLE remove_keys.sh"
. /opt/usr/remove_keys.sh msg		# just print out messages
#. /opt/usr/remove_keys.sh del		# remove the actual keys
touch $TMP_AFTER

# remove script remove_keys.sh and intermediate files created during the script
rm /opt/usr/remove_keys.sh
rm /opt/usr/bk_memory.txt
rm /opt/usr/bk_system.txt
rm /opt/usr/vk_memory.txt
rm /opt/usr/vk_system.txt

%files
%license LICENSE

%files devel
%defattr(-,root,root,-)
/usr/include/vconf/*.h
%{_libdir}/pkgconfig/*.pc

%files config-profile_common
/opt/usr/vconf-internal-keys_scripts_common/*.sh
/opt/usr/vconf-internal-keys_scripts_common/*.txt
%license LICENSE

%files config-profile_tv
/opt/usr/vconf-internal-keys_scripts_tv/*.sh
/opt/usr/vconf-internal-keys_scripts_tv/*.txt
%license LICENSE

%if %{defined profile}
%define _profile %profile
%else
%define _profile base
%endif

%if "%{?profile}" == "mobile" || "%{?profile}" == "wearable" || "%{?profile}"=="tv" || "%{?profile}" == "ivi" || "%{?profile}" == "common"
%define _with_legacy_imageconfig 1
%endif
%bcond_with legacy_imageconfig

%define baseline tizen-3.0

Summary:	Create kickstart files for Tizen images
Name:		image-configurations
Version:	102
Release:	1
License:	GPL-2.0
Group:		System/Configuration
URL:		http://www.tizen.org
Source:		image-configurations-%{version}.tar.bz2
Source1001: 	image-configurations.manifest

BuildArch:	noarch
BuildRequires:  kickstarter >= 0.15
BuildRequires:  meta-generic
%if %{with legacy_imageconfig}
BuildRequires:  meta-%{_profile}
%else
BuildRequires:	meta-common
%endif
BuildRequires:  package-groups
BuildRequires:  python

%description
Create Configuration files to build Tizen images

%prep
%setup -q
cp %{SOURCE1001} .


%build

# merge the configuration files from generic and the current profile
# in the same input dir to make kickstarter aware of the generic scripts.
%if %{with legacy_imageconfig}
mkdir -p input
for profile in generic %_profile; do
    pdir=%{_datadir}/image-configurations/$profile
    [ -d $pdir ] && cp -a $pdir/* input/
done

pdir=%{_datadir}/package-groups
[ -d "$pdir" ] && cp "$pdir/group.xml" input/

kickstarter -c input/%_profile.yaml \
    -e input/configs \
    -r input/%_profile-repos.yaml \
    -T input/%_profile-targets.yaml \
    -t %{_repository} \
    -i image-configs.xml
%else
echo "<image-configs>" > image-configs.xml
for profile in common; do
    mkdir -p input-$profile
    for pn in generic $profile; do
        pdir=%{_datadir}/image-configurations/$pn
        [ -d $pdir ] && cp -a $pdir/* input-$profile/
    done

    kickstarter -c input-$profile/$profile.yaml \
        -e input-$profile/configs \
        -r input-$profile/$profile-repos.yaml \
        -T input-$profile/$profile-targets.yaml \
        -t %{_repository} \
        -i image-configs_$profile.xml

    cat image-configs_$profile.xml | sed 's/<image-configs>//g' |sed 's/<\/image-configs>//g' >> image-configs.xml
done
echo "</image-configs>" >> image-configs.xml

# copy groups.xml file to input for convert_ks.py
mkdir -p input
pdir=%{_datadir}/package-groups
[ -d "$pdir" ] && cp "$pdir/group.xml" input/
%endif

%install

mkdir -p %{buildroot}/usr/share/image-configurations
[ -n "$(ls -A %{baseline}/*.ks 2>/dev/null)" ] &&  cp %{baseline}/*.ks %{buildroot}/usr/share/image-configurations
cp image-configs.xml %{buildroot}/usr/share/image-configurations

[ -d %{buildroot}/usr/share/image-configurations ] && for ksfile in $(ls -A %{buildroot}/usr/share/image-configurations/*.ks 2>/dev/null)
do
    %{__python} convert_ks.py "${ksfile}" input/group.xml
    chmod go+r "${ksfile}"
done

%files
%manifest %{name}.manifest
#%dir %_datadir/image-configurations
%_datadir/image-configurations/*

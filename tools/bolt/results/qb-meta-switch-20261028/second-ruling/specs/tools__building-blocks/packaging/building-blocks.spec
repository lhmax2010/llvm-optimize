# There are meta packages only.
%define __debug_install_post %{nil}
%define debug_package %{nil}
%define tizen_feature() sed -i 's#\\\(\\\"%{1}\\\".\\\+>\\\).\\\+\\\(</key>\\\)#\\\1%{2}\\\2#' %{_sysconfdir}/config/model-config.xml;
%define tizen_hal_feature() sed -i 's#\\\(\\\"%{1}\\\".\\\+>\\\).\\\+\\\(</key>\\\)#\\\1%{2}\\\2#' %{_hal_sysconfdir}/config/model-config.xml;

%global dotnet_feature "on"

Name:		building-blocks
Version:	11.0.0
Release:	0
License:	Apache-2.0
Summary:	The Root of All Tizen Meta Packages (building blocks)
Url:		http://tizen.org
Group:		Meta
Source0:	%{name}-%{version}.tar.gz

# Domains are rearranged by API sets according to developer.tizen.org
Source1200:	domain-apis.inc
Source1201:	domain-apis-account.inc
Source1202:	domain-apis-appfw.inc
Source1203:	domain-apis-base.inc
Source1204:	domain-apis-content.inc
Source1205:	domain-apis-context.inc
Source1206:	domain-apis-location.inc
Source1208:	domain-apis-messaging.inc
Source1209:	domain-apis-multimedia.inc
Source1210:	domain-apis-network.inc
Source1211:	domain-apis-security.inc
Source1212:	domain-apis-social.inc
Source1213:	domain-apis-system.inc
Source1214:	domain-apis-telephony.inc
Source1215:	domain-apis-ui.inc
Source1216:	domain-apis-uix.inc
Source1217:	domain-apis-web.inc
Source1218:	domain-apis-machinelearning.inc

Source1300: domain-features.inc
Source1301: domain-features-dotnet.inc
Source1302: domain-features-webapi.inc
Source1303: domain-features-esplusplayer.inc
Source1304: domain-features-bootanimation.inc
Source1305: domain-features-starter.inc
Source1306: domain-features-upgrade.inc
Source1307: domain-features-tool_and_locale.inc
Source1308: domain-features-recovery.inc
Source1309: domain-features-setup.inc
Source1310: domain-features-resource_manager.inc
Source1311: domain-features-diagnostics.inc
Source1312: domain-features-power_manager.inc
Source1314: domain-features-resource_monitor.inc
Source1315: domain-features-isu.inc
Source1316: domain-features-kdbus.inc
Source1317: domain-features-rscmgr_service.inc


%if %{dotnet_feature} == "on"
Source1400:	domain-csapis.inc
Source1401:	domain-csapis-account.inc
Source1402:	domain-csapis-appfw.inc
Source1403:	domain-csapis-content.inc
Source1404:	domain-csapis-context.inc
Source1405:	domain-csapis-location.inc
Source1407:	domain-csapis-messaging.inc
Source1408:	domain-csapis-multimedia.inc
Source1409:	domain-csapis-network.inc
Source1410:	domain-csapis-security.inc
Source1411:	domain-csapis-social.inc
Source1412:	domain-csapis-system.inc
Source1413:	domain-csapis-telephony.inc
Source1414:	domain-csapis-ui.inc
Source1415:	domain-csapis-uix.inc
Source1417:	domain-csapis-machinelearning.inc
%endif

Source1500:	domain-halapis.inc

Source2010:	epicfeature-development.inc
Source2020:	epicfeature-application.inc

Source3500:	platform-preset-iot.inc
Source3501:	platform-preset-iot-headless-images.inc
Source3502:	platform-preset-iot-headed-images.inc
Source3503:	platform-preset-partitions.inc

Source3800:	platform-preset-boards.inc
%ifarch %{arm} aarch64
Source3815:	platform-preset-boards-rpi4-hal-backend.inc
Source3816:	platform-preset-boards-generic-hal-backend.inc
Source3820:	platform-preset-boards-common.inc
Source3813:	platform-preset-boards-vim3-hal-backend.inc
%endif
%ifarch riscv64
Source3815:	platform-preset-boards-visionfive2-hal-backend.inc
Source3816:	platform-preset-boards-generic-hal-backend.inc
Source3817:	platform-preset-boards-bpif3-hal-backend.inc
Source3818:	platform-preset-boards-lpi4a-hal-backend.inc
Source3820:	platform-preset-boards-common.inc
%endif
%ifarch armv7l
Source3812:	platform-preset-boards-artik530-hal-backend.inc
%endif
%ifarch aarch64
Source3814:	platform-preset-boards-c4-hal-backend.inc
Source3819:	platform-preset-boards-rubikpi3-hal-backend.inc
Source3821:	platform-preset-boards-orinnano-hal-backend.inc
%endif
%ifarch %{ix86} x86_64
Source3803: platform-preset-boards-emul.inc
%endif

# To get .ks files
BuildRequires:	image-configurations

# To check the rules
BuildRequires:	python

# Root Categories
Suggests:	%{name}-category-domains
Suggests:	%{name}-category-epicfeatures
Suggests:	%{name}-category-Presets

%description
The root of all Tizen building block meta packages.
Every root-level Tizen building block should be included by this.
Any "minimal" required packages should be somehow (directly or indirectly)
required (included) by this package.
In Tizen building blocks,
"Requires" means mandatory package.
"Suggests" means optional package.
"Recommends" is reserved for future usage.
"Conflicts" is to unselect unconditionally.


%package	category-domains
Summary:	Tizen Techinical Domains
Suggests:	%{name}-root-domain_API
Suggests:   %{name}-root-domain_Feature
%if %{dotnet_feature} == "on"
Suggests:	%{name}-root-domain_CSAPI
%endif
#Suggests:	%{name}-root-domain_WebAPI
Suggests:	%{name}-root-domain_HALAPI
%description	category-domains
This meta package lists all Tizen blocks (meta packages) designating
technical domains.
%files		category-domains
# Intentionally empty


%package	category-epicfeatures
Summary:	Tizen Major Features
Suggests:	%{name}-root-feature_Development
Suggests:	%{name}-root-feature_App
%description	category-epicfeatures
This meta package lists all Tizen blocks (meta packages) designating
major features that are supposed to be orthogonal to each other
and to most domains.
%files		category-epicfeatures
# Intentionally empty


%package	category-Preset
Summary:	Tizen Presets
Suggests:	%{name}-root-Preset_boards
Suggests:	%{name}-root-Preset_iot_core
Suggests:	%{name}-root-Preset_iot_headed
Suggests:	%{name}-root-Preset_iot_headless
Suggests:	%{name}-root-Preset_img_headless
Suggests:	%{name}-root-Preset_img_headed
Suggests:	%{name}-root-Preset_partition
%description	category-Preset
This meta pacakge lists all Tizen blocks (meta packages) designating
Tizen platform presets, HAL/device-support presets, and
presets describing specific products.
%files		category-Preset
# Intentionally empty


# Do not try to include files unless RPMBUILD has already expanded source files to SOURCES
# Use Source1001 (domain-kernel) as the probing point.
%define include_if_mainbuild() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then print("%include "..rpm.expand("%{1}").." ") end}}

# Create a target device preset from .ks file used to create device iamge.
# This script writes build-spec when building the build-spec itself. :)
# Importing .ks file with list_with_require() based on image-configuration will work
# after Tizen:Unified starts to generate its own platform images.
%define list_with_require() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then \
	local start = 0 \
	if posix.access(rpm.expand("%{1}")) then \
		for line in io.lines(rpm.expand("%{1}")) do \
			if (string.match(line, '%%end')) then break end \
			if (string.match(line, '%%packages')) then \
				start = 1 \
			else \
				if (start == 1) then \
					if (string.match(line, '#')) then \
					elseif (string.sub(line, 1, 1) == '-') then \
					elseif (string.len(line) == 0) then\
					else \
						print("Requires: "..line) \
						print("\\n") \
					end \
				end \
			end \
		end \
	else \
		print("Requires: CANNOT_FIND_REQUIRED_FILES\\n") \
	end \
end}}

# Create a target device preset from .ks file used to create device iamge.
# This script writes build-spec when building the build-spec itself. :)
# Importing .ks file with list_with_require() based on image-configuration will work
# after Tizen:Unified starts to generate its own platform images.
# Removing the target-dependent files.
%define list_with_require_nodep_device() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then \
	local start = 0 \
	if posix.access(rpm.expand("%{1}")) then \
		for line in io.lines(rpm.expand("%{1}")) do \
			if (string.match(line, '%%end')) then break end \
			if (string.match(line, '%%packages')) then \
				start = 1 \
			else \
				if (start == 1) then \
					if (string.match(line, '#')) then \
					elseif (string.sub(line, 1, 1) == '-') then \
					elseif (string.len(line) == 0) then\
					elseif (string.match(line,"model%-config")) then\
					elseif (string.match(line,"pepper")) then\
					elseif (string.match(line,"system%-plugin")) then\
					elseif (string.match(line,"vconf%-internal%-keys%-config%-profile")) then\
					else \
						print("Requires: "..line) \
						print("\\n") \
					end \
				end \
			end \
		end \
	else \
		print("Requires: CANNOT_FIND_REQUIRED_FILES\\n") \
	end \
end}}


# Create Suggests List of blocks with yaml file list
# DIRECTORY, Prefix-To-Be-Removed, Prefix-for-block-name
%define list_suggest() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then \
	for f in posix.files(rpm.expand("%{1}")) do \
		local line =  string.sub(f, string.len(rpm.expand("%{2}"))+2) \
		local prefix = string.sub(f, 1, string.len(rpm.expand("%{2}"))) \
		if (string.sub(line, 1, 10) == 'adaptation') then \
		elseif (string.sub(line, 1, 4) == 'boot') then \
		elseif (prefix == rpm.expand("%{2}")) then \
			line = string.gsub(line, "-", "_")
			print("Suggests: %{name}-"..rpm.expand("%{3}").."zblock_"..line) \
			print("\\n") \
		end \
	end \
end}}


# Requires the created suggests list of blocks with yaml file list
# DIRECTORY, Prefix-To-Be-Removed, Prefix-for-block-name
%define list_suggest_linkreq() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then \
	for f in posix.files(rpm.expand("%{1}")) do \
		local line =  string.sub(f, string.len(rpm.expand("%{2}"))+2) \
		local prefix = string.sub(f, 1, string.len(rpm.expand("%{2}"))) \
		if (string.sub(line, 1, 10) == 'adaptation') then \
		elseif (string.sub(line, 1, 4) == 'boot') then \
		elseif (prefix == rpm.expand("%{2}")) then \
			line = string.gsub(line, "-", "_")
			print("Requires: %{name}-"..rpm.expand("%{3}").."zblock_"..line) \
			print("\\n") \
		end \
	end \
end}}


# Create Requires List of packages for all blocks with yaml file list
# DIRECTORY, Prefix-To-Be-Removed, Prefix-for-block-name
%define list_require() %{expand:%{lua:if posix.access(rpm.expand("%{SOURCE1200}"), "f") then \
	for f in posix.files(rpm.expand("%{1}")) do \
		local line =  string.sub(f, string.len(rpm.expand("%{2}"))+2) \
		local prefix = string.sub(f, 1, string.len(rpm.expand("%{2}"))) \
		if (string.sub(line, 1, 10) == 'adaptation') then \
		elseif (string.sub(line, 1, 4) == 'boot') then \
		elseif (prefix == rpm.expand("%{2}")) then \
			local pkg = rpm.expand("%{3}").."zblock_"..string.gsub(line, "-", "_") \
			local summary_available = 0 \
			local filename = rpm.expand("%{1}").."/"..f \
			print("\\n") \
			print("%package "..pkg.."\\n") \
			if posix.access(filename) then \
				for tag in io.lines(filename) do \
					if (string.sub(tag, 1, 8) == "Summary:") then \
						print(tag) \
						print("\\n") \
						summary_available = 1 \
						break \
					end \
				end \
			end \
			if (summary_available == 0) then \
				print("Summary: "..f) \
				print("\\n") \
			end \
			if posix.access(filename) then \
				for line in io.lines(rpm.expand("%{1}").."/"..f) do \
					if (string.match(line, 'Packages:')) then \
						start = 1 \
					elseif (string.sub(line, 1, 2) == '- ') then \
						if (start == 1) then \
							print("Requires: "..string.sub(line, 3)) \
							print("\\n") \
						end \
					elseif (string.sub(line, 1, 1) == '#') then \
					elseif (string.len(line) == 0) then \
					else \
						start = 0
					end \
				end \
			else \
				print("Requires: CANNOT_FIND_REQUIRED_FILES\\n") \
			end \
			print("%description "..pkg.."\\n") \
			print("Auto Generated Block (zblock) of "..f.."\\n") \
			print("%files "..pkg.."\\n") \
			print("\\n\\n\\n") \
		end \
	end \
end}}

%prep
%setup

%build

# Auto require generation still requires further decision making. This shows the basic data for it in the build log.
ls -l %{_datadir}/image-configurations/*

mkdir -p %{buildroot}/opt/share/bb
cp -f mapping*.xml %{buildroot}/opt/share/bb
cp -f make_tizenfx_from_bb.sh %{buildroot}/opt/share/bb
cp -f make_ABB_tag.sh %{buildroot}/opt/share/bb

# rule_checker returns non-zero if there is an error in *.inc, breaking the build
%{__python} ./rule_checker.py

%files

############## DOMAINS ##################
%{include_if_mainbuild %{SOURCE1200}}
%{include_if_mainbuild %{SOURCE1201}}
%{include_if_mainbuild %{SOURCE1202}}
%{include_if_mainbuild %{SOURCE1203}}
%{include_if_mainbuild %{SOURCE1204}}
%{include_if_mainbuild %{SOURCE1205}}
%{include_if_mainbuild %{SOURCE1206}}
%{include_if_mainbuild %{SOURCE1208}}
%{include_if_mainbuild %{SOURCE1209}}
%{include_if_mainbuild %{SOURCE1210}}
%{include_if_mainbuild %{SOURCE1211}}
%{include_if_mainbuild %{SOURCE1212}}
%{include_if_mainbuild %{SOURCE1213}}
%{include_if_mainbuild %{SOURCE1214}}
%{include_if_mainbuild %{SOURCE1215}}
%{include_if_mainbuild %{SOURCE1216}}
%{include_if_mainbuild %{SOURCE1217}}
%{include_if_mainbuild %{SOURCE1218}}

%{include_if_mainbuild %{SOURCE1300}}
%{include_if_mainbuild %{SOURCE1301}}
%{include_if_mainbuild %{SOURCE1302}}
%{include_if_mainbuild %{SOURCE1303}}
%{include_if_mainbuild %{SOURCE1304}}
%{include_if_mainbuild %{SOURCE1305}}
%{include_if_mainbuild %{SOURCE1306}}
%{include_if_mainbuild %{SOURCE1307}}
%{include_if_mainbuild %{SOURCE1308}}
%{include_if_mainbuild %{SOURCE1309}}
%{include_if_mainbuild %{SOURCE1310}}
%{include_if_mainbuild %{SOURCE1311}}
%{include_if_mainbuild %{SOURCE1312}}
%{include_if_mainbuild %{SOURCE1314}}
%{include_if_mainbuild %{SOURCE1315}}
%{include_if_mainbuild %{SOURCE1316}}
%{include_if_mainbuild %{SOURCE1317}}

%if %{dotnet_feature} == "on"
%{include_if_mainbuild %{SOURCE1400}}
%{include_if_mainbuild %{SOURCE1401}}
%{include_if_mainbuild %{SOURCE1402}}
%{include_if_mainbuild %{SOURCE1403}}
%{include_if_mainbuild %{SOURCE1404}}
%{include_if_mainbuild %{SOURCE1405}}
%{include_if_mainbuild %{SOURCE1407}}
%{include_if_mainbuild %{SOURCE1408}}
%{include_if_mainbuild %{SOURCE1409}}
%{include_if_mainbuild %{SOURCE1410}}
%{include_if_mainbuild %{SOURCE1411}}
%{include_if_mainbuild %{SOURCE1412}}
%{include_if_mainbuild %{SOURCE1413}}
%{include_if_mainbuild %{SOURCE1414}}
%{include_if_mainbuild %{SOURCE1415}}
%{include_if_mainbuild %{SOURCE1417}}
%endif

%{include_if_mainbuild %{SOURCE1500}}
############## EPIC FEATURES ######################

# Dev tools
%{include_if_mainbuild %{SOURCE2010}}

# Platform features
%{include_if_mainbuild %{SOURCE2020}}


############# PLATFORM PRESET #####################

# Tizen Platform Presets.
# Unlike Preset-Recipes of TIC, you cannot deselect packages from these presets.
%{include_if_mainbuild %{SOURCE3500}}
%{include_if_mainbuild %{SOURCE3501}}
%{include_if_mainbuild %{SOURCE3502}}
%{include_if_mainbuild %{SOURCE3503}}

%{include_if_mainbuild %{SOURCE3800}}
%ifarch %{arm} aarch64
%{include_if_mainbuild %{SOURCE3815}}
%{include_if_mainbuild %{SOURCE3816}}
%{include_if_mainbuild %{SOURCE3820}}
%{include_if_mainbuild %{SOURCE3813}}
%endif
%ifarch riscv64
%{include_if_mainbuild %{SOURCE3815}}
%{include_if_mainbuild %{SOURCE3816}}
%{include_if_mainbuild %{SOURCE3817}}
%{include_if_mainbuild %{SOURCE3818}}
%{include_if_mainbuild %{SOURCE3820}}
%endif
%ifarch armv7l
%{include_if_mainbuild %{SOURCE3812}}
%endif
%ifarch aarch64
%{include_if_mainbuild %{SOURCE3814}}
%{include_if_mainbuild %{SOURCE3819}}
%{include_if_mainbuild %{SOURCE3821}}
%endif
%ifarch %{ix86} x86_64
%{include_if_mainbuild %{SOURCE3803}}
%endif
%package	mapping-files
Summary:	Some mapping-files for building-blocks
Requires:	sed
Requires:	rpm
Requires:	grep
Requires:	gawk
%description	mapping-files
This package includes some mapping-files for building-blocks such as tct, rootstrap and tizenfx.
%files		mapping-files
/opt/share/bb/mapping-bb-rs.xml
/opt/share/bb/mapping-bb-tizenfx.xml
/opt/share/bb/mapping-bb-tct.xml
/opt/share/bb/make_tizenfx_from_bb.sh
/opt/share/bb/make_ABB_tag.sh

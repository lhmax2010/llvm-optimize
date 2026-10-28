Name:           docbook_4
VCS:            platform/upstream/docbook_4#b032429cb6ff8f9333b3b7ac7621d4ffb794e829
BuildRequires:  fdupes
BuildRequires:  sgml-skel
BuildRequires:  unzip
Provides:       docbk_4
Provides:       docbook
Provides:       docbook-dtd
Provides:       docbook-dtds
Obsoletes:      docbk_4
Requires:       iso_ent
Requires:       libxml2
%define regcat /usr/bin/sgml-register-catalog
Requires(pre):         %{regcat} /usr/bin/xmlcatalog sgml-skel
Requires(pre):         sed grep awk
Summary:        DocBook DTD Version 4.x
License:        BSD-3-Clause ; MIT
Group:          Productivity/Publishing/DocBook
Version:        4.5
Release:        1.1
Source0:        dummy-%{version}.tar.bz2
Source7:        CATALOG.docbook_4
# DocBook 4.1
Source410:      http://www.oasis-open.org/docbook/sgml/4.1/docbk41.zip
Source411:      http://www.oasis-open.org/docbook/xml/4.1/docbkx412.zip
# No RNG and XSD files for DB4.1
Source414:      CATALOG.db41xml
# DocBook 4.2
Source420:      http://www.oasis-open.org/docbook/sgml/4.2/docbook-4.2.zip
Source421:      http://www.oasis-open.org/docbook/xml/4.2/docbook-xml-4.2.zip
Source422:      http://www.oasis-open.org/docbook/rng/4.2/docbook-rng-4.2.zip
Source423:      http://www.oasis-open.org/docbook/xsd/4.2/docbook-xsd-4.2.zip
Source424:      CATALOG.db42xml
# DocBook 4.3
Source430:      http://www.docbook.org/sgml/4.3/docbook-4.3.zip
Source431:      http://www.docbook.org/xml/4.3/docbook-xml-4.3.zip
Source432:      http://www.docbook.org/rng/4.3/docbook-rng-4.3.zip
Source433:      http://www.docbook.org/xsd/4.3/docbook-xsd-4.3.zip
Source434:      CATALOG.db43xml
# DocBook 4.4
Source440:      http://www.oasis-open.org/docbook/sgml/4.4/docbook-4.4.zip
Source441:      http://www.oasis-open.org/docbook/xml/4.4/docbook-xml-4.4.zip
Source442:      http://www.docbook.org/rng/4.4/docbook-rng-4.4.zip
Source443:      http://www.docbook.org/xsd/4.4/docbook-xsd-4.4.zip
Source444:      CATALOG.db44xml
# DocBook 4.5
Source450:      http://www.oasis-open.org/docbook/sgml/4.5/docbook-4.5.zip
Source451:      http://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip
Source452:      http://www.docbook.org/rng/4.5/docbook-rng-4.5.zip
Source453:      http://www.docbook.org/xsd/4.5/docbook-xsd-4.5.zip
Source454:      CATALOG.db45xml
Source1001: 	docbook_4.manifest
Patch0:         docbook-4-3-cat.diff
Patch1:         docbook-4-3.diff
Patch2:         docbook-4-3-xml-cat.diff
Patch3:         docbook.4.4.dcl.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Url:            http://www.oasis-open.org/docbook/

%description
DocBook is a schema. It is particularly well-suited to books and papers
about computer hardware and software (though it is not limited to these
applications at all). This package has SGML- and XML-DTD versions
included. Some versions of DocBook contain also a RELAX NG and W3C
Schema.

%define INSTALL install -m755 -s
%define INSTALL_DIR install -d -m755
%define INSTALL_DATA install -m644
%define INSTALL_SCRIPT install -m755
%define sgml_dir %{_datadir}/sgml
%define sgml_docbook_dir %{sgml_dir}/docbook
%define sgml_docbook_dtd_dir %{sgml_docbook_dir}/dtd
%define sgml_docbook_custom_dir %{sgml_docbook_dir}/custom
%define sgml_docbook_style_dir %{sgml_docbook_dir}/stylesheet
%define xml_dir %{_datadir}/xml
%define xml_docbook_dir %{xml_dir}/docbook
%define xml_docbook_dtd_dir %{xml_docbook_dir}/schema/dtd
%define xml_docbook_rng_dir %{xml_docbook_dir}/schema/rng
%define xml_docbook_xsd_dir %{xml_docbook_dir}/schema/xsd
%define xml_docbook_custom_dir %{xml_docbook_dir}/custom
%define xml_docbook_style_dir %{xml_docbook_dir}/stylesheet
%define sgml_config_dir /var/lib/sgml
%define sgml_sysconf_dir %{_sysconfdir}/sgml
%define xml_config_dir /var/lib/xml
%define xml_sysconf_dir %{_sysconfdir}/xml

%prep
%setup -n %{name} -c -T
cp %{SOURCE1001} .
mkdir -p dtd/4.1 dtd/4.2 dtd/4.3 dtd/4.4 dtd/4.5 4.1xml 4.2xml 4.3xml 4.4xml 4.5xml
chmod 755 dtd/4.1 dtd/4.2 dtd/4.3 dtd/4.4 dtd/4.5 4.1xml 4.2xml 4.3xml 4.4xml 4.5xml
echo "**** %{S:410}"
cd dtd/4.1; unzip -q -a %{S:410}; cd ../..
cd 4.1xml; unzip -q -a %{S:411}; cd ..
cd dtd/4.2; unzip -q -a %{S:420}; cd ../..
cd 4.2xml; unzip -q -a %{S:421}; cd ..
cd dtd/4.3; unzip -q -a %{S:430}; cd ../..
cd 4.3xml; unzip -q -a %{S:431}; cd ..
cd dtd/4.4
unzip -q -a %{S:440}
%patch3 -p 0
cd ../..
cd 4.4xml; unzip -q -a %{S:441}; cd ..
cd dtd/4.5; unzip -q -a %{S:450}; cd ../..
cd 4.5xml; unzip -q -a %{S:451}; cd ..
%patch -p 1 -P 1 -p 0
%patch2 -p 1
# CATALOG.* files
cp %{S:7} %{S:414} %{S:424} %{S:434} %{S:444} %{S:454} .
chmod -R a+rX,g-w,o-w .
find . -type f | xargs chmod a-x

%build
CATALOG=docbook_41.xml
# # build root catalog fragment
xmlcatbin=/usr/bin/xmlcatalog
"$xmlcatbin" --create --noout "$CATALOG"
docbookdir=%{xml_docbook_dtd_dir}/4.1
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.1.2//EN" \
    "file://$docbookdir/dbpoolx.mod" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.1.2//EN" \
    "file://$docbookdir/docbookx.dtd" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.1.2//EN" \
    "file://$docbookdir/dbcentx.mod" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.1.2//EN" \
    "file://$docbookdir/dbnotnx.mod" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.1.2//EN" \
    "file://$docbookdir/dbgenent.mod" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.1.2//EN" \
    "file://$docbookdir/dbhierx.mod" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "file://$docbookdir/soextblx.dtd" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.1.2//EN" \
    "file://$docbookdir/calstblx.dtd" "$CATALOG"
"$xmlcatbin" --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.1.2" \
    "file://$docbookdir" "$CATALOG"
"$xmlcatbin" --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.1.2" \
    "file://$docbookdir" "$CATALOG"
# === iso
isodir=$docbookdir/ent
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN//XML" \
    "file://$isodir/iso-pub.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN//XML" \
    "file://$isodir/iso-grk1.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN//XML" \
    "file://$isodir/iso-box.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN//XML" \
    "file://$isodir/iso-grk3.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN//XML" \
    "file://$isodir/iso-amsn.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN//XML" \
    "file://$isodir/iso-num.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN//XML" \
    "file://$isodir/iso-grk4.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN//XML" \
    "file://$isodir/iso-dia.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN//XML" \
    "file://$isodir/iso-grk2.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN//XML" \
    "file://$isodir/iso-amsa.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN//XML" \
    "file://$isodir/iso-amso.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN//XML" \
    "file://$isodir/iso-cyr1.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN//XML" \
    "file://$isodir/iso-tech.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN//XML" \
    "file://$isodir/iso-amsc.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN//XML" \
    "file://$isodir/iso-lat1.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN//XML" \
    "file://$isodir/iso-amsb.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN//XML" \
    "file://$isodir/iso-lat2.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN//XML" \
    "file://$isodir/iso-amsr.ent" "$CATALOG"
"$xmlcatbin" --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN//XML" \
    "file://$isodir/iso-cyr2.ent" "$CATALOG"
# ====
%define FOR_ROOT_CAT for-catalog-%{name}-%{version}.xml
CATALOG=etc/xml/$CATALOG
rm -f "%{FOR_ROOT_CAT}.tmp"
"$xmlcatbin" --noout --create "%{FOR_ROOT_CAT}.tmp"
for v in 4.2 4.3 4.4 4.5; do
  cat42=%{xml_docbook_dtd_dir}/$v/catalog.xml
  for s in \
    "-//OASIS//DTD DocBook XML V${v}//EN" \
    "-//OASIS//DTD DocBook CALS Table Model V${v}//EN" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "-//OASIS//ELEMENTS DocBook Information Pool V${v}//EN" \
    "-//OASIS//ELEMENTS DocBook Document Hierarchy V${v}//EN" \
    "-//OASIS//ENTITIES DocBook Additional General Entities V${v}//EN" \
    "-//OASIS//ENTITIES DocBook Notations V${v}//EN" \
    "-//OASIS//ENTITIES DocBook Character Entities V${v}//EN"
   do
   "$xmlcatbin" --noout --add "delegatePublic" "$s" \
     "file://$cat42" "%{FOR_ROOT_CAT}.tmp"
  done
  case "$v" in
    4.[345])
      "$xmlcatbin" --noout --add "delegatePublic" \
         "-//OASIS//ELEMENTS DocBook XML HTML Tables V${v}//EN" \
         "file://$cat42" "%{FOR_ROOT_CAT}.tmp"
      ;;
    *)
      true
  esac
  "$xmlcatbin" --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/xml/${v}" \
    "file://$cat42" "%{FOR_ROOT_CAT}.tmp"
  "$xmlcatbin" --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/xml/${v}" \
    "file://$cat42" "%{FOR_ROOT_CAT}.tmp"
  "$xmlcatbin" --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/${v}" \
    "file://%{xml_docbook_dtd_dir}/${v}" "%{FOR_ROOT_CAT}.tmp"
  "$xmlcatbin" --noout --add "delegatePublic" \
    "ISO 8879:1986" \
    "file:///$CATALOG" "%{FOR_ROOT_CAT}.tmp"
done
# 41xml
for s in \
  "-//OASIS//DTD DocBook XML V4.1" \
  "-//OASIS//ELEMENTS DocBook Information Pool V4.1" \
  "-//OASIS//ELEMENTS DocBook Document Hierarchy V4.1" \
  "-//OASIS//ENTITIES DocBook Additional General Entities V4.1" \
  "-//OASIS//ENTITIES DocBook Notations V4.1" \
  "-//OASIS//ENTITIES DocBook Character Entities V4.1"
 do
 "$xmlcatbin" --noout --add "delegatePublic" "$s" \
   "file:///$CATALOG" "%{FOR_ROOT_CAT}.tmp"
done
"$xmlcatbin" --noout --add "delegateSystem" \
  "http://www.oasis-open.org/docbook/xml/4.1" \
  "file:///$CATALOG" "%{FOR_ROOT_CAT}.tmp"
"$xmlcatbin" --noout --add "delegateURI" \
  "http://www.oasis-open.org/docbook/xml/4.1" \
  "file:///$CATALOG" "%{FOR_ROOT_CAT}.tmp"
# Create tag
sed '/<catalog/a\
  <group id="%{name}-%{version}">
/<\/catalog/i\
  </group>' \
  "%{FOR_ROOT_CAT}.tmp" > "%{FOR_ROOT_CAT}"

%install
%{INSTALL_DIR} "$RPM_BUILD_ROOT"%{sgml_config_dir}
%{INSTALL_DIR} "$RPM_BUILD_ROOT"%{xml_config_dir}
%{INSTALL_DATA} CATALOG.* "$RPM_BUILD_ROOT"%{sgml_config_dir}
# for CATALOG.* links
%define my_all_cat docbook_4 db41xml db42xml db43xml db44xml db45xml
for v in 4.1 4.2 4.3 4.4 4.5; do
  vl=$(printf "%s" "$v" | sed 's/\.//')
  %{INSTALL_DIR} "$RPM_BUILD_ROOT"%{sgml_docbook_dtd_dir}/$v
  %{INSTALL_DATA} dtd/${v}/* "$RPM_BUILD_ROOT"%{sgml_docbook_dtd_dir}/${v}
  %{INSTALL_DIR} "$RPM_BUILD_ROOT"%{xml_docbook_dtd_dir}/$v
  cp -a ${v}xml/* "$RPM_BUILD_ROOT"%{xml_docbook_dtd_dir}/$v
  ln -s %{xml_docbook_dtd_dir}/$v "$RPM_BUILD_ROOT"%{sgml_docbook_dtd_dir}/${v}xml
  ln -sf %{sgml_config_dir}/CATALOG.db${vl}xml \
    "$RPM_BUILD_ROOT"%{sgml_dir}/CATALOG.db${vl}xml
done
ln -sf %{sgml_docbook_dtd_dir}/4.1 "$RPM_BUILD_ROOT"%{sgml_dir}/%{name}.1
ln -sf %{sgml_config_dir}/CATALOG.%{name} \
  "$RPM_BUILD_ROOT"%{sgml_dir}/CATALOG.%{name}
ln -sf %{sgml_config_dir}/CATALOG.%{name} \
  "$RPM_BUILD_ROOT"%{sgml_dir}/CATALOG.docbk41
cat_dir=%{buildroot}/etc/xml
%{INSTALL_DIR} "$cat_dir"
%{INSTALL_DATA} %{FOR_ROOT_CAT} docbook_41.xml "$cat_dir"
# rng
%{INSTALL_DIR} "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.3 "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.4 \
               "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.3 "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.4
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.2 %{S:422}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.3 %{S:432}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.4 %{S:442}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_rng_dir}/4.5 %{S:452}
# w3c schema
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.2 %{S:422}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.3 %{S:433}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.4 %{S:443}
unzip -q -a -d "$RPM_BUILD_ROOT"%{xml_docbook_xsd_dir}/4.5 %{S:453}
# cleanup
%fdupes "$RPM_BUILD_ROOT"

%post
if [ -x %{regcat} ]; then
  for c in %{my_all_cat}; do
    %{regcat} -a  %{sgml_dir}/CATALOG.$c \
      >/dev/null 2>&1 || true
  done
fi
if [ -x /usr/bin/edit-xml-catalog ]; then
  /usr/bin/edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
      --add /etc/xml/%{FOR_ROOT_CAT}
fi

%postun
if [ "$1" = "0" -a -x %{regcat} ]; then
  for c in %{my_all_cat}; do
    %{regcat} -r %{sgml_dir}/CATALOG.$c \
      >/dev/null 2>&1 || true
  done
fi
# remove entries only on removal of file
if [ ! -f %{xml_sysconf_dir}/%{FOR_ROOT_CAT} -a -x /usr/bin/edit-xml-catalog ] ; then
  /usr/bin/edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
      --del %{name}-%{version}
fi

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%config %{sgml_config_dir}/CATALOG.*
%{sgml_dir}/CATALOG.*
%{sgml_docbook_dtd_dir}/4.1
%{sgml_docbook_dtd_dir}/4.2
%{sgml_docbook_dtd_dir}/4.3
%{sgml_docbook_dtd_dir}/4.4
%{sgml_docbook_dtd_dir}/4.5
#
%{sgml_docbook_dtd_dir}/4.1xml
%{sgml_docbook_dtd_dir}/4.2xml
%{sgml_docbook_dtd_dir}/4.3xml
%{sgml_docbook_dtd_dir}/4.4xml
%{sgml_docbook_dtd_dir}/4.5xml
#
%{xml_docbook_dtd_dir}/4.1
%{xml_docbook_dtd_dir}/4.2
%{xml_docbook_dtd_dir}/4.3
%{xml_docbook_dtd_dir}/4.4
%{xml_docbook_dtd_dir}/4.5
#
%{xml_docbook_rng_dir}/4.2
%{xml_docbook_rng_dir}/4.3
%{xml_docbook_rng_dir}/4.4
%{xml_docbook_rng_dir}/4.5
#
%{xml_docbook_xsd_dir}/4.2
%{xml_docbook_xsd_dir}/4.3
%{xml_docbook_xsd_dir}/4.4
%{xml_docbook_xsd_dir}/4.5
#
%config %{xml_sysconf_dir}/docbook_41.xml
%config %{xml_sysconf_dir}/%{FOR_ROOT_CAT}
%dir %{sgml_dir}/docbook/dtd
%{sgml_dir}/docbook_4.1
# %dir %{xml_dir}
# %dir %{xml_docbook_dir}
%dir %{xml_docbook_dir}/schema
%dir %{xml_docbook_dtd_dir}
%dir %{xml_docbook_rng_dir}
%dir %{xml_docbook_xsd_dir}

%changelog
* Mon Jun 11 2012 coolo@suse.com
- iso_ent is required for SGML, so readd it as long as it's supported
* Tue Jun  5 2012 ke@suse.de
- spec: No longer Requires iso_ent (now Recommends) and xmlcharent
  (xml entities are shipped together with the DTD).
* Sun Sep 18 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
  (cf. packaging guidelines)
* Tue Apr  5 2011 ke@suse.de
- Also provide docbook-dtds; bnc#674044.
* Mon Aug 17 2009 aj@suse.de
- Only remove file from catalog if it disappeared.
- Do not use release numbers, they're not needed anymore.
- Fix some rpmlint warnings: do not remove buildroot, use fdupes.
* Thu Mar 29 2007 aj@suse.de
- Really add unzip as build requirement.
* Thu Mar 29 2007 toms@suse.de
- Added unzip as build requirements
* Fri Feb 16 2007 toms@suse.de
- Added RELAX NG and W3C schema for 4.5
- Completed DocBook 4.2 with RELAX NG and W3C
* Thu Feb 15 2007 toms@suse.de
- Added DocBook v4.5 XML and SGML DTD
- Added RELAX NG and W3C schema for 4.3 and 4.4
* Mon Jan 15 2007 ke@suse.de
- PreReq sgml-skel instead of file name.
* Fri Jan 12 2007 dmueller@suse.de
- fix build of depending packages once again
* Fri Jan 12 2007 ke@suse.de
- Remove 'exit 0' from %%post and %%postun; reported by Klaus Kaempf
  [# 216944].
* Thu Jan 11 2007 ke@suse.de
- Remove /usr/share/xml from the files list.
* Mon Aug 14 2006 ke@suse.de
- Remove obsolete compatibility link for <= SL 9.0.
* Sun Feb 19 2006 ro@suse.de
- modify setup line in spec file
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Dec 21 2005 aj@suse.de
- Package symlink.
* Fri Sep 16 2005 ke@suse.de
- Add catalog entries for version 4.3 and 4.4 (SGML flavor); reported by
  Ulrich Windl [# 104872].
- Allow ":" in attribute names for version 4.4, too (SGML flavor).
- Cleanup CATALOG.docbook_4: Remove commented entries, comment obsolete
  4.4 references (SGML flavor).
* Wed May 18 2005 ke@suse.de
- docbook-4-3-xml-cat.diff: add catalog entries for HTML tables;
  reported by Thomas Schraitle [# 84023].
* Wed Feb  2 2005 ke@suse.de
- Add docbook version 4.4 (SGML and XML).
* Fri Jul  2 2004 ke@suse.de
- Disable support for catalog support for 4.3 (SGML) for the moment;
  reported by Takashi Iwai.
* Mon Jun  7 2004 ke@suse.de
- Add docbook version 4.3 (SGML, XML, and experimental RNG flavor).
- Cleanup .spec file.
* Mon Mar  1 2004 ke@suse.de
- In %%postun check for the update case.
* Tue Feb 24 2004 hmacht@suse.de
- building as non-root
* Tue Feb 10 2004 ke@suse.de
- Move XML DTDs to /usr/share/xml/docbook/schema/dtd.
* Fri Jan 30 2004 ke@suse.de
- Add links pointing from the SGML hierarchy to the XML files.
* Thu Jan 22 2004 ke@suse.de
- Adjust directories according to FHS 2.3:
  * Move XML DTDs to /usr/share/xml/docbook.
  * Move SGML DTDs to /usr/share/sgml/docbook.
  * Keep CATALOG.* files in /usr/share/sgml for the time being.
  * Provide compatibility links for SL =< 9.0 (log this info in
    /var/adm/SuSEconfig/run-sgmldir-links for later processing).
* Fri Jul 11 2003 ke@suse.de
- Remove disturbing link %%{_datadir}/sgml/db42xml via %%pre.
* Wed Apr 30 2003 ke@suse.de
- Use the "//XML" suffix for Formal Public Identifiers of XML ISO
  entity sets.
* Tue Apr 29 2003 ke@suse.de
- Use /etc/xml/suse-catalog.xml instead of /etc/xml/catalog.
* Tue Apr 29 2003 ke@suse.de
- Use <group> sectioning in  /etc/xml/catalog.
* Mon Apr 28 2003 ke@suse.de
- Use edit-xml-catalog in %%post/%%postun for managing /etc/xml/catalog.
* Tue Apr 15 2003 ke@suse.de
- Fix %%preun/%%postun scripts: Use %%postun only to avoid nuking catalog
  entries during update; add rewriteSystem statement.
  Reported by Gernot Hillier [# 26270].
* Mon Nov 25 2002 ke@suse.de
- Use sgml-register-catalog to populate /etc/sgml/catalog.
* Fri Nov 15 2002 ke@suse.de
- Also for the 4.2 DTD provide convenience links for psgml.
* Wed Nov  6 2002 ke@suse.de
- Map DocBook 4.0 system identifiers to 4.1.
* Wed Aug 14 2002 ke@suse.de
- Add delegatePublic and delegateSystem for DocBook DTD 4.1 to the XML
  catalog.  Thus scrollkeeper-update can make use of local resources.
  Reported by Thorsten Kukuk and Olaf Hering [# 17646].
- Add more files to the uninstall cleanup scripts.
* Mon Aug 12 2002 ke@suse.de
- Don't use hardcoded version number ("41") when building the the 42
  SGML Open Catalog for the XML DTD.
  Reported by Norbert Eicker.
* Thu Aug  8 2002 ke@suse.de
- Add the third slash for "file:///' again (necessary because I removed
  one from the variable assignemnt).
* Wed Aug  7 2002 mls@suse.de
- Fixed exit status of postinstall script.
* Wed Aug  7 2002 ke@suse.de
- Drop the SuSEconfig script; reported by Thorsten Kukuk [# 17448].
* Tue Aug  6 2002 ke@suse.de
- Add missing PreReq (libxml2, zlib); reported by Thorsten Kukuk [#
  17435].
* Fri Jul 26 2002 ke@suse.de
- SuSEconfig.docbook_4: Remove CATALOG file with length of zero.
- Add "DTD DocBook XML V4.1" to /etc/xml/docbook_41.xml.
- Drop superfluous slashes ("file:///", not "file:////").
- Fix FPI names in /etc/xml/docbook_41.xml.
* Fri Jul 26 2002 ke@suse.de
- Actually install the catalogs and make sure applications will find
  more DTD.
* Wed Jul 24 2002 ke@suse.de
- Add SGML and XML DTD version 4.2.
- Simplify catalog creation and management.
* Mon Jun 24 2002 ke@suse.de
- Don't install XML ISO entity links; instead require xmlcharent.
- Start to prepare for release 4.2.
  Mon May  6 10:40:29 CEST 2002 - ke@suse.de
- Don't try to call the SuSEconfig script as long as the system isn't
  mounted on "/".
* Fri May  3 2002 ke@suse.de
- Provide /sbin/conf.d/SuSEconfig.%%{name} to initialize catalogs
  later if xmlcatalog isn't available at installation time.
* Thu May  2 2002 ke@suse.de
- Require libxml2 to install proper /etc/xml catalog files.
- Maintain /etc/xml catalog files via %%post/%%postun.
* Mon Aug 27 2001 ke@suse.de
- Rename README.SuSE to docbook_4-README.SuSE.
- Install DTD and ENTITY links using install-dtd.sh to support
  Emacs/PSGML.
- Cleanup spec file.
- Add sgml-skel to 'neededforbuild'.
* Tue Mar 13 2001 ke@suse.de
- Rename package: docbk_4 -> docbook_4 (cf. docbook_3).
- Update XML DTD (version 4.1.2).
- Add 'OVERRIDE YES' to XML catalog.
- Add README.SuSE.
* Tue Jun 27 2000 ke@suse.de
- Correct CATALOG entries for entities.
* Tue Jun 20 2000 ke@suse.de
- Initial package: version 4.1.

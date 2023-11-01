Summary:       Hardware lister
Name:          lshw
Version:       B.02.19.2
Release:       6%{?dist}
License:       GPLv2
Group:         Applications/System
URL:           http://ezix.org/project/wiki/HardwareLiSter
Source0:       http://www.ezix.org/software/files/lshw-%{version}.tar.gz
Patch1:        lshw-B.02.18-scandir.patch
Patch2:        lshw-B.02.18-revert-json.patch
Patch3:        lshw-B.02.19.2-cmake.patch
Patch4:        lshw-B.02.19.2-Add-the-FindPkgConfig-to-CMakeLists.patch
Patch5:        0001-report-CPU-family-model-stepping.patch
Patch6:        0002-move-PnP-devices-to-the-ISA-LPC-bridge.patch
Patch7:        0003-correctly-format-SMBIOS-UUID.patch
Patch8:        0004-cosmetic-clean-up.patch
Patch9:        0005-begin-work-on-input-devices.patch
Patch10:       0006-cosmetic-fixes.patch
Patch11:       0007-detect-sound-devices.patch
Patch12:       0008-detect-framebuffers.patch
Patch13:       0009-try-to-connect-input-devices-to-the-right-parent.patch
Patch14:       0010-devtree-Add-chip-id-from-the-dimm-module.patch
Patch15:       0011-devtree-Add-chip-id-from-CPU-node.patch
Patch16:       0012-volumes-fix-segfault-in-apfs-volume-code.patch
Patch17:       0013-merge-Github-PR-53.patch
Patch18:       0014-devtree-Add-capabilites-to-the-OPAL-Firmware.patch
Patch19:       0015-fix-issue-with-logical-names-being-truncated-dev-sda.patch
Patch20:       0016-code-clean-up-for-read-3.patch
Patch21:       0017-report-product-model-on-Power-systems.patch
Patch22:       0001-Fix-few-memory-leaks.patch
Patch23:       0002-Build-against-gtk3-instead-of-gtk2.patch
Patch24:       0003-Remove-deprecated-stock-messages.patch
Patch25:       0004-Remove-hack-which-is-apparently-not-useful-anymore.patch
Patch26:       0005-Use-GtkFileChooserNative-instead-of-GtkFileChooserDi.patch
Patch27:       0006-Replace-deprecated-GtkIconFactory-with-GHashTable.patch
Patch28:       0007-Replace-the-last-GtkStock-in-overwrite-dialog.patch
Patch29:       0008-Remove-deprecated-widgets.patch
Patch30:       0009-Remove-deprecated-use_action_appearance-property.patch
Patch31:       0010-Move-to-GtkApplication.patch
Patch32:       0011-Replace-signals-with-GSimpleActions.patch
Patch33:       0012-Enable-Disable-GSimpleAction-instead-of-button-sensi.patch
Patch34:       0013-Move-from-GtkMenuBar-to-GMenu.patch
Patch35:       0014-Replace-the-about-GtkDialog-with-a-GtkAboutDialog.patch
Patch36:       0015-Update-docs-TODO.patch
Patch37:       0016-Update-docs-TODO.patch
Patch38:       0017-update-man-page.patch
Patch39:       0018-fix-man-page-after-previous-update.patch
Patch40:       rhelonly-cleanup-remove-unused-support.c-support.h-generated-.patch
Patch41:       0001-Report-correct-memory-size-on-SMBIOS-2.7.patch
Patch42:       0001-devtree-Add-UUID-property.patch
Patch43:       0001-Fix-getting-size-of-memory-banks-32GiB.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: gtk3-devel >= 3.22
BuildRequires: libappstream-glib
BuildRequires: ninja-build
BuildRequires: python3-devel
BuildRequires: sqlite
BuildRequires: sqlite-devel
Requires:      hwdata
%description
lshw is a small tool to provide detailed informaton on the hardware
configuration of the machine. It can report exact memory
configuration, firmware version, mainboard configuration, CPU version
and speed, cache configuration, bus speed, etc. on DMI-capable x86
systems and on some PowerPC machines (PowerMac G4 is known to work).

Information can be output in plain text, XML or HTML.

%package       gui
Summary:       Graphical hardware lister
Group:         Applications/System
Requires:      polkit
Requires:      gtk3 >= 3.22
Requires:      %{name} = %{version}-%{release}
%description   gui
Graphical frontend for the hardware lister (lshw) tool. If desired,
hardware information can be saved to file in plain, XML or HTML
format.

%prep
%setup -q
%patch01 -p1
%patch02 -R -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1

%build
mkdir build && pushd build
%cmake .. -DNOLOGO=ON -DHWDATA=OFF -DPOLICYKIT=ON -DBUILD_SHARED_LIBS=OFF -DSQLITE=ON -GNinja
%ninja_build

%install
pushd build
%ninja_install
ln -s gtk-lshw %{buildroot}%{_sbindir}/lshw-gui

# translations seems borken, remove for now
#find_lang %{name}
rm -rf %{buildroot}%{_datadir}/locale/fr/

%check
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

# check json output is valid
pushd build
src/lshw -json \
    -disable usb -disable pcmcia -disable isapnp \
    -disable ide -disable scsi -disable dmi -disable memory \
    -disable cpuinfo 2>/dev/null | %{__python3} -m json.tool

#files -f %{name}.lang
%files
%license COPYING
%doc README.md
%{_mandir}/man1/lshw.1*
%{_sbindir}/lshw

%files gui
%license COPYING
%{_bindir}/lshw-gui
%{_sbindir}/gtk-lshw
%{_sbindir}/lshw-gui
%dir %{_datadir}/lshw
%{_datadir}/lshw/artwork
%dir %{_datadir}/lshw/ui
%{_datadir}/lshw/ui/gtk-lshw.ui
%{_datadir}/pixmaps/gtk-lshw.svg
%{_datadir}/applications/gtk-lshw.desktop
%{_datadir}/appdata/gtk-lshw.appdata.xml
%{_datadir}/polkit-1/actions/org.ezix.lshw.gui.policy

%changelog
* Tue Jun 08 2021 Tao Liu <ltao@redhat.com> - B.02.19.2-6
- Fix getting size of memory banks <32GiB

* Tue Feb 02 2021 Lianbo Jiang <lijiang@redhat.com> - B.02.19.2-5
- Fix the wrong memory information in azure m or mv2 series
- Add UUID property to PowerVM LPAR

* Wed Dec 16 2020 Lianbo Jiang <lijiang@redhat.com> - B.02.19.2-4
- Fix the gtk3 dependency for lshw-gui instead of lshw
- Resolves: rhbz#1905816

* Thu Dec 03 2020 Lianbo Jiang <lijiang@redhat.com> - B.02.19.2-3
- Update to upstream master 56f1de9d1e4d
- Resolves: rhbz#1844426

* Wed May 27 2020 Lianbo Jiang <lijiang@redhat.com> - B.02.19.2-2
- Update to upstream master 3775782808e8

* Tue May 26 2020 Lianbo Jiang <lijiang@redhat.com> - B.02.19.2-1
- B.02.19.2

* Mon Feb 10 2020 Lianbo Jiang <lijiang@redhat.com> - B.02.18-23
- Do not show modified time with -notime option
- Resolves: rhbz#1733126

* Thu Nov 21 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-22
- Display proper logical name of network device
- Resolves: rhbz#1724087
- Add DIMM running speed and Print dimm rank information
- Resolves: rhbz#1725199

* Mon May 13 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-21
- Update to upstream master 6cc0581bc805.
- Resolves: rhbz#1664092

* Thu Apr 25 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-20
- Change python to python3 in selftest/Makefile for the CI gating test.
- Resolves: rhbz#1680623

* Thu Apr 25 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-19
- Enable SQLite and fix the CI gating test.
- Resolves: rhbz#1680623

* Tue Apr 23 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-18
- Fix:59a8e99ab22d ("Porting the code from /CoreOS/lshw/sanity/check-output for the CI gating")
- Resolves: rhbz#1680623

* Fri Apr 19 2019 Lianbo Jiang <lijiang@redhat.com> - B.02.18-17
- Add the CI gating test
- Resolves: rhbz#1680623

* Mon Apr 02 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-16
- Update to commit 20cda77
- Convert to cmake build system

* Thu Feb 08 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-15
- Fix JSON issue (rhbz#1543320)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-13
- Fix date
- Need gettext

* Fri Jan 26 2018 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-12
- Update to commit d05baa7

* Mon Aug 28 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-11
- Prefer lshw-gui in lshw-gui context

* Sun Aug 13 2017 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-10
- Add AppData bz#1476498

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - B.02.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 24 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-5
- Modify lshw gui wrapper to fix bz#1368404

* Thu Aug 11 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-4
- Add patches to fix sysconf/long_bit issue and crash (bz#1342792)

* Wed May 18 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-3
- Add patch to fix crash (bz#1332486)

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-2
- Date fix

* Mon Apr 25 2016 Terje Rosten <terje.rosten@ntnu.no> - B.02.18-1
- B.02.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - B.02.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - B.02.17-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-2
- Add patch to fix segfault in scan fat code

* Thu Sep 26 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.17-1
- B.02.17

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-8
- Rename macro

* Sun Jun 09 2013 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-7
- Fix desktop file (bz #953684)
- Remove broken translations (bz #905896)
- Add vendor macro
 
* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - B.02.16-6
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-3
- Switch from consolehelper to PolicyKit (bz #502730)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.16-2
- Rebuilt for c++ ABI breakage

* Sun Jan 29 2012 Terje Rosten <terje.rosten@ntnu.no> - B.02.16-1
- B.02.16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-3
- Own all dirs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.15-1
- B.02.15
- Remove patches now upstream
- Build with sqlite support

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-5
- Add patch to fix build with gcc-4.5

* Sun Sep 05 2010 Terje Rosten <terje.rosten@ntnu.no> - B.02.14-4
- Add patch to fix ext4 issue

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Adam Jackson <ajax@redhat.com> - B.02.14-2
- Requires: hwdata
- Drop redundant copies of pci.ids and friends, since we'll pick up the
  copies in hwdata at runtime

* Sun Mar  1 2009 Terje Rosten <terjeros@phys.ntnu.no> - B.02.14-1
- B.02.14
- Drop gcc43 patch now upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - B.02.13-4
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-3
- rebuild

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-2
- proper patch macro

* Wed Aug 13 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.13-1
- B.02.13
- remove patches now upstream
- add new gcc43 patch

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-5
- rebuild

* Tue Apr 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-4
- add patch to fix bz #442501

* Mon Feb 11 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-3
- add patch to build with gcc-4.3

* Sat Feb 09 2008 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-2
- rebuild

* Mon Nov  5 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.12.01-1
- B.02.12.01
- Replace trademark icons

* Tue Aug 14 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-3
- Move desktop and pam config to files
- Simplify build

* Tue Aug 07 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-2
- Remove trademarks

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11.01-1
- B.02.11.01

* Sun Aug 05 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-3
- Move artwork to gui subpackage
- Implement consolehelper support

* Sat Aug 04 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-2
- License is GPLv2 (only)
- Fix ui %%description

* Wed Aug 01 2007 Terje Rosten <terjeros@phys.ntnu.no> - B.02.11-1
- Follow upstream version scheme

* Wed Jul 25 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.11-1
- 2.11

* Wed Jun 27 2007 Terje Rosten <terjeros@phys.ntnu.no> - 2.10-2
- minor fixes
- add patch to avoid stripping
- add desktop file
- strip changelog
- move from sbin to bin
- new url

* Wed Feb 14 2007 Dag Wieers <dag@wieers.com> - 2.10-1 - 4876+/dag
- Updated to release B.02.10.

* Tue Dec 21 2004 Dag Wieers <dag@wieers.com> - 2.0-1
- Initial package. (using DAR)


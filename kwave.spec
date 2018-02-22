Name:           kwave
Version:        17.12.2
Release:        1%{?dist}
Summary:        Sound Editor for KDE
Summary(de):    Sound-Editor für KDE

# See the file LICENSES for the licensing scenario
License:        GPLv2+ and BSD and CC-BY-SA
URL:            http://kwave.sourceforge.net
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(KF5Archive)
BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5WidgetsAddons)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  cmake(KF5Completion)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5IconThemes)
BuildRequires:  cmake(KF5Crash)
BuildRequires:  cmake(KF5DBusAddons)
BuildRequires:  cmake(KF5TextWidgets)
BuildRequires:  cmake(KF5DocTools)
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel >= 0.3.0
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  fftw-devel >= 3.0
BuildRequires:  flac-devel
BuildRequires:  gettext
BuildRequires:  id3lib-devel >= 3.8.1
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib
BuildRequires:  libmad-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libvorbis-devel
BuildRequires:  opus-devel
BuildRequires:  poxml
BuildRequires:  pulseaudio-libs-devel >= 0.9.16

Requires:       %{name}-doc = %{version}-%{release}

%description
With Kwave you can record, play back, import and edit many sorts of audio files
including multi-channel files. Kwave includes some plugins to transform audio
files in several ways and presents a graphical view with a complete zoom- and
scroll capability.

%description -l de
Mit Kwave können Sie ein- oder mehrkanalige Audio-Dateien aufnehmen, wieder-
geben, importieren und bearbeiten. Kwave verfügt über Plugins zum Umwandeln
von Audio-Dateien auf verschiedene Weise. Die grafische Oberfläche bietet
alle Möglichkeiten für Änderungen der Ansichtsgröße und zum Rollen.

%package doc
Summary:        User manuals for %{name}
Summary(de):    Benutzerhandbücher für %{name}
License:        GFDL
BuildArch:      noarch


%description doc
This package contains arch-independent files for %{name}, especially the
HTML documentation.

%description doc -l de
Dieses Paket enthält architekturunabhängige Dateien für %{name},
speziell die HTML-Dokumentation.

%prep
%autosetup -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} -DWITH_MP3=ON ..
%make_build
popd

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_metainfodir}/org.kde.%{name}.appdata.xml || :
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop || :

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_kf5_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_kf5_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS CHANGES README TODO
%license GNU-LICENSE LICENSES
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_kf5_metainfodir}/org.kde.%{name}.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/apps/%{name}.*
%{_kf5_datadir}/icons/hicolor/*/actions/%{name}*
%{_kf5_datadir}/%{name}/
%{_kf5_datadir}/kservicetypes5/%{name}-plugin.desktop
%{_kf5_qtplugindir}/%{name}/
%{_kf5_libdir}/lib%{name}.so.*
%{_kf5_libdir}/lib%{name}gui.so.*

%files doc
%{_kf5_docdir}/HTML/*/%{name}

%changelog
* Thu Feb 22 2018 Sérgio Basto <sergio@serjux.com> - 17.12.2-1
- Update kwave to 17.12.2

* Tue Jan 30 2018 Sérgio Basto <sergio@serjux.com> - 17.12.1-1
- Update kwave to 17.12.1

* Tue Jan 02 2018 Sérgio Basto <sergio@serjux.com> - 17.12.0-2
- Use _kf5_metainfodir to fix appdata directory issue

* Fri Dec 29 2017 Sérgio Basto <sergio@serjux.com> - 17.12.0-1
- Update kwave to 17.12.0

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 17.08.1-1
- Update kwave to 17.08.1

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 17.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 17.04.2-1
- Update to 17.04.2

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 16.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 16.12.2-1
- Initial port to kf5

* Sun Feb 15 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-7
- Add BSD license

* Sat Feb 07 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-6
- Add mp3 support via libmad

* Tue Feb 03 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-5
- Remove gcc-c++ from BR
- Fix %%post and %%postun
- Move lsm file to the -doc subpackage

* Mon Feb 02 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-4
- Move the documentation to a noarch subpackage

* Sat Jan 31 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-3
- Add update-desktop-database scriptlet

* Wed Jan 28 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-2
- Generate png icons

* Fri Jan 16 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 0.8.99-1
- Initial package

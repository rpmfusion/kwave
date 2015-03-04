%global MP3ENABLED "-DWITH_MP3=ON"

Name:           kwave
Version:        0.8.99
Release:        7%{?dist}
Summary:        Sound Editor for KDE
Summary(de):    Sound-Editor für KDE

# See the file LICENSES for the licensing scenario
License:        GPLv2+ and BSD and CC-BY-SA
URL:            http://kwave.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-2.tar.bz2
Source1:        %{name}.appdata.xml
# This has been already fixed upstream
Patch0:         %{name}-desktop.diff

BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel >= 0.3.0
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  fftw-devel >= 3.0
BuildRequires:  flac-devel
BuildRequires:  gettext
BuildRequires:  id3lib-devel >= 3.8.1
BuildRequires:  ImageMagick
BuildRequires:  kdemultimedia-devel >= 4.0
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

Requires:       kde-filesystem

%description doc
This package contains arch-independent files for %{name}, especially the
HTML documentation.

%description doc -l de
Dieses Paket enthält architekturunabhängige Dateien für %{name},
speziell die HTML-Dokumentation.

%prep
%setup -q
%patch0

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} %{MP3ENABLED} ../
popd
make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

mkdir -p %{buildroot}%{_kde4_datadir}/appdata/
install -p -m 644 %{SOURCE1} %{buildroot}%{_kde4_datadir}/appdata/

# Generate resized icons
mkdir -p %{buildroot}/%{_kde4_iconsdir}/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,72x72,96x96,128x128,256x256}/apps
for s in 16x16 22x22 24x24 32x32 48x48 64x64 72x72 96x96 128x128 256x256
do
    convert -background none %{name}/pics/%{name}.svgz -resize $s %{buildroot}/%{_kde4_iconsdir}/hicolor/$s/apps/%{name}.png;
done

%find_lang kwave %{name}.lang

%check
appstream-util validate-relax --nonet %{buildroot}%{_kde4_datadir}/appdata/%{name}.appdata.xml || :
desktop-file-validate %{buildroot}/%{_datadir}/applications/kde4/%{name}.desktop || :

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS CHANGES README TODO
%license GNU-LICENSE LICENSES
%{_kde4_appsdir}/%{name}
%{_kde4_bindir}/%{name}
%{_kde4_datadir}/applications/kde4/%{name}.desktop
%{_kde4_datadir}/appdata/%{name}.appdata.xml
%{_kde4_iconsdir}/hicolor/*/apps/%{name}.*
%{_kde4_iconsdir}/hicolor/*/actions/%{name}*
%{_kde4_libdir}/kde4/plugins/%{name}
%{_kde4_libdir}/lib%{name}.so.*
%{_kde4_libdir}/lib%{name}gui.so.*

%files doc
%doc kwave.lsm
%{_kde4_docdir}/HTML/*/%{name}

%changelog
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

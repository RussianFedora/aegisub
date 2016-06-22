Summary:	Advanced Subtitle Editor
Name:		aegisub
Version:	3.2.2
Release:	3%{?dist}

URL:		http://www.aegisub.org
Group:		Applications/Multimedia
License:	BSD
Source0:	http://ftp.aegisub.org/pub/archives/releases/source/%{name}-%{version}.tar.xz
Patch0:	        fix-tools-ldflags.patch

BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libass)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	wxGTK3-devel
BuildRequires:	pkgconfig(lua-5.1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(ffms2)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool


%description
Aegisub is an advanced subtitle editor that assists in the creation of
subtitles, translations, and complex overlays using audio or video. Developed
by enthusiasts it builds on work-flows created and perfected through
professional, hobby, and everyday use.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .ldflags

%build
#remove version postfix
sed -e 's/aegisub-3\.2/aegisub/' -e 's/aegisub-32/aegisub/' -i configure
%configure \
	--without-oss \
	--without-openal \
	--with-player-audio=pulseaudio \
	--with-wx-config=wx-config-3.0

%make_build


%install
%make_install
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc automation/demos/ automation/v4-docs/
%license LICENCE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Wed Jun 22 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 3.2.2-3
- Rebuild for new boost

* Wed Nov 04 2015 Ivan Epifanov <isage.dna@gmail.com> - 3.2.2-3.R
- Fix tools ldflags

* Wed Nov 04 2015 Vasiliy N. Glazov <vascom2@gmail.com> 3.2.2-2.R
- bump release fo rebuild

* Mon Jan  5 2015 Ivan Epifanov <isage.dna@gmail.com> - 3.2.2-1.R
- update to 3.2.2

* Sat May 17 2014 Ivan Epifanov <isage.dna@gmail.com> - 3.1.3-1.R
- update to 3.1.3

* Fri Mar 28 2014 Ivan Epifanov <isage.dna@gmail.com> - 3.1.2-1.R
- update to 3.1.2

* Wed Jan 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.1.8-1
- initial build for Fedora
- fix build with ffmpeg
- fix DSO for libz
- fix build w/o fatal exceptions in wxWidgets

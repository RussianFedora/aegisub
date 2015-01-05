Summary:	Advanced Subtitle Editor
Name:		aegisub
Version:	3.2.2
Release:	1%{?dist}

URL:		http://www.aegisub.org
Group:		Applications/Multimedia
License:	BSD
Source0:	http://ftp.aegisub.org/pub/archives/releases/source/%{name}-%{version}.tar.xz

BuildRequires:	alsa-lib-devel
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libass-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw-devel
BuildRequires:	hunspell-devel
BuildRequires:	wxGTK3-devel
%if 0%{?fedora} >= 20
BuildRequires:	compat-lua-devel
%else
BuildRequires:	lua-devel
%endif
BuildRequires:	freetype-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	ffms2-devel
BuildRequires:	boost-devel
BuildRequires:	libicu-devel
BuildRequires:	desktop-file-utils
BuildRequires:	intltool


%description
Aegisub is an advanced subtitle editor that assists in the creation of
subtitles, translations, and complex overlays using audio or video. Developed
by enthusiasts it builds on work-flows created and perfected through
professional, hobby, and everyday use.


%prep
%setup -q -n %{name}-%{version}


%build
#remove version postfix
sed -e 's/aegisub-3\.2/aegisub/' -e 's/aegisub-32/aegisub/' -i configure
%configure \
	--without-oss \
	--without-openal \
	--with-player-audio=pulseaudio \
	--with-wx-config=wx-config-3.0

make %{?_smp_mflags}


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
%doc LICENCE automation/demos/ automation/v4-docs/
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
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

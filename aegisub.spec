Summary:	Advanced Subtitle Editor
Name:		aegisub
Version:	2.1.8
Release:	1%{?dist}

URL:		http://www.aegisub.org
Group:		Applications/Multimedia
License:	BSD
Source:		http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.gz
Patch0:		aegisub-2.1.8-fatal-exceptions.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alsa-lib-devel
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libass-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	hunspell-devel
BuildRequires:	wxGTK-devel
BuildRequires:	perl-devel
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	ruby-devel
BuildRequires:	lua-devel
BuildRequires:	freetype-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	desktop-file-utils
BuildRequires:	intltool


%description
Aegisub is an advanced subtitle editor that assists in the creation of
subtitles, translations, and complex overlays using audio or video. Developed
by enthusiasts it builds on workflows created and perfected through
professional, hobby, and everyday use.


%prep
%setup -q
%patch0 -p1 -b .fatal-exceptions


%build
export LDFLAGS="-lz"
export CXXFLAGS="-D__STDC_CONSTANT_MACROS $RPM_OPT_FLAGS"
%configure \
	--without-oss \
	--without-openal \
	--with-perl \
	--with-ruby \
	--with-provider-video=ffmpeg \
	--with-provider-audio=ffmpeg \
	--with-player-audio=pulseaudio

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_datadir}/doc

find %{buildroot} -name "*.pl" -exec chmod 755 {} \;

%find_lang aegisub21


%clean
rm -rf %{buildroot}


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


%files -f aegisub21.lang
%defattr(-,root,root)
%doc README INSTALL automation/demos/ automation/v4-docs/ automation/automation3.txt
%{_bindir}/aegisub-2.1
%dir %{_datadir}/aegisub
%{_datadir}/aegisub/*
%{_datadir}/applications/aegisub.desktop
%{_datadir}/icons/hicolor/*/apps/aegisub.*


%changelog
* Wed Jan 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.1.8-1
- initial build for Fedora
- fix build with ffmpeg
- fix DSO for libz
- fix build w/o fatal exceptions in wxWidgets

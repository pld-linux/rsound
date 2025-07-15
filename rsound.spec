# TODO: roar, muroar, binds/cs
#
# Conditional build:
%bcond_without	alsa		# ALSA support in rsd
%bcond_without	libao		# libao support in rsd
%bcond_without	jack		# JACK support in rsd
%bcond_with	muroar		# muRoar support in rsd
%bcond_without	openal		# OpenAL support in rsd
%bcond_without	oss		# OSS support in rsd
%bcond_without	portaudio	# PortAudio support in rsd
%bcond_without	pulseaudio	# PulseAudio support in rsd
%bcond_with	roar		# RoarAudio support in rsd

Summary:	RSound - a portable networked audio system
Summary(pl.UTF-8):	RSound - przenośny, sieciowy system dźwięku
Name:		rsound
Version:	1.1
Release:	1
License:	GPL v3+
Group:		Applications/Sound
Source0:	https://github.com/Themaister/RSound/archive/v%{version}/RSound-%{version}.tar.gz
# Source0-md5:	d416ecd6d1ca39af78c7626ed1b3833e
Patch0:		%{name}-libdir.patch
URL:		http://themaister.net/rsound.html
%{?with_openal:BuildRequires:	OpenAL-devel}
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9}
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
%{?with_libao:BuildRequires:	libao-devel}
%{?with_roar:BuildRequires:	libroar-devel}
BuildRequires:	libsamplerate-devel
%{?with_muroar:BuildRequires:	muroar-devel}
%{?with_portaudio:BuildRequires:	portaudio-devel}
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RSound is a portable networked audio system. It allows you to send
audio from an application and transfer it directly to a different
computer on your LAN network. It is an audio daemon with a much
different focus than most other audio daemons.

%description -l pl.UTF-8
RSound to przenośny, sieciowy system dźwięku. Pozwala na przesyłanie
dźwięku z aplikacji i wysyłanie go bezpośrednio do innego komputera w
sieci lokalnej. Jest to demon dźwięku skupiający się na innych
elementach, niż większość innych demonów.

%package libs
Summary:	RSound shared library
Summary(pl.UTF-8):	Biblioteka współdzielona RSound
Group:		Libraries

%description libs
RSound audio library, designed for seamless networked transfer of
audio streams.

%description libs -l pl.UTF-8
Biblioteka dźwiękowa RSound, zaprojektowana do przezroczystego
przesyłania strumieni dźwiękowych przez sieć.

%package devel
Summary:	Header files for RSound library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki RSound
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for RSound library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki RSound.

%package static
Summary:	Static RSound library
Summary(pl.UTF-8):	Statyczna biblioteka RSound
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static RSound library.

%description static -l pl.UTF-8
Statyczna biblioteka RSound.

%package -n python-rsound
Summary:	Python binding for RSound
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki RSound
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-rsound
Python binding for RSound.

%description -n python-rsound -l pl.UTF-8
Wiązanie Pythona do biblioteki RSound.

%prep
%setup -q -n RSound-%{version}
%patch -P0 -p1

%build
# not autoconf configure
CC="%{__cc}" \
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
./configure \
	--prefix=%{_prefix} \
	%{!?with_alsa:--disable-alsa} \
	%{!?with_jack:--disable-jack} \
	%{!?with_libao:--disable-libao} \
	%{!?with_muroar:--disable-muroar} \
	%{!?with_openal:--disable-openal} \
	%{!?with_oss:--disable-oss} \
	%{!?with_portaudio:--disable-portaudio} \
	%{!?with_pulseaudio:--disable-pulse} \
	%{!?with_roar:--disable-roar}

# not supported by configure
echo "LIBDIR = %{_libdir}" >> src/config.mk

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D binds/python/rsound.py $RPM_BUILD_ROOT%{py_sitescriptdir}/rsound.py
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/rsd
%attr(755,root,root) %{_bindir}/rsdplay
%{_mandir}/man1/rsd.1*
%{_mandir}/man1/rsdplay.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librsound.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librsound.so.3

%files devel
%defattr(644,root,root,755)
%doc DOCUMENTATION
%attr(755,root,root) %{_libdir}/librsound.so
%{_includedir}/rsound.h
%{_pkgconfigdir}/rsound.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librsound.a

%files -n python-rsound
%defattr(644,root,root,755)
%{py_sitescriptdir}/rsound.py[co]

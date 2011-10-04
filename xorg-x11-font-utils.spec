%define pkgname font-utils

Summary: X.Org X11 font utilities
Name: xorg-x11-%{pkgname}
Version: 7.5
Release: 4
License: MIT/X11
Group: System/X11
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/app/bdftopcf-1.0.2.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/app/fonttosfnt-1.0.4.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/app/mkfontdir-1.0.5.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/app/mkfontscale-1.0.7.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/app/font-util-1.1.1.tar.bz2
Source101: xorg-x11-font-utils-rpmlintrc

Patch0:  change-default-fontrootdir-option.patch

BuildRequires: pkgconfig
# xorg-x11-libXfont-devel needed for bdftopcf
BuildRequires: libXfont-devel
# xorg-x11-libX11-devel needed for fonttosfnt
BuildRequires: libX11-devel
# xorg-x11-libfontenc-devel needed for fonttosfnt, mkfontscale
BuildRequires: libfontenc-devel >= 0.99.2-2
# freetype-devel needed for bdftopcf, fonttosfnt, mkfontscale
BuildRequires: freetype-devel
# zlib-devel needed for bdftopcf
BuildRequires: zlib-devel
# xorg-x11-proto-devel is needed for mkfontscale, which includes headers
# from it directly.
BuildRequires: pkgconfig(fontsproto)

BuildRequires: autoconf

# NOTE: This versioned pre-dependency is needed to ensure that the bugfix for
# bug #173875 is installed in order for mkfontscale/mkfontdir to work
# properly.  It is a "pre" dep, to ensure libfontenc gets installed before
# xorg-font-utils, before any fonts in an rpm upgrade or multi-transaction
# set, avoiding a possible race condition.
Requires(pre): libfontenc >= 0.99.2-2

Provides: %{pkgname}
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, ucs2any
Obsoletes: xorg-x11-base-fonts <= 6.7.99.903-3

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%package -n bdftruncate
Summary: Generate truncated BDF font from ISO 10646-1 encoded BDF font
Group:   Applications/System

%description -n bdftruncate
bdftruncate allows one to generate from an ISO10646-1 encoded BDF font
other ISO10646-1 BDF fonts in which all characters above a threshold
code value are stored unencoded. This is often desirable because the
Xlib API and X11 protocol data structures used for representing font
metric information are extremely inefficient when handling sparsely
populated fonts.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4

%patch0 -p0 -b .change-default-fontrootdir-option

%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      pushd $app-*
      case $app in
        font-util)
         autoconf
         ;;
      esac
      %configure
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
    for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
	pushd $app-*
	make install DESTDIR=$RPM_BUILD_ROOT
	popd
    done
    for i in */README ; do
	[ -s $i ] && cp $i README-$(echo $i | sed 's/-[0-9].*//')
    done
    for i in */COPYING ; do
	grep -q stub $i || cp $i COPYING-$(echo $i | sed 's/-[0-9].*//')
    done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README-* COPYING-*
%{_bindir}/bdftopcf
%{_bindir}/fonttosfnt
%{_bindir}/mkfontdir
%{_bindir}/mkfontscale
%{_bindir}/ucs2any
# blech.  this one should be in -filesystem
%dir %{_datadir}/X11/
%dir %{_datadir}/X11/fonts
%dir %{_datadir}/X11/fonts/util
%{_datadir}/X11/fonts/util/map-*
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
%doc %{_mandir}/man1/bdftopcf.1*
%doc %{_mandir}/man1/fonttosfnt.1*
%doc %{_mandir}/man1/mkfontdir.1*
%doc %{_mandir}/man1/mkfontscale.1*
%doc %{_mandir}/man1/ucs2any.1*

%files -n bdftruncate
%defattr(-,root,root,-)
%{_bindir}/bdftruncate
%doc %{_mandir}/man1/bdftruncate.1*



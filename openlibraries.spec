%define major		0
%define libname		%mklibname %name %major
%define old_libname	%mklibname %name 0.0.5
%define libnamedev	%mklibname %name -d
%define libname_orig	lib%{name}
%define snapshot	20081210

Summary:	Library suite for non-linear editing, VFX and rich media applications
Name:		openlibraries
Version:	0.5.0
Release:	%mkrel 0.%{snapshot}.3
License:	LGPL+
Group:		System/Libraries
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{snapshot}.tar.lzma
Patch0:		openlibraries-20081210-system-boost.patch
Patch1:		openlibraries-0.2-compile.patch
Patch2:		openlibraries-0.5.0-libpath.patch
Patch3:		openlibraries-20081210-mltconfig.patch
Patch4:		openlibraries-20081210-underlink.patch
# From http://gimpel.ath.cx/trac/browser/gimpel/media-libs/openlibraries
# (rediffed): fix a variable type problem in avformat plugin - thanks
# Thomas Kuther - AdamW 2008/12
Patch5:		openlibraries-20081210-alt-avformat-make.patch
# Check for (and set libs and cflags for) avcodec, avutil and swscale
# as well as avformat: needed as the avformat plugin must link against
# them too - AdamW 2008/12
Patch6:		openlibraries-20081210-libavcodec.patch
# Fix for a change in boost's handling of leaf in 1.36 - AdamW 2008/12
Patch7:		openlibraries-20081210-oil_boost_leaf.patch
URL:		http://www.openlibraries.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires:	boost >= 1.33
BuildRequires:	qt3-devel
BuildRequires:	glew-devel >= 1.3.3
BuildRequires:	boost-devel >= 1.33
BuildRequires:	sqlite3-devel
BuildRequires:	tiff-devel
BuildRequires:	bzip2-devel
BuildRequires:	zlib-devel
BuildRequires:	libxml2-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
Buildconflicts:	libcaca-devel
BuildRequires:	openal-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	python-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	MesaGLU-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglut-devel
BuildRequires:	mlt-devel
BuildRequires:	mlt++-devel

%description
Openlibraries contains a powerful cross-platform set of libraries that provide 
developers with the key building blocks they need to easily create, test
and deploy rich media applications.

%package -n 	%{libname}
Summary:	OpenLibraries libraries
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%old_libname

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with openlibraries.

%package -n	%{libnamedev}
Summary:	Headers for developing programs that will use openlibraries
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{libname_orig}-devel = %{version}-%{release}
Obsoletes:	%old_libname-devel

%description -n %{libnamedev}
OpenLibraries development headers/libs.

%package media
Summary:	OpenLibraries sample media files
Group:		Video
Requires:	openlibraries = %{version}
Requires:	boost >= 1.33
Requires:	glew >= 1.3.3

%description media
OpenLibraries sample media files.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .system-boost
%patch1 -p1 -b .compile
%patch2 -p1 -b .libpath
%patch3 -p1 -b .mltconfig
%patch4 -p1 -b .underlink
%patch5 -p1 -b .vars
%patch6 -p1 -b .libavcodec
%patch7 -p1 -b .boost-leaf

%build
if [ ! -z $QTDIR ]; then
        export QTPATH=$QTDIR/bin
        export PATH=$PATH:$QTPATH
else
        export PATH=$PATH:%{qt3dir}
fi

autoreconf -i

%configure2_5x \
	--enable-static \
	--disable-cg \
	--with-boostruntime=mt \
	--with-boostthreadruntime=mt \
	--with-boostprefix=%{_prefix} \
	--with-qtinclude=%{qt3include} \
	--with-qtlib=%{qt3lib} \
%if %{mdkversion} >= 200710
	--with-pythonversion=2.5
%endif
make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/%{name}-%{version}/*/plugins/*.so.%{major}*
%{py_platsitedir}/*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc COPYING
%{_includedir}/%{name}-%{version}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/%{name}-%{version}/*/plugins/*.a
%{_libdir}/%{name}-%{version}/*/plugins/*.la
%{_libdir}/%{name}-%{version}/*/plugins/*.so
%{_libdir}/%{name}-%{version}/*/plugins/*.opl
%{_libdir}/pkgconfig/*.pc

%files media
%defattr(-,root,root)
%{_datadir}/%{name}-%{version}

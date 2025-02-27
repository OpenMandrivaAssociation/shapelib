%define	major 4
%define	oldlibname %mklibname %{name} 2
%define	olddevelname %mklibname %{name} -d
%define	libname %mklibname shp
%define	develname %mklibname shp -d

Summary:	API in "C" for Shapefile handling
Name:		shapelib
Version:	1.6.1
Release:	1
License:	LGPL MIT
Group:		Sciences/Geosciences
URL:		https://shapelib.maptools.org/
Source0:	https://github.com/OSGeo/shapelib/archive/v%{version}.tar.gz
Requires:	proj >= 4.4.1
BuildRequires:	pkgconfig(proj) >= 4.4.1

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%package -n	%{libname}
Summary:	API in "C" for Shapefile handling
Group:		System/Libraries
%rename %{oldlibname}

%description -n	%{libname}
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%package -n	%{develname}
Summary:	API in "C" for Shapefile handling
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 1 -d}
%rename %{olddevelname}

%description -n	%{develname}
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%prep
%autosetup -p1
%configure --includedir=%{_includedir}/libshp

%build
make CFLAGS="$RPM_OPT_FLAGS"
%ifarch sparc sparcv9 sparc64 ppc
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_BIG_ENDIAN -I.. -w" -C contrib
%else
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_LITTLE_ENDIAN -I.. -w" -C contrib
%endif

%install
%makeinstall_std
%makeinstall_std -C contrib

%files -n %{name}
%doc README.tree
%{_bindir}/*

%files -n %{develname}
%{_includedir}/libshp
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

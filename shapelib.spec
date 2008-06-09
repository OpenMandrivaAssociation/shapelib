%define	major 1
%define	libname %mklibname %{name} %{major}
%define	develname %mklibname %{name} -d

Summary:	API in "C" for Shapefile handling
Name:		shapelib
Version:	1.2.10
Release:	%mkrel 4
License:	LGPL MIT
Group:		Sciences/Geosciences
URL:		http://shapelib.maptools.org/
Source0:	http://shapelib.maptools.org/dl/%{name}-%{version}.tar.bz2
Patch0:		shapelib-1.2.10-gcc4-fix.patch
Patch1:		shapelib-1.2.10-mdkconf.patch
Requires:	proj >= 4.4.1
BuildRequires:	libproj-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%package -n	%{libname}
Summary:	API in "C" for Shapefile handling
Group:		System/Libraries

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

%description -n	%{develname}
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

%prep

%setup -q
%patch0 -p1 -b .gcc4
%patch1 -p1 -b .mdkconf

%build
make CFLAGS="$RPM_OPT_FLAGS"
%ifarch sparc sparcv9 sparc64 ppc
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_BIG_ENDIAN -I.. -w" -C contrib
%else
make CFLAGS="$RPM_OPT_FLAGS -DPROJ4 -D_LITTLE_ENDIAN -I.. -w" -C contrib
%endif
make lib CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m755 dbfadd dbfcreate dbfdump shpadd shpcreate shpdump shptest %{buildroot}%{_bindir}
install -m755 contrib/{dbfcat,dbfinfo,shpcat,shpcentrd,shpdata,shpdxf,shpfix,shpinfo,shpwkb,shpproj} %{buildroot}%{_bindir}

make lib_install LIB=%{_lib} DESTDIR=$RPM_BUILD_ROOT

#(peroyvind) don't care about these for now..
rm -f %{buildroot}%{_libdir}/lib*.*a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{name}
%defattr (-,root,root)
%doc README.tree dbf_api.html shapelib.html shp_api.html
%doc contrib/doc/shpproj.txt
%{_bindir}/*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/libshp/shapefil.h
%{_libdir}/*.so

%files -n %{libname}
%defattr (-,root,root)
%{_libdir}/*.so.*

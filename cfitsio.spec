%define major 4
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d
%define oldlibname %mklibname %{name} 9

%bcond_without	bzip
%bcond_without	curl
%bcond_without	utils
#FIXME: TestProg fails on znver1 arch
%bcond_with	tests
%ifarch %{x86_64}
%bcond_without	sse2
%bcond_without	ssse3
%else
%bcond_with	sse2
%bcond_with	ssse3
%endif
%bcond_without	shared

Summary:	Library for accessing files in FITS format for C and Fortran
Name:		cfitsio
Version:	4.2.0
Release:	1
Group:		System/Libraries
License:	BSD-like
Url:		https://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source0:	https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{name}-%{version}.tar.gz
#Patch0:		cfitsio-4.2.0-fix_soname.patch
Patch1:		cfitsio-4.2.0-fix_install_path.patch
# (fedora) https://src.fedoraproject.org/rpms/cfitsio/raw/rawhide/f/cfitsio-noversioncheck.patch
Patch2:		cfitsio-noversioncheck.patch
# (fedora) https://src.fedoraproject.org/rpms/cfitsio/raw/rawhide/f/cfitsio-ldflags.patch
Patch3:		cfitsio-ldflags.patch
# (fedora) https://src.fedoraproject.org/rpms/cfitsio/raw/rawhide/f/cfitsio-remove-rpath.patch
Patch4:		cfitsio-remove-rpath.patch

BuildRequires:	gcc-gfortran
%if %{with bzip}
BuildRequires:	pkgconfig(bzip2)
%endif
%if %{with curl}
BuildRequires:	pkgconfig(libcurl)
%endif
BuildRequires:	pkgconfig(zlib)

%description
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

%if %{with utils}
%files
%{_bindir}/*
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Obsoletes:	%{oldlibname} < %{EVRD}

%description -n %{libname}
This package contains the shared library for %{name}.

%files -n %{libname}
%{_libdir}/libcfitsio.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{devname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{_lib}cfitsio-static-devel

%description -n %{devname}
This package contains the headers required for compiling software that uses
the cfits library.

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# use soversion from configure
sover=$(sed -ne "s,^CFITSIO_SONAME=\(.*\)\1,,p" configure)
sed -i -e "s,@SONAME@,$sover," CMakeLists.txt

# add ldflags to configure.in
sed -e 's|LDFLAGS=.*|LDFLAGS="%{ldflags}"|g' -i configure.in

# fix cfitsio.pc.in
sed -i  \
	-e 's|includedir=@includedir@|&/cfitsio|' \
	-e 's|Libs.private:.*|& -lz |' \
 	-e 's|Cflags:|Cflags: -D_REENTRANT|' \
	cfitsio.pc.in

# fix cfitsio.pc.cmake
sed -i  \
	-e 's|Libs.private:.*|& -lz |' \
 	-e 's|Cflags:|Cflags: -D_REENTRANT|' \
	cfitsio.pc.cmake

%build
#FC=f95
#export FC
#export CC=%{__cc} # fixes -O*, -g

%cmake \
	-DBUILD_SHARED_LIBS:BOOL=%{?with_shared:ON}%{?!with_shared:OFF} \
	-DUSE_BZIP:BOOL=%{?with_bzip:ON}%{?!with_bzip:OFF} \
	-DUSE_CURL:BOOL=%{?with_curl:ON}%{?!with_curl:OFF} \
	-DUSE_PTHREADS:BOOL=ON \
	-DUSE_SSE2:BOOL=%{?with_sse2:ON}%{?!with_sse2:OFF} \
	-DUSE_SSSE3:BOOL=%{?with_ssse3:ON}%{?!with_ssse3:OFF} \
	-DUTILS:BOOL=%{?with_utils:ON}%{?!with_utils:OFF} \
	-DTESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-G Ninja
%ninja_build

#autoreconf -fiv
#configure \
#	--%{?with_curl:en}%{?!with_curl:dis}able-curl \
#	--enable-reentrant \
#	--%{?with_sse2:en}%{?!with_sse2:dis}able-sse2 \
#	--%{?with_ssse3:en}%{?!with_ssse3:dis}able-ssse3 \
#	--with%{?!with_bzip:out}-bzip2
#
#make_build \
#	%{?with_shared:shared}

#if %{with utils}
#make_build fpack
#make_build funpack
#make_build fitscopy
#make_build imcopy
#endif
#unset FC

%install
%ninja_install -C build
#make_install \
#	INCLUDEDIR=%{_includedir}/%{name} \
#	CFITSIO_LIB=%{buildroot}%{_libdir} \
#	CFITSIO_INCLUDE=%{buildroot}%{_includedir}/%{name}

%if %{with utils}
#install -Dm 0755 fpack %{buildroot}%{_bindir}/fpack
#install -Dm 0755 funpack %{buildroot}%{_bindir}/funpack
#install -Dm 0755 fitscopy %{buildroot}%{_bindir}/fitscopy
#install -Dm 0755 imcopy %{buildroot}%{_bindir}/imcopy
%endif

%if %{with shared}
#rm -f %{buildroot}%{_libdir}/*.a
%endif

%check
%if %{with tests}
export LD_LIBRARY_PATH=.
%ninja_test -C build
%endif


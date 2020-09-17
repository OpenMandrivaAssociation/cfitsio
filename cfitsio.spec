%define sversion %(echo %{version} |sed -e 's#\\.##')
%define major 5
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Library for accessing files in FITS format for C and Fortran
Name:		cfitsio
Version:	3.49
Release:	1
Group:		System/Libraries
License:	BSD-like
Url:		http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source0:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/cfitsio/raw/master/f/cfitsio-zlib.patch
Patch1:		https://src.fedoraproject.org/rpms/cfitsio/raw/master/f/cfitsio-noversioncheck.patch
Patch2:		https://src.fedoraproject.org/rpms/cfitsio/raw/master/f/cfitsio-sformat.patch
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(bzip2)
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

%package -n %{libname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries

%description -n %{libname}
This package contains the shared library for %{name}.

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

%prep
%autosetup -p1

# remove bundled zlib
# not all the files inside zlib belong to zlib
cd zlib
    rm adler32.c crc32.c deflate.c infback.c inffast.c inflate.c inflate.h \
    inftrees.c inftrees.h zlib.h deflate.h trees.c trees.h uncompr.c zconf.h \
    zutil.c zutil.h crc32.h  inffast.h  inffixed.h 
cd ..

sed -e 's|LDFLAGS=.*|LDFLAGS="%{build_ldflags}"|g' -i configure.in
autoreconf -fi

sed -e 's|includedir=@includedir@|includedir=@includedir@/cfitsio|' -i cfitsio.pc.in
sed -e 's|Libs.private:.*|Libs.private: @LIBS@ -lz -lm|' -i cfitsio.pc.in
sed -e 's|Cflags: -I${includedir}|Cflags: -D_REENTRANT -I${includedir}|' -i cfitsio.pc.in

%build
FC=f95
export FC
export CC=%{__cc} # fixes -O*, -g

%configure \
    %ifarch %{x86_64}
	--enable-sse2 \
    %endif
	--enable-reentrant \
	--with-bzip2

%make_build shared
%make_build fpack
%make_build funpack
%make_build fitscopy
%make_build imcopy
unset FC

%check
# disable for now..
exit 0
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std

%install
%make_install
install -D -m755 fpack %{buildroot}%{_bindir}/fpack
install -D -m755 funpack %{buildroot}%{_bindir}/funpack
install -D -m755 fitscopy %{buildroot}%{_bindir}/fitscopy
install -D -m755 imcopy %{buildroot}%{_bindir}/imcopy

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libcfitsio.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

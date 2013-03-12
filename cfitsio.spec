%define	sversion %(echo %{version} |sed -e 's#\\.##')
%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Summary:	Library for accessing files in FITS format for C and Fortran
Name:		cfitsio
Version:	3.310
Release:	2
Patch0:		cfitsio.patch
Group:		System/Libraries
License:	BSD-like
Url:		http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source0:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sversion}.tar.gz
BuildRequires:	gcc-gfortran

%description
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

%package -n	%{libname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries

%description -n	%{libname}
This package contains the share library for %{name}.

%package -n	%{devname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{_lib}cfitsio-static-devel

%description -n	%{devname}
This package contains the headers required for compiling software that uses
the cfits library.

%prep
%setup -qn %{name}
%apply_patches

sed -e 's|includedir=@includedir@|includedir=@includedir@/cfitsio|' -i cfitsio.pc.in
sed -e 's|Libs: -L${libdir} -lcfitsio @LIBS@|Libs: -L${libdir} -lcfitsio|' -i cfitsio.pc.in
sed -e 's|Libs.private: -lm|Libs.private: @LIBS@ -lz -lm|' -i cfitsio.pc.in 
sed -e 's|Cflags: -I${includedir}|Cflags: -D_REENTRANT -I${includedir}|' -i cfitsio.pc.in

%build
FC=f95
export FC
export CC=gcc # fixes -O*, -g
%configure2_5x	\
	--enable-reentrant
%make shared
ln -s libcfitsio.so.0 libcfitsio.so
%make fpack
%make funpack
unset FC

%check
# disable for now..
exit 0
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std

%install
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
make LIBDIR=%{_lib} INCLUDEDIR=include/%{name} CFITSIO_LIB=%{buildroot}%{_libdir} \
     CFITSIO_INCLUDE=%{buildroot}%{_includedir}/%{name} install
pushd %{buildroot}%{_libdir}
ln -s libcfitsio.so.0 libcfitsio.so
popd
mkdir %{buildroot}%{_bindir}
cp -p f{,un}pack %{buildroot}%{_bindir}/

rm -f %{buildroot}%{_libdir}/*.a

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libcfitsio.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*


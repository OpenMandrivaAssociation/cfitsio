%define sversion %(echo %version |sed -e 's#\\.##')
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %name -d
%define develnamestatic %mklibname %name -d -s

Name: cfitsio
Version: 3.250
Release: %mkrel 1
URL:	http://heasarc.gsfc.nasa.gov/docs/software/fitsio/
Source:	ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/%{name}%{sversion}.tar.gz
Patch0:         cfitsio.patch
Patch1:         cfitsio-pkgconfig.patch
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
License: BSD-like
Summary: Library for accessing files in FITS format for C and Fortran
Group:	 	 System/Libraries
Obsoletes:	%{_lib}%{name} < 3.090

%description -n %{libname}

CFITSIO is a library of C and Fortran subroutines for reading and
writing data files in FITS (Flexible Image Transport System) data
format.  CFITSIO simplifies the task of writing software that deals
with FITS files by providing an easy to use set of high-level routines
that insulate the programmer from the internal complexities of the
FITS file format.  At the same time, CFITSIO provides many advanced
features that have made it the most widely used FITS file programming
interface in the astronomical community.  This package contains the
shared library required by prgrams that use the cfits library.

%package -n %{develname}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Provides:	fitsio-devel = %{version} 
Provides:   cfitsio-devel = %{version}
Requires:   pkgconfig
Requires:   %libname = %version
Conflicts:	%{_lib}%{name} < 3.090

%description -n %{develname}
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

This package contains the headers required for compiling software that uses
the cfits library.

%package -n %{develnamestatic}
License:	BSD-like
Summary:	Library for accessing files in FITS format for C and Fortran
Group:		System/Libraries
Requires:   %{develname}
Requires:   %libname = %version

%description -n %{develnamestatic}
CFITSIO is a library of C and Fortran subroutines for reading and 
writing data files in FITS (Flexible Image Transport System) data format. 
CFITSIO simplifies the task of writing software that deals with FITS 
files by providing an easy to use set of high-level routines that insulate 
the programmer from the internal complexities of the FITS file format. 
At the same time, CFITSIO provides many advanced features that have made 
it the most widely used FITS file programming interface in the astronomical 
community.

This package contains the headers required for compiling software that uses
the cfits library.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
FC=f95
export FC
export CC=gcc # fixes -O*, -g
%configure2_5x
%make shared
ln -s libcfitsio.so.0 libcfitsio.so
%make fpack
%make funpack
unset FC
# Manually fix pkgconfig .pc file (BZ 436539, BZ 618291)
sed 's|/usr/include|/usr/include/%{name}|' cfitsio.pc >cfitsio.pc.new
mv cfitsio.pc.new cfitsio.pc

%check
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std

%install
rm -rf %{buildroot}
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
%clean
rm -Rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n %{develnamestatic}
%defattr(-,root,root)
%{_libdir}/*.a


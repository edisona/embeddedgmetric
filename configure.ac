AC_INIT(embeddedgmetric, [v1.0.0], [nickg -at- modp -dot- com])
AC_PREREQ(2.59)
AM_INIT_AUTOMAKE
AM_CONFIG_HEADER(config.h)
AC_CONFIG_SRCDIR(src)

AC_PROG_CC
AC_PROG_LIBTOOL
AC_CHECK_FUNCS([memset memcpy htons gethostbyname socket sendto xdr_u_int xdr_string xdr_enum xdrmem_create])
AC_ARG_ENABLE(gcov, AC_HELP_STRING([--enable-gcov],[turn on code coverage analysis tools]))

EXTRACFLAGS="-Wall -Werror -I. -Isrc"

if test "x$enable_gcov" = "xyes";
then
    EXTRACFLAGS="$EXTRACFLAGS -fprofile-arcs -ftest-coverage"
    dnl Turn off optimization so code coverage tool
    dnl can get accurate line numbers
    CFLAGS=`echo "$EXTRACFLAGS" | sed -e 's/-O[0-9]*//g'`
fi
CFLAGS="$EXTRACFLAGS $CFLAGS"

AC_CONFIG_FILES([
	Makefile
	python/Makefile
	 ])

AC_PROG_MAKE_SET
AC_OUTPUT
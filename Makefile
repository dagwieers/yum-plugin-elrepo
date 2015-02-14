prefix=/usr
libdir=$(prefix)/lib
sysconfdir=/etc
plugindir=$(libdir)/yum-plugins
pluginconfdir=$(sysconfdir)/yum/pluginconf.d
DESTDIR=

all:
	@echo "Nothing to do."

install:
	-[[ ! -f $(DESTDIR)$(pluginconfdir)/elrepo.conf ]] && install -Dp -m0644 elrepo.conf $(DESTDIR)$(pluginconfdir)/elrepo.conf
	install -Dp -m0644 elrepo.py $(DESTDIR)$(plugindir)/elrepo.py

#syntax=docker/dockerfile:1
ARG CPUARCH=x86_64
ARG GCC_VERSION="11.2.0"

FROM quay.io/pypa/musllinux_1_1_${CPUARCH}:2024-03-10-4935fcc as build
ARG CPUARCH
ARG GCC_VERSION

RUN apk add --no-cache make build-base git
RUN <<-EOF
	set -euxo pipefail

	apk add --no-cache make build-base git
	git clone https://github.com/richfelker/musl-cross-make /root/musl-cross-make
	cd /root/musl-cross-make
	git checkout 678797f0625ea9e7a74aebdc0b7d2afcf3d66e07
EOF

WORKDIR /root/musl-cross-make
RUN <<-EOF
	set -euxo pipefail

	# Write config.mak
	MUSL_VERSION=$( (/lib/libc.musl-$CPUARCH.so.1 2>&1 || true) | grep "Version" | cut -d " " -f2)

	cat <<-EOF2 > config.mak
		TARGET = $CPUARCH-linux-musl
		OUTPUT = /opt/gcc-$GCC_VERSION

		GCC_VER = $GCC_VERSION
		MUSL_VER = git-v$MUSL_VERSION
	EOF2
EOF

RUN <<-EOF
	set -euxo pipefail

	make -j $(expr $(nproc) + 2)
	make install
EOF

FROM quay.io/pypa/musllinux_1_1_${CPUARCH}:2024-03-10-4935fcc
ARG CPUARCH
ARG GCC_VERSION

COPY --from=build /opt/gcc-$GCC_VERSION /opt/gcc-$GCC_VERSION
RUN <<-EOF
	set -euxo pipefail

	# Symlink each of /opt/gcc-.../bin/$CPUARCH-linux-musl-[EXE] to /usr/local/bin/[EXE]
	cd /opt/gcc-$GCC_VERSION/bin
	ls | xargs -I {} sh -c "ln -s $PWD/{} /usr/local/bin/\$(echo {} | sed -e s/^$CPUARCH-linux-musl-//)"
EOF

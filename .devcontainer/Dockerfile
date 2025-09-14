FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive
RUN cat <<-"EOF" > /etc/apt/apt.conf.d/99-local
	APT::Get::Assume-Yes "true";
	APT::Install-Suggests "false";
EOF

# Will also do apt update
RUN yes | unminimize
RUN apt-get install

# CMake
RUN bash <<-"EOF"
	set -euxo pipefail
	# See also: https://apt.kitware.com/

	apt-get install ca-certificates gpg curl
	test -f /usr/share/doc/kitware-archive-keyring/copyright ||
	curl -L https://apt.kitware.com/keys/kitware-archive-latest.asc \
		| gpg --dearmor - \
		> /usr/share/keyrings/kitware-archive-keyring.gpg
	echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ noble main' \
		> /etc/apt/sources.list.d/kitware.list
	apt-get update
	test -f /usr/share/doc/kitware-archive-keyring/copyright \
		|| rm /usr/share/keyrings/kitware-archive-keyring.gpg
	apt-get install kitware-archive-keyring
	apt-get install cmake
EOF

# Git
RUN bash <<-"EOF"
	set -euxo pipefail

	apt-get install software-properties-common
	add-apt-repository ppa:git-core/ppa
	apt-get update
	apt-get install git
EOF

# C++
RUN apt-get install clang clang-tools  # Compilers
RUN apt-get install curl zip unzip tar pkg-config make  # Vcpkg deps
RUN apt-get install ninja-build

# Python
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# VS Code extension support
RUN add-apt-repository ppa:dotnet/backports
RUN apt-get update
RUN apt-get install dotnet-sdk-9.0

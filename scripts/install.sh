# Build Release configuration and install it in the default cmake prefix path.
cmake --build "build" --config Release &&
cmake --install "build" --prefix ~/.local --config Release
from setuptools import setup
from rust_ext import build_rust_cmdclass, install_lib_including_rust

setup(
    name = 'libsarkara',
    version = '0.1.1',
    description = "sarkara simple python api.",
    url = "https://github.com/quininer/python-sarkara-simple",
    author = "quininer kel",
    author_email = "quininer@live.com",
    license = "MIT",
    cmdclass = {
        'build_rust': build_rust_cmdclass('libsarkara/Cargo.toml'),
        'install_lib': install_lib_including_rust
    },
    packages = ['libsarkara'],
    zip_safe=False,
    libraries = [
        ("libsarkara", {
            "sources": [
                "libsarkara/Cargo.toml",
                "libsarkara/src/lib.rs",
                "libsarkara/src/macros.rs"
            ]
        })
    ]
)

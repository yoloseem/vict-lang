try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="Vict-lang",
    version="0.1",
    url="http://github.com/kimjayd/vict-lang",
    license="MIT",
    author="Kim Hyunjun",
    author_email="kim@hyunjun.kr",
    description="Vict programming language",
    packages=["vict",],
    install_requires=["lepl",],
)

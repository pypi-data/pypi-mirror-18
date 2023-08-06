from setuptools import setup


setup(
    name='bearsh',
    description="IPython shell extension for coala",
    author="Stefan Zimmermann",
    author_email="user@zimmermann.co",

    license='AGPLv3',

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    install_requires=['coala', 'coala-bears'],

    packages=['bearsh'],
)

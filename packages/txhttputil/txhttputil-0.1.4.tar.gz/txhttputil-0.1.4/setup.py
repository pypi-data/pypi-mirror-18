from distutils.core import setup

setup(
    name='txhttputil',
    packages=['txhttputil', 'txhttputil.downloader', 'txhttputil.login_page', 'txhttputil.site', 'txhttputil.util'],
    package_data={'txhttputil.login_page': ['*.xml']},
    version='0.1.4',
    description='Synerty utility classes for serving a static site with twisted.web with user permissions.',
    author='Synerty',
    author_email='contact@synerty.com',
    url='https://github.com/Synerty/txhttputil',
    download_url='https://github.com/Synerty/txhttputil/tarball/0.1.4',
    keywords=['twisted', 'resource', 'file', 'download', 'synerty'],
    classifiers=[],
)

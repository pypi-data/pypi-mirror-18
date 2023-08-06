from distutils.core import setup

setup(
    name='xenon_player',
    packages=['xenon_player'],  # this must be the same as the name above
    version='0.1.2',
    description='Xenon Player based on mplayer & mplayer.py',
    author='minus79',
    author_email='gergely06@gmail.com',
    url='https://github.com/minus79/xenon_player',  # use the URL to the github repo
    download_url='https://github.com/minus79/xenon_player/tarball/0.1',  # I'll explain this in a second
    keywords=['xenon', 'xenon-player', 'xenon_player'],  # arbitrary keywords
    install_requires=[
        'xenon_tools', 'mplayer.py',
    ],
    classifiers=[],
)

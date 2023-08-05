from setuptools import setup

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='twitterbymb',
    version='0.5.2',
    description='Simple console and web Twitter wall',
    author='Marek Bertovic',
    author_email='mb.bertovic@gmail.com',
    license='Public Domain',
    url='https://github.com/marekbert/MI-PYP1',
    packages=['twitterbymb'],
    package_data={'twitterbymb': ['templates/*.html']},
    include_package_data=True,
    zip_safe = False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=['Flask', 'click>=6','requests>2.10','Jinja2>=2.8'],
    entry_points={
        'console_scripts':[
            'ultimatetwitter=twitterbymb.twitwall:main'
        ]
    }
)

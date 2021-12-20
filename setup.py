from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='0.0.4',
    license='',
    author='gilyuliiy',
    author_email='',
    url='',
    packages=find_packages(),
    scripts = ['package/rss_reader.py'],
    entry_points={
        'console_scripts': [
            'rss_reader=package.rss_reader:run_rss_reader'
        ]
    },
    install_requires=[
        'requests',
        'feedparser',
        'argparse',
        'pandas'
    ],
    description="Yet another Pytohn RSS Readyer by gilyuliiy",
)
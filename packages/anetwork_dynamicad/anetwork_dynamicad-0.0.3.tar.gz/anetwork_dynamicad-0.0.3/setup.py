from distutils.core import setup

from Anetwork import DynamicAd

setup(
    name=DynamicAd.__title__,
    packages=['Anetwork', 'Anetwork.DynamicAd'],
    version=DynamicAd.__version__,
    description=DynamicAd.__summary__,
    author=DynamicAd.__author__,
    author_email=DynamicAd.__email__,
    url=DynamicAd.__uri__,
    download_url='',
    keywords=['Anetwork', 'anetwork', 'campaign', 'DynamicAd'],
    requires=['requests']
)

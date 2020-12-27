from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", mode='r') as req:
        req_text = req.read()

    req_list = req_text.split('\n')

    return req_list


setup(
    name='csvcli',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        csvcli=csvcli.cli:cli
    '''
)
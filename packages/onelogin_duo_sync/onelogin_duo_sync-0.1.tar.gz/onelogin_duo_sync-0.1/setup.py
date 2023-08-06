from setuptools import setup

setup(name="onelogin_duo_sync",
        version='0.1',
        description='simple script to mirror OneLogin users and groups to Duo',
        url='https://github.com/ottiferous/OneLogin-Duo-Sync',
        author='Andrew Marrone',
        author_email='nope@nope.com',
        license='MIT',
        packages=['onelogin_duo_sync'],
        install_requires=[
            'requests',
            'duo_client'
        ],
        zip_safe=False)

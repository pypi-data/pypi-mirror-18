from setuptools import find_packages, setup

def get_readme():
    readme = ''
    try:
        import pypandoc
        readme = pypandoc.convert('README.md', 'rst')
    except (ImportError, IOError):
        with open('README.md', 'r') as file_data:
            readme = file_data.read()
    return readme

setup(
        name='number2name_es',
	    version='1.0.0',
	    description='Transform numbers digits to numbers in words',
        long_description=get_readme(),
	    url='https://github.com/dpineiden/number2name',
	    author='David Pineda Osorio',
	    author_email='dahalpi@gmail.com',
	    license='MIT',
	    classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'License :: OSI Approved :: MIT License',],
        keywords='numbers words',
        packages=find_packages(),
        install_requires=['markdown==2.6.5'],
        package_data={
            #'sample': ['package_data.dat'],
        },
)



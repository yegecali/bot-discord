"""
Setup.py para BotPersonal
"""
from setuptools import setup, find_packages
from pathlib import Path

# Leer versión desde archivo
version_file = Path(__file__).parent / 'VERSION'
version = version_file.read_text().strip()

# Leer README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='BotPersonal',
    version=version,
    description='Bot de Discord para gestión de gastos con OCR de facturas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tu Nombre',
    author_email='tu.email@example.com',
    url='https://github.com/tuusuario/BotPersonal',
    license='MIT',
    packages=find_packages(where='src') + find_packages(where='.', include=['tests']),
    package_dir={
        '': '.',
        'src': 'src',
    },
    include_package_data=True,
    install_requires=[
        'discord.py>=2.3.0',
        'SQLAlchemy>=2.0.0',
        'Flask>=2.3.0',
        'python-dotenv>=1.0.0',
        'Pillow>=10.0.0',
        'pytesseract>=0.3.10',
        'requests>=2.31.0',
        'PyNaCl>=1.5.0',
        'Jinja2>=3.1.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=7.0.0',
            'pytest-asyncio>=0.21.0',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications :: Chat',
    ],
    entry_points={
        'console_scripts': [
            'botpersonal=main:main',
        ],
    },
)


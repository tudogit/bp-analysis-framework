from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bp-analysis-framework',
    version='1.0.0',
    description='Complete Business Process Analysis Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='BP Analysis Team',
    author_email='team@bp-analysis.dev',
    url='https://github.com/tudogit/bp-analysis-framework',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'sqlalchemy>=1.4.0',
        'plotly>=5.0.0',
        'psycopg2-binary>=2.9.0',
        'python-dotenv>=0.19.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Business/Enterprise',
        'Topic :: Office/Business',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='business process mining analysis workflow',
)

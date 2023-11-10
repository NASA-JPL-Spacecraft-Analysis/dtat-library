"""Basic setup for the application"""

from setuptools import setup

setup(
    name="dtat",
    description="Data Trending and Analysis Tool",
    author="Europa FSPA",
    author_email="europa_fspa_sw@jpl.nasa.gov",
    url="https://github.jpl.nasa.gov/Europa-PESS",
    version="0.0.1",
    python_requires="~=3.10",
    install_requires=[
        #dash>=2.2.0
        #dash-core-components>=2.0.0
        #dash-html-components>=2.0.0
        #dash-renderer>=1.5.1
        #flask>=2.2.2
        'pandas',
        'plotly',
        #pymysql>=0.9.3
        #sd_material_ui>=4.6.0
        #werkzeug>=0.15.6
        #sd_material_ui
        'setuptools'
        #requests~=2.25
        #boto3~=1.20
        #typing-extensions~=4.0
    ]
)

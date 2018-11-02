import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_graph_api",
    version="1.0.0",
    author="Sir Jayesh",
    author_email="sirjayesh1@gmail.com",
    description="A project to connect to your Microsoft Graph Explorer registered in Microsoft Azure AD. Register your app in azure portal and configure the details in config.py file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sirjayesh/flask-graph-api",
    packages=setuptools.find_packages(),
	install_requires=[
          'flask',
		  'simplejson',
		  'flask_jsonpify',
		  'requests'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
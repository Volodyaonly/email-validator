from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-validator-tool",
    version="1.0.0",
    author="Volodyaonly",
    author_email="volodyaovsannikov15@gmail.com",
    description="Professional email validator with MX records check and Telegram integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Volodyaonly/email-validator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "dnspython>=2.3.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "email-validator=src.check_email:main",
            "telegram-sender=src.telegram_sender:send_to_telegram",
        ],
    },
)

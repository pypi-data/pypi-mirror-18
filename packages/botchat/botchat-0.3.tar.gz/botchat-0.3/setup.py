from setuptools import setup

setup(name='botchat',
      version='0.3',
      description='Let a bot chat on your behalf on whatsapp',
      url='https://github.com/lakshaykalbhor/Whatsapp-BotChat',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages=['botchat'],
      install_requires=[
          'selenium',
          'bs4',
      ],
      entry_points={
        'console_scripts': ['botchat=botchat.command_line:main'],
      },
      zip_safe=False
      )
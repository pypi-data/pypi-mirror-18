from setuptools import setup

setup(name='pymono',
      version='1.0.2',
      description='Monopoly game built with Python 3 & Cocos2d',
      url='https://github.com/MrKomish/Monopoly',
      author='Michael Konviser',
      author_email='misha.konviser@gmail.com',
      license='MIT',
      packages=['pymono',
                'pymono.controllers',
                'pymono.data',
                'pymono.models',
                'pymono.lib',
                'pymono.res',
                'pymono.views'],
      install_requires=['cocos2d', 'pyglet'],
      keywords=['monopoly', 'game', 'board', 'pymono', 'mono']
      )

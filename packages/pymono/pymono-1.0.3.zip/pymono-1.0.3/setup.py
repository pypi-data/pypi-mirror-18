from setuptools import setup

setup(name='pymono',
      version='1.0.3',
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
      keywords=['monopoly', 'game', 'board', 'pymono', 'mono'],
	  package_data={
		'pymono/res': [
			'pymono/res/dice1.png',
			'pymono/res/dice2.png',
			'pymono/res/dice3.png',
			'pymono/res/dice4.png',
			'pymono/res/dice5.png',
			'pymono/res/dice6.png',
			'pymono/res/diceNone.png',
			'pymono/res/dice_sides.jpeg',
			'pymono/res/Monopoly.png',
			'pymono/res/Monopoly-1000px.png'
		],
		'pymono/res/dots': [
			'pymono/res/dots/green.png',
			'pymono/res/dots/red.png',
			'pymono/res/dots/green.png',
			'pymono/res/dots/yellow.png'
		]
	  }
      )

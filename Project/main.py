from kivy.config import Config 
# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', False) 
  
# fix the width of the window  
Config.set('graphics', 'width', '1194') 
  
# fix the height of the window  
Config.set('graphics', 'height', '834') 

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, Ellipse, Line
from kivy.core.text import FontContextManager as FCM

import numpy as np
import cv2
from collections import deque
Window.clearcolor = (1, 1, 1, 1)


class MainPage(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.title = Label(text="Interactive Flash Cards", size_hint=(0.75, 0.10), pos_hint={'x': 0.125, 'y': 0.75}, color=[0, 0, 0, 1], valign='middle', halign='center', font_size=64, font_name='RobotoMono-Regular')
		self.add_widget(self.title)

		self.start_button = Button(text="▶️Start Game◀️", size_hint=(0.25, 0.08), pos_hint={'x': 0.375, 'y': 0.4}, background_color=[1., 0.404, 0., 1.], background_normal='', valign='middle', halign='center', font_size=36, font_name='DejaVuSans')
		self.add_widget(self.start_button)

		self.settings_button = Button(text="⚙️Settings⚙", size_hint=(0.25, 0.08), pos_hint={'x': 0.375, 'y': 0.3}, background_color=[1., 0.404, 0., 1.], background_normal='', valign='middle', halign='center', font_size=36, font_name='DejaVuSans')
		self.add_widget(self.settings_button)

		self.author_name = Label(text="Made by Prudhviraj Naidu", size_hint=(0.20, 0.03), pos_hint={'x': 0.4, 'y': 0.1}, color=[0, 0, 0, 1], valign='middle', halign='center', font_size=18, font_name='RobotoMono-Regular')
		self.add_widget(self.author_name)


class PaintWidget(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.size_hint = (0.75, 0.75)
		self.pos_hint= {'x':.25, 'y':.25}

		self.cv2_canvas = None

	def on_touch_down(self, touch):
		
		if self.cv2_canvas is None:
			self.cv2_canvas = np.ones((int(self.size[1]), int(self.size[0])), dtype=np.uint8) * 255

		if self.collide_point(touch.x, touch.y):
			with self.canvas:
				Color(0, 0, 0)
				d = 30.
				# Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
				touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)
				

				# print(int(touch.x - self.x))
				# print(int(touch.y - self.y))
				# cv2.circle(self.cv2_canvas, (int(touch.x - self.x), int(self.height - int(touch.y - self.y))), 17, (0, 0, 0), -1)
				# cv2.imwrite('h1.png', self.cv2_canvas)

	def on_touch_move(self, touch):
		if self.collide_point(touch.x, touch.y):
			touch.ud['line'].points += [touch.x, touch.y]

	def on_touch_up(self, touch):
		if self.collide_point(touch.x, touch.y):
			pts = touch.ud['line'].points
			line_points = np.array([[int(pts[i] - self.x), int(self.height - pts[i+1] + self.y)] for i in range(0, len(pts), 2)], dtype=np.int32)

			cv2.polylines(self.cv2_canvas, [line_points], isClosed=False, color=(0, 0, 0), thickness=10)
			cv2.imwrite('h1.png', self.cv2_canvas)



class SelectLanguage(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.title = Label(text="Select Language", size_hint=(0.75, 0.10), pos_hint={'x': 0.125, 'y': 0.75}, color=[0, 0, 0, 1], valign='middle', halign='center', font_size=64, font_name='RobotoMono-Regular')
		self.add_widget(self.title)

		self.english = Button(text="English", size_hint=(0.25, 0.08), pos_hint={'x': 0.375, 'y': 0.4}, background_color=[1., 0.404, 0., 1.], background_normal='', valign='middle', halign='center', font_size=36, font_name='DejaVuSans')
		self.add_widget(self.english)

		self.hindi = Button(text="िहंदी", size_hint=(0.25, 0.08), pos_hint={'x': 0.375, 'y': 0.3}, background_color=[1., 0.404, 0., 1.], background_normal='', valign='middle', halign='center', font_size=36, font_name='NotoSans-Regular.ttf')
		self.add_widget(self.hindi)

		self.return_button = Button(size_hint=(0.03, 0.04), pos_hint={'x': 0.02, 'y': 0.02}, background_normal='baseline_arrow_back_ios_black_18dp.png', background_down='baseline_arrow_back_ios_black_18dp.png')
		# return_Image = Image(source='')
		# self.return_button.add_widget(return_Image, size_hint)

		self.add_widget(self.return_button)

class CanvasPage(FloatLayout):
	def __init__(self, text='Tree', current_score=0, total_score=2, **kwargs):
		super().__init__(**kwargs)

		self.title = Label(text=f"Draw: [u]{text}[/u]", markup=True, size_hint=(0.4, 0.10), pos_hint={'x': 0.3, 'y': 0.9}, color=[0, 0, 0, 1], valign='middle', halign='center', font_size=64, font_name='RobotoMono-Regular')
		self.add_widget(self.title)

		self.score = Label(text=f"Score: {current_score}/{total_score}", markup=False, size_hint=(0.08, 0.06), pos_hint={'x': 0.85, 'y': 0.92}, color=[0, 0, 0, 1], valign='middle', halign='center', font_size=36, font_name='RobotoMono-Regular')
		self.add_widget(self.score)

		self.paint_widget = PaintWidget()
		self.add_widget(self.paint_widget)
		


class MainApp(App):
	def build(self):
		return CanvasPage()

if __name__ == '__main__':
	MainApp().run()
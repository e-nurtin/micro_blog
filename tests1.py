import os

os.environ['DATABASE_URL'] = 'sqlite://'

from flask import current_app
from datetime import datetime, timedelta
from unittest import TestCase, main
from app import db
from app.models import User, Post


class UserModelCase(TestCase):
	def setUp(self):
		self.app_context = current_app.app_context()
		self.app_context.push()
		db.create_all()
	
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
	
	def test_password_hashing(self):
		u = User(username='mathew')
		u.set_password('pass')
		self.assertFalse(u.check_password('false'))
		self.assertTrue(u.check_password('pass'))
	
	def test_avatar(self):
		u = User(username='emily', email='emily@example.com')
		expected = 'https://www.gravatar.com/avatar/6695238d137b7f2c818f76d1c67dbcbb?d=identicon&s=128'
		self.assertEqual(expected, u.avatar(128))
	
	def test_follow(self):
		u1 = User(username='mathew', email='mathew@example.com')
		u2 = User(username='emily', email='emily@example.com')
		
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		
		self.assertEqual([], u1.followed.all())
		self.assertEqual([], u2.followed.all())
		
		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(1, u1.followed.count())
		self.assertEqual('emily', u1.followed.first().username)
		self.assertEqual(1, u2.followers.count())
		self.assertEqual('mathew', u2.followers.first().username)
		
		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(0, u1.followed.count())
		self.assertEqual(0, u2.followers.count())
	
	def test_follow_posts(self):
		# arrange users
		u1 = User(username='mathew', email='mathew@example.com')
		u2 = User(username='emily', email='emily@example.com')
		u3 = User(username='george', email='george@example.com')
		u4 = User(username='billy', email='billy@example.com')
		
		db.session.add_all([u1, u2, u3, u4])
		
		# arrange posts
		now = datetime.utcnow()
		p1 = Post(body='mathew posted this', author=u1, timestamp=now + timedelta(seconds=1))
		p2 = Post(body='emily posted this', author=u2, timestamp=now + timedelta(seconds=4))
		p3 = Post(body='george posted this', author=u3, timestamp=now + timedelta(seconds=3))
		p4 = Post(body='billy posted this', author=u4, timestamp=now + timedelta(seconds=2))
		
		db.session.add_all([p1, p2, p3, p4])
		db.session.commit()
		
		# arrange follows
		u1.follow(u2)  # mathew follows emily
		u1.follow(u4)  # mathew follows billy
		u2.follow(u3)  # emily follows george
		u3.follow(u4)  # george follows billy
		
		db.session.commit()
		
		# Assert that the result is correct
		self.assertEqual([p2, p4, p1], u1.followed_posts().all())
		self.assertEqual([p2, p3], u2.followed_posts().all())
		self.assertEqual([p3, p4], u3.followed_posts().all())
		self.assertEqual([p4], u4.followed_posts().all())


if __name__ == '__main__':
	main(verbosity=2)

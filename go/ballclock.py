#!/usr/bin/python
#Author: Mike Parmer
from sys import argv,exit
"""
- Operation of the Ball Clock -
Every minute, the least recently used ball is removed from the queue of balls at the bottom of the clock, elevated, then deposited on the minute indicator track, which is able to hold four balls. When a fifth ball rolls on to the minute indicator track, its weight causes the track to tilt. The four balls already on the track run back down to join the queue of balls waiting at the bottom in reverse order of their original addition to the minutes track. The fifth ball, which caused the tilt, rolls on down to the five-minute indicator track. This track holds eleven balls. The twelfth ball carried over from the minutes causes the five-minute track to tilt, returning the eleven balls to the queue, again in reverse order of their addition. The twelfth ball rolls down to the hour indicator. The hour indicator also holds eleven balls, but has one extra fixed ball which is always present so that counting the balls in the hour indicator will yield an hour in the range one to twelve. The twelfth ball carried over from the five-minute indicator causes the hour indicator to tilt, returning the eleven free balls to the queue, in reverse order, before the twelfth ball itself also returns to the queue.

- Guidelines - 
The exercise should be completed in Golang. You are welcome to do it in multiple languages to show appitude, but we would like to see the test in Go.

No permutation or LCM algorithms are allowed.  A full simulation is required. Please ensure that your code moves each ball.

- Implementation -

Valid numbers are in the range 27 to 127.

Clocks must support two modes of computation.

The first mode takes a single parameter specifying the number of balls and reports the number of balls given in the input and the number of days (24-hour periods) which elapse before the clock returns to its initial ordering.

  Sample Input
  30
  45

  Output for the Sample Input
  30 balls cycle after 15 days.
  45 balls cycle after 378 days.

The second mode takes two parameters, the number of balls and the number of minutes to run for.  If the number of minutes is specified, the clock must run to the number of minutes and report the state of the tracks at that point in a JSON format.

  Sample Input
  30 325

  Output for the Sample Input
  {"Min":[],"FiveMin":[22,13,25,3,7],"Hour":[6,12,17,4,15],"Main"
  [11,5,26,18,2,30,19,8,24,10,29,20,16,21,28,1,23,14,27,9]}




"""

class ballclock:
	def __init__(self,balls=27,minutes=''):
		self.pool = [] #min 27, max 127
		self.pool_orig = [] # original pool picure
		self.min = [] #max = 4
		self.five_min = [] #max = 11
		self.hour = [] #max = 11
		self.bc_run_time = 0
		self.minutes = minutes
		self.balls = balls
		#print "balls = %s, minutes = %s" % (balls,minutes)
		self.load(balls)
		self.main()


	# set up the pool and a copy of the original pool
	def load(self,balls):
		for i in range(balls):
			i = i+1
			self.pool.append(i)
			self.pool_orig.append(i)
		self.pool.reverse()
		self.pool_orig.reverse()

		
	# run the program
	def main(self):
		#start the cycle so that our while condition will work
		self.min.append(self.pool.pop())
		self.bc_run_time = 1
		
		if not self.minutes: #if only the number of balls is specified
			while self.pool != self.pool_orig: #run until the pool repeats itself
				self.min_queue(self.pool.pop())
				self.bc_run_time += 1
			days = self.bc_run_time / 1440
			print "%s balls cycle after %s days" % (self.balls,days)
		else:
			while self.bc_run_time != self.minutes:
				self.min_queue(self.pool.pop())
				self.bc_run_time += 1
			json = {"Min":self.min,"FiveMin":self.five_min,"Hour":self.hour,"Main":self.pool}
			print json


	
	def min_queue(self,ball):
			if len(self.min) < 4:
				self.min.append(ball)
			else:
				self.min.extend(self.pool)
				self.pool = self.min
				self.min = []
				self.five_queue(ball)


	def	five_queue(self,ball):
		if len(self.five_min) < 11:
			self.five_min.append(ball)
		else:
			self.five_min.extend(self.pool)
			self.pool = self.five_min
			self.five_min = []
			self.hour_queue(ball)


	def hour_queue(self,ball):
		if len(self.hour) < 11:
			self.hour.append(ball)
		else:
			newpool = [ball]
			newpool.extend(self.hour)
			newpool.extend(self.pool)
			self.pool = newpool
			self.hour = []
			#print self.pool


if __name__ == "__main__":
# this program takes 2 sets of args, 1: just a number of balls between 27-127
# 2: a number of balls between 27-127, and a number of minutes to run
	balls = 0
	minutes = ''
	if len(argv) < 2:
		print "You must supply at least a number of balls, and/or a number of minutes to run.  Valid ball numbers are 27-127"
		exit(0)
	try:
		balls = int(argv[1])
	except:
		print "The ball clock requires at least one number for the number of balls. Valid numbers are 27-127"
		exit(0)
	if 27 > balls or 127 < balls:
		print "%s is an invalid number. Valid numbers are 27-127" % argv[1]
		exit(0)
	try:
		if len(argv) > 2:
			minutes = int(argv[2])
	except:
		print "%s is an invalid number of minutes." % argv[2]
		exit(0)
		
	ballclock(balls,minutes)


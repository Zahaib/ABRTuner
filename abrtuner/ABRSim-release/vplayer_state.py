#!/usr/bin/python

import time
import sys
import collections
import numpy as np
import config
from algorithms import *

class State:
	def __init__(self, config, trace_file):
		self.trace_file = trace_file
		self.SIMULATION_STEP = config.SIMULATION_STEP
		self.CHUNKSIZE = config.CHUNKSIZE
		self.TOTAL_CHUNKS = config.TOTAL_CHUNKS

		self.candidateBR, \
		self.playtimems, \
		self.sessiontimems, \
		self.bitrate_groundtruth, \
		self.bufftimems, \
		self.BR, \
		self.bwArray = self._ParseTrace(config, trace_file)

		self.jointime = 0
		self.BLEN = 0
		self.CHUNKS_DOWNLOADED = 0
		self.BUFFTIME = 0
		self.PLAYTIME = 0
		self.CANONICAL_TIME = 0
		self.CLOCK = self.jointime
		self.BR = 0
		self.BW = 0
		self.AVG_SESSION_BITRATE = 0
		self.SWITCH_LOCK = 0
		self.ATTEMPT_ID = 0
		self.sessionHistory = dict()
		self.sessionHistory[0] = [self.jointime]
		self.chunk_residue = 0
		self.first_chunk = True if self.BLEN < self.CHUNKSIZE else False

		self.avgbw, self.stdbw = self._GetBWStdDev()

		self.BW = int(self.bwArray[0][1])
		if (self.jointime < self.bwArray[0][0]):
			self.bwArray = self._InsertJoinTimeAndInitBW()

		self.decision_cycle = 50 
		self.oldBR = self.BR
		self.buffering = False
		self.sessionFullyDownloaded = False
		self.numSwitches = 0
		self.dominantBitrate = dict()
		self.timeSinceLastDecision = 0
		self.interval = config.SIMULATION_STEP
		self.upr_h = -1000
		self.upr_b = 0.4
		self.configsUsed = []
		self.firstRebuf = False
		self.lastABR = ''
		self.chunk_residue = 0.0

		self.allPerf = collections.OrderedDict()
		self.completionTimeStamps = []
		self.maxQoE = -sys.maxint

		self.switchFlag = False

		self.lastBlen_decisioncycle = list()
		## hyb
		self.min_playable_buff = 0.45 if config.DASH_BUFFER_ADJUST else 0.0

		self.minCellSize = 900
		self.max_error = 0
		###### Change detection variables start ######
		self.q = collections.deque(maxlen = 2)
		self.last_chd_interval = 0
		self.clock_inc = 0
		self.last_clock_val = 0
		self.ch_detected = False
		self.ch_index = 0
		self.playerVisibleBW = []
		self.chunk_when_last_chd_ran = -1
		self.numChunks = -1
		self.gradual_transition = 0
		self.additive_inc = 0.0
		###### Change detection variables end.. ######
		###### MPC variables start ###################
		self.discount = 0
		self.bandwidthEsts = list()
		self.pastErrors = list()
		self.change_magnitude = 0
		self.windowSize = config.MPC_WINDOWSIZE
		###### MPC variables end.. ###################
		###### BOLA variables start ###################
		self.buffer_target_s = 30
		###### BOLA variables end.. ###################

		self.initialBSM = 0.25
		self.p1_min = self.initialBSM

		self.upr = -10000000
		self.A = self.initialBSM
		self.bwMap = dict()
		self.sizeDict = dict()
		self.usedBWArray = []
		self.nSamples = collections.deque(5 * [0], 5)
		self.hbCount = 0

		#self.BSM = A
		self.upr_h = -10000000
		self.upr_b = 0.4
		self.chunk_sched_time_delay = 0.0
		#self.blen_decrease = False
		#self.CHUNKS_DOWNLOADED_old = -1

		self.playStalled_thisInterval = 0
		self.chd_thisInterval = 0
		self.blenAdded_thisInterval = 0

		self.gp = getBolaGP()
		self.bola_vp = getBolaVP(self.gp)


	def _ParseTrace(self, config, trace_file):
		ts, bw = [], []
		init_br = 0
		bitrates = range(0, config.NUM_BITRATES)
		try:
			ls = open(trace_file).readlines()
			for l in ls:
				if l in ['\n', '\r\n']:
					continue
				try:
					ts.append(float(l.split("\t")[0]))
					bw.append(float(l.split("\t")[1]))
				except ValueError:
					ts.append(float(l.split(" ")[0]))
					bw.append(float(l.split(" ")[1]))

		except IOError:
			print >> sys.stderr, ("Incorrect filepath: " + trace_file + " no such file found...")
			sys.exit()

		try:
			init_br = int(float(ls[-1].rstrip("\n").split(" ")[9]))
		except (IndexError, ValueError):
			init_br = bitrates[0]

		try:
			totalTraceTime = ts[-1] # read this value as the last time stamp in the file
		except IndexError:
			print >> sys.stderr, "Problem with file format: " + trace_file
			sys.exit()
		return bitrates, totalTraceTime, totalTraceTime, 1, 1, init_br, zip(ts,bw)


	def _GetBWStdDev(self):
		bwMat = np.array(self.bwArray)
		return np.around(np.average(bwMat[:,1]),2), np.around(np.std(bwMat[:,1]),2)

	def _InsertJoinTimeAndInitBW():
		t = []
		t.append(self.jointime)
		b = []
		b.append(self.BW)
		row = zip(t,b)
		self.bwArray = row + self.bwArray
		return

	# function prints a print header
	def PrintHeader(self):
		print "Session joined..."
		print "TIME" + "\t" \
			+ "BW" + "\t" \
			+ "BLEN" + "\t" \
			+ "OBR" + "\t" \
			+ "BR" + "\t" \
			+ "CHKS" + "\t" \
			+ "RSDU" + "\t" \
			+ "BUFF" + "\t" \
			+ "PLAY"

	# function prints current session status
	def PrintStats(self):
		if self.CLOCK == 0:
			self.PrintHeader()
		print str(round(self.CLOCK/1000.0,2)) + "\t" \
			+ str(round(self.BW,2)) + "\t" \
			+ str(round(self.BLEN,2)) + "\t" \
			+ str(self.oldBR) + "\t" \
			+ str(self.BR) + "\t" \
			+ str(self.CHUNKS_DOWNLOADED) + "\t" \
			+ str(round(self.chunk_residue,2)) + "\t" \
			+ str(round(self.BUFFTIME,2)) + "\t" \
			+ str(round(self.PLAYTIME,2))

	def PrintStatsChunkBoundary(self):
		print str(round(self.CLOCK/1000.0,2)) + "\t" \
			+ str(round(self.BW,2)) + "\t" \
			+ str(round(self.BLEN,2)) + "\t" \
			+ str(self.oldBR) + "\t" \
			+ str(self.BR) + "\t" \
			+ str(self.CHUNKS_DOWNLOADED) + "\t" \
			+ str(round(self.chunk_residue,2)) + "\t" \
			+ str(round(self.BUFFTIME,2)) + "\t" \
			+ str(round(self.PLAYTIME,2)) + "\t" \
			+ str(round(self.max_error,4)) + "\t" \
			+ str(self.discount) + "\t" \
			+ str(self.chunk_when_last_chd_ran)
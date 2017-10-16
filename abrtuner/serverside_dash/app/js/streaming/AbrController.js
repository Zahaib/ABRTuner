/*
 * The copyright in this software is being made available under the BSD License, included below. This software may be subject to other third party and contributor rights, including patent rights, and no such rights are granted under this license.
 * 
 * Copyright (c) 2013, Digital Primates
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 * •  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * •  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * •  Neither the name of the Digital Primates nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
MediaPlayer.dependencies.AbrController = function () {
	"use strict";

	var autoSwitchBitrate = true,
	sessionStartTime = 0,
	qualityDict = {},
	confidenceDict = {},
	//Xiaoqi
	oldQuality = 0,
	chunkCount = 0,
	lastRequested = -1, // Xiaoqi_new
	lastQuality = -1,
	//Xiaoqi
	// Xiaoqi_new
	bufferLevelLog = [0],
	// MPC racecar video
	// bitrateArray = [350,600,1000,2000,3000],
	//bitrateArray = [825,1300,1800,2500,3200,3700],
	//bitrateArray = [825,1300,1800,2500,3200],
	// Pensieve Video 
	bitrateArray = [300,750,1200,1850,2850,4300],
	reservoir = 5,
	BUFFER_SAFETY_MARGIN = 1.0,
	BITRATE_WEIGHT = 1,
	BUFFERING_WEIGHT = -1000000,
	cushion = 60,
	p_rb = 1,
	// p_rb = 0.85,
	bufferLevelAdjusted = 0,
	bufferLevelAdjusted_mpc = 0,
	// Xiaoqi_new
	// Xiaoqi: Visual
	abrAlgo = 0,
	fixedQualityArray = [],
	// Xiaoqi: Visual

	getInternalQuality = function (type) {
		var quality;

		if (!qualityDict.hasOwnProperty(type)) {
			qualityDict[type] = 0;
		}

		quality = qualityDict[type];

		return quality;
	},

	setInternalQuality = function (type, value) {
		qualityDict[type] = value;
	},

	getInternalConfidence = function (type) {
		var confidence;

		if (!confidenceDict.hasOwnProperty(type)) {
			confidenceDict[type] = 0;
		}

		confidence = confidenceDict[type];

		return confidence;
	},

	setInternalConfidence = function (type, value) {
		confidenceDict[type] = value;
	};

	return {
		debug: undefined,
		abrRulesCollection: undefined,
		manifestExt: undefined,
		metricsModel: undefined,
		// Xiaoqi
		metricsExt: undefined,
		// Xiaoqi_new
		fastMPC: undefined,
		bwPredictor: undefined,
		vbr: undefined,
		// Xiaoqi_new
		// Xiaoqi_cr
		festive: undefined,
		// Xiaoqi_cr
		// Xiaoqi

		getSessionStartTime: function (){
			return sessionStartTime;
		},

		getBitrateBB: function (bLevel) {
			var self = this,
			tmpBitrate = 0,
			tmpQuality = 0;
			
			if (bLevel <= reservoir) {
				tmpBitrate = bitrateArray[0];
			} else if (bLevel > reservoir + cushion) {
				tmpBitrate = bitrateArray[bitrateArray.length-1];
			} else {
				tmpBitrate = bitrateArray[0] + (bitrateArray[bitrateArray.length-1] - bitrateArray[0])*(bLevel - reservoir)/cushion;
			}
			
			// findout matching quality level
			for (var i = bitrateArray.length-1; i>=0; i--) {
				if (tmpBitrate >= bitrateArray[i]) {
					tmpQuality = i;
					break;
				}
				tmpQuality = i;
			}
			self.debug.log("----------BB: tmpBitrate="+tmpBitrate+", tmpQuality="+tmpQuality + ", bufferLevel="+bLevel);
			return tmpQuality;
			// return 5;
		},

		getBitrateHYB: function (bLevel, bandwidth, index) {
				var self = this,
					tmpBitrate = 0,
					tmpQuality = 0;
				var utility = -10000000;
				var estBufferingTime;

				for (var q =0; q<bitrateArray.length; q++){
					estBufferingTime = -1*Math.min((bLevel)*BUFFER_SAFETY_MARGIN - (self.vbr.getChunkSize(index,q)*8)/(1000*bandwidth),0);
					if (utility < estBufferingTime * BUFFERING_WEIGHT + bitrateArray[q] * BITRATE_WEIGHT){
						tmpBitrate = bitrateArray[q];
						tmpQuality = q;
						utility = estBufferingTime * BUFFERING_WEIGHT + bitrateArray[q] * BITRATE_WEIGHT;
					}
					self.debug.log("----------YUN HYB: bufferLevel="+bLevel+", bandwidth="+bandwidth + ", q="+q+", Chunk ID = "+index+","+self.vbr.getChunkSize(index,q) + ", estBufferTime = "+estBufferingTime);
				}
				//if (index==0){
				//		tmpQuality  = 0;
				//	}

				self.debug.log("----------YUN HYB: tmpBitrate="+tmpBitrate+", tmpQuality="+tmpQuality + ", bufferLevel="+bLevel+", Chunk ID = "+index);
				return tmpQuality;
				// return 3;
		},

		getBitrateRB: function (bandwidth) {
			var self = this,
			tmpBitrate = 0,
			tmpQuality = 0;
			
			tmpBitrate = bandwidth*p_rb;
			
			// findout matching quality level
			for (var i = bitrateArray.length-1; i>=0; i--) {
				if (tmpBitrate >= bitrateArray[i]) {
					tmpQuality = i;
					break;
				}
				tmpQuality = i;
			}
			self.debug.log("----------RB: tmpBitrate="+tmpBitrate+", tmpQuality="+tmpQuality + ", bandwidth="+bandwidth);
			return tmpQuality;	
			// return 0;
		},

		getAutoSwitchBitrate: function () {
			return autoSwitchBitrate;
		},

		setAutoSwitchBitrate: function (value) {
			autoSwitchBitrate = value;
		},

		// Xiaoqi: Visual
		setAbrAlgorithm: function(algo) {
			abrAlgo = algo;
			console.log("-----VISUAL: set abrAlgo="+abrAlgo);
		},

		setFixedBitrateArray: function(fixedBitrateArray) {
			fixedQualityArray = fixedBitrateArray;
			console.log("-----VISUAL: set fixedBitrateArray");
		},
		// Xiaoqi: Visual

		getMetricsFor: function (data) {
			var deferred = Q.defer(),
			self = this;

			self.manifestExt.getIsVideo(data).then(
				function (isVideo) {
					if (isVideo) {
						deferred.resolve(self.metricsModel.getMetricsFor("video"));
					} else {
						self.manifestExt.getIsAudio(data).then(
							function (isAudio) {
								if (isAudio) {
									deferred.resolve(self.metricsModel.getMetricsFor("audio"));
								} else {
									deferred.resolve(self.metricsModel.getMetricsFor("stream"));
								}
							}
						);
					}
				}
			);

			return deferred.promise;
		},

		next_chunk_size: function (index, quality) {
		    // This is the Envivio video we are using.
		    // Racecar video!
		    // index is the index of the *next* chunk
		    // var size_video1 = [1680951,1637558,1371111,1684293,1400042,1792609,1213669,1191552,1888982,1381292,1593129,1384566,1918298,1605664,1356382,1278860,1580165,1315506,1642869,928190,1416000,865548,1284104,1692271,1504744,1484004,1405086,891371,1401736,1743545,1084561,1099310,1789869,1675658,1636106,1492615,1200522,1787763,1690817,1459339,1250444,1691788,1403315,1732710,1270067,1514363,1615320,1507682,1260622,1784654,1352160,1115913,1637646,1546975,1637443,1475444,1616179,1113960,466635,1727956,1316739,1373312,458410,320487,573826],
		    // size_video2 = [1184008,1123706,854424,1150093,902304,1237428,763515,840707,1279590,930828,996858,950867,1285933,1049248,984261,876058,1054391,875132,996451,660126,1032091,626844,949274,1197901,1001670,994288,925341,623084,977347,1184694,766276,834528,1285071,1017030,1080835,1078945,788728,1165402,1123991,937434,804808,1178153,922947,1175468,903392,970351,1094905,931644,854957,1179875,978233,794797,1073857,942081,1074761,1033448,1181202,660582,297985,1188866,910001,974311,314327,221329,445973],
		    // size_video3 = [604139,577615,418531,555427,469238,614632,393715,428426,594788,527047,460827,500774,621760,556545,476734,417508,552639,462442,552256,303234,522859,337637,471941,598737,560588,487684,479873,284277,564825,546935,394056,442514,610493,523364,574457,499175,412705,586327,560284,476697,408166,570011,502061,569274,444948,507586,525450,541979,391886,539537,506089,408110,515570,462132,574826,523754,572621,344553,157240,610010,460871,480012,169331,126490,236234],
		    // size_video4 = [361158,370284,246858,357922,264156,371586,241808,270621,327839,334864,313171,253682,348331,319047,311275,282933,308899,289234,307870,207573,354546,208087,305510,364291,331480,298846,298034,195290,327636,354076,261457,272419,344053,307537,344697,301834,261403,332467,324205,276260,260969,357539,301214,320538,292593,290952,325914,285965,266844,327707,308757,271734,313780,284833,295589,331270,307411,224531,94934,385537,306688,310705,95847,78651,162260],
		    // size_video5 = [207189,219272,134208,204651,164461,230942,136746,150366,193697,193362,189146,153391,195591,177177,190923,155030,185660,164741,179442,131632,198676,115285,148044,181978,200708,177663,176815,109489,203211,196841,161524,151656,182521,172804,211407,171710,170866,178753,175461,184494,154382,206330,175870,178679,173567,172998,189473,172737,163181,181882,186151,164281,172026,173011,162488,201781,176856,137099,57015,234214,172494,184405,61936,43268,81580];

	    	// 6 bitrate weird video
			var size_video1 = [2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658],
			size_video2 = [1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412],
			size_video3 = [1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850],
			size_video4 = [668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450],
			size_video5 = [450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954],
			size_video6 = [181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270];


		    // upper number is 96 if 2 second chunks for weird video
		    // if 4 second chunks, make that number 48
		    // 64 for old video (racecar)
		    if (index < 0 || index > 48) {
		        return 0;
		    }
		    var chunkSize = [size_video1[index], size_video2[index], size_video3[index], size_video4[index], size_video5[index], size_video6[index]];
		    // for Envivio race car uncomment the line below and comment the line above
		    // var chunkSize = [size_video1[index], size_video2[index], size_video3[index], size_video4[index], size_video5[index]];
		    return chunkSize;
		},

		// returns size of last chunk using HTTPRequest object (not hardcoded :))
		last_chunk_size: function (lastreq) {
		    var tot = 0;
		    // for ( var tt = 0; tt < lastreq.trace.length; tt++ ) {
	        tot = lastreq.trace[lastreq.trace.length - 1]['b'][0];
		    // }
		    return tot;
		},

        // returns intermediate bandwidth samples computed from chunk download trace
		last_chunk_bw: function (lastreq) {
			console.log("ZA getting intermediate BW values");
            var chunkBWArray = [];
            var bytes_downloaded = 0;
            var duration = 0;
            var bw = 0
            for ( var tt = 1; tt < lastreq.trace.length; tt++ ) {
              	bytes_downloaded = lastreq.trace[tt]['b'][0] - lastreq.trace[tt - 1]['b'][0];
               	duration = lastreq.trace[tt]['d'];
               	if ((duration > 0) && (bytes_downloaded > 0)){
               		bw = (bytes_downloaded * 8) / duration;
               		chunkBWArray.push(bw);
	               	console.log("last_chunk_bw " + tt + " bytes " + bytes_downloaded + " dur " + duration + " bw " + bw);
               	}
            }
            return chunkBWArray;
		},

		getPlaybackQuality: function (type, data, /*Xiaoqi*/lastRequestedSegmentIndex, lastBufferedSegmentIndex, bufferLevel, representation/*Xiaoqi*/, currentVideoTime, rebuffer) {
			var self = this,
			deferred = Q.defer(),
			newQuality = MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE,
			newConfidence = MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE,
			i,
			len,
			funcs = [],
			req,
			values,
			quality,
			confidence,
			//Xiaoqi
			lastHTTPRequest,
			downloadTime,
			bitrate,
			bandwidthEst,
			//Xiaoqi_cr
			bandwidthEstError,
			//Xiaoqi_cr
			nextBitrate;
			//Xiaoqi
			quality = getInternalQuality(type);
			confidence = getInternalConfidence(type);
			// Xiaoqi_cr
			quality = oldQuality;
			self.debug.log("RRRRRRRRRRRRRRRRRRRRRR Total Rebuffer Time " + rebuffer);
			if (lastRequestedSegmentIndex === lastBufferedSegmentIndex && lastRequested === lastRequestedSegmentIndex) {
				// Xiaoqi_cr
				if (autoSwitchBitrate) {
				//self.debug.log("Check ABR rules.");
					self.getMetricsFor(data).then(
					function (metrics) {
						self.abrRulesCollection.getRules().then(
						function (rules) {
							for (i = 0, len = rules.length; i < len; i += 1) {
								funcs.push(rules[i].checkIndex(quality, metrics, data));
							}
							Q.all(funcs).then(
							function (results) {
								//self.debug.log(results);
								values = {};
								values[MediaPlayer.rules.SwitchRequest.prototype.STRONG] = MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE;
								values[MediaPlayer.rules.SwitchRequest.prototype.WEAK] = MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE;
								values[MediaPlayer.rules.SwitchRequest.prototype.DEFAULT] = MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE;

								for (i = 0, len = results.length; i < len; i += 1) {
									req = results[i];
									if (req.quality !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE) {
										values[req.priority] = Math.min(values[req.priority], req.quality);
									}
								}

								if (values[MediaPlayer.rules.SwitchRequest.prototype.WEAK] !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE) {
									newConfidence = MediaPlayer.rules.SwitchRequest.prototype.WEAK;
									newQuality = values[MediaPlayer.rules.SwitchRequest.prototype.WEAK];
								}

								if (values[MediaPlayer.rules.SwitchRequest.prototype.DEFAULT] !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE) {
									newConfidence = MediaPlayer.rules.SwitchRequest.prototype.DEFAULT;
									newQuality = values[MediaPlayer.rules.SwitchRequest.prototype.DEFAULT];
								}

								if (values[MediaPlayer.rules.SwitchRequest.prototype.STRONG] !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE) {
									newConfidence = MediaPlayer.rules.SwitchRequest.prototype.STRONG;
									newQuality = values[MediaPlayer.rules.SwitchRequest.prototype.STRONG];
								}

								if (newQuality !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE && newQuality !== undefined) {
									quality = newQuality;
								}

								if (newConfidence !== MediaPlayer.rules.SwitchRequest.prototype.NO_CHANGE && newConfidence !== undefined) {
									confidence = newConfidence;
								}
								// Xiaoqi_cr
								self.debug.log("-----Original: quality: "+quality+", confidence: "+confidence);
								// Xiaoqi_cr
								self.manifestExt.getRepresentationCount(data).then(
								function (max) {
									// be sure the quality valid!
									if (quality < 0) {
										quality = 0;
									}
									// zero based
									if (quality >= max) {
										quality = max - 1;
									}

									if (confidence != MediaPlayer.rules.SwitchRequest.prototype.STRONG && confidence != MediaPlayer.rules.SwitchRequest.prototype.WEAK) {
										confidence = MediaPlayer.rules.SwitchRequest.prototype.DEFAULT;
									}

									// Xiaoqi_cr
									var quality_original = quality;
									// Xiaoqi_cr
									// Xiaoqi
									//currentIndex = streamProcessor.indexHandler.getCurrentIndex();
									quality = oldQuality;
									nextBitrate = 0;

									var tmpRequest = self.metricsExt.getCurrentHttpRequest(metrics);
									if (tmpRequest){
										for (i = 0; i < tmpRequest.trace.length; i++){
											self.debug.log("MMMMMMMMMMMMMMMMMM " + tmpRequest.trace[i].s + " " + tmpRequest.trace[i].d + " " + tmpRequest.trace[i].b);
										}
									}

									if (lastRequestedSegmentIndex === lastBufferedSegmentIndex && lastRequested === lastRequestedSegmentIndex) {
										// Bandwidth estimation
										// Xiaoqi_new
										//bandwidthEst = self.bwPredictor.predictBandwidth(lastRequested, metrics, 0);
										//self.debug.log("----------abrController BW Predict: "+bandwidthEst);
										// Xiaoqi_new
										if (lastRequested >=0  && metrics){
											lastHTTPRequest = self.metricsExt.getCurrentHttpRequest(metrics);

											if (lastHTTPRequest) {
												if (lastRequestedSegmentIndex===0) sessionStartTime = lastHTTPRequest.trequest.getTime();
												var start_temp = lastHTTPRequest.trequest.getTime() - sessionStartTime,
												end_temp = lastHTTPRequest.tfinish.getTime() - sessionStartTime,
												ttfb_temp = lastHTTPRequest.tresponse.getTime() - sessionStartTime;
												//self.debug.log("Yun Final Log : chunkID="+lastHTTPRequest.index+", requestStar="+lastHTTPRequest.requestStartDate+", timeToFirstByte="+lastHTTPRequest.firstByteDate+", requestEnd="+lastHTTPRequest.requestEndDate+", Bitrate="+lastHTTPRequest.quality+", availabilityStartTime="+lastHTTPRequest.availabilityStartTime+", startTime="+lastHTTPRequest.startTime);
												self.debug.log("Yun Final Log chunk information: url="+lastHTTPRequest.url+", trequest="+start_temp+", tresponse="+ttfb_temp+", tfinish="+end_temp+", currentPlaylocation="+currentVideoTime+", bufferLength="+bufferLevel);
			                                    //if (lastRequestedSegmentIndex === 48) {
			                                    //    var xmlHttp = new XMLHttpRequest();
			                                    //    xmlHttp.open( "GET", "http://localhost/finishme.txt", false);
			                                    //    xmlHttp.send( null );
			                                    //}

												//for (var bw=0; bw<lastHTTPRequest.trace.length; bw++){
												//	if (lastHTTPRequest.trace[bw].b!==0) self.debug.log("Yun Final Log chunk information bandwidth: url="+lastHTTPRequest.url+", start="+lastHTTPRequest.trace[bw].s+", end="+lastHTTPRequest.trace[bw].d+", byte="+lastHTTPRequest.trace[bw].b);
												//}

												// Xiaoqi_new
												// self.debug.log("----------abrController BW Predict: lastRequested="+lastRequested+", lastQuality=" + lastQuality);
												// Bandwidth Prediction
												bandwidthEst = self.bwPredictor.predictBandwidth(lastRequested, lastQuality, lastHTTPRequest);
												// Xiaoqi_cr
												// bandwidthEstError = self.bwPredictor.getPredictionError(lastRequested);
												// self.debug.log("----------abrController BW Predict: " + bandwidthEst + ", Error: " + bandwidthEstError);
												// // multistep prediction error					  
												// bandwidthEstError = self.bwPredictor.getCombinedPredictionError(lastRequested);
												// self.debug.log("----------abrController BW Predict Combined: " + bandwidthEst + ", Error: " + bandwidthEstError);
												// Xiaoqi_cr
												// self.debug.log("-----FastMPC:" + self.fastMPC.getBitrate(0, 0, 350));
												// self.debug.log("-----FastMPC:" + self.fastMPC.getBitrate(4, 20, 3000));
												// Adjust buffer level to avoid latency, etc
												var baseBuffer = 4;
												bufferLevelAdjusted_mpc = bufferLevel-0.15-0.4-baseBuffer;
                                                                                                bufferLevelAdjusted = bufferLevel-0.15-0.4-baseBuffer;
                                                                                                bufferLevelAdjusted = bufferLevelAdjusted < 0 ? 0 : bufferLevelAdjusted;
                                                                                                self.debug.log("-----abrController: baseBuffer="+baseBuffer);
												// bufferLevelAdjusted = bufferLevel-0.15-0.4; // mpc_nobuffer
												// bufferLevelAdjusted = bufferLevel-0.15-0.4-2; // mpc
												// bufferLevelAdjusted = bufferLevel-0.15-0.4-4; // mpc
												// // Fast MPC
												// quality = self.fastMPC.getBitrate(lastQuality, bufferLevelAdjusted, bandwidthEst);
												// self.debug.log("-----FastMPC:" + quality);
												// // Robust Fast MPC
												// quality = self.fastMPC.getBitrate(lastQuality, bufferLevelAdjusted, bandwidthEst/(1+bandwidthEstError));
												// self.debug.log("-----Robust FastMPC:" + quality);
												// // BB
												// quality = self.getBitrateBB(bufferLevelAdjusted);
												// self.debug.log("-----Buffer-Based:" + quality);
												// // RB
												// quality = self.getBitrateHYB(bufferLevelAdjusted, bandwidthEst, lastRequestedSegmentIndex + 1);
												 //self.debug.log("-----Rate-Based:" + quality);
												// // Original DASH.js
												// quality = quality_original;
												// self.debug.log("-----ORIGINAL DASH.js:" + quality);
												// FESTIVE
												// quality = self.festive.getBitrate(lastQuality, bufferLevelAdjusted, bandwidthEst, lastRequested, bitrateArray);
												// self.debug.log("-----FESTIVE:" + quality);
												// Xiaoqi_new
												// Log bufferlevel
												bufferLevelLog[lastRequested+1] = bufferLevelAdjusted;
												self.debug.log("-----bufferLevelLog=" + bufferLevelLog[lastRequested+1]);

												// Xiaoqi: Visual
												// self.debug.log("NNNNNNNNNNNNNNNNNNNNNNNNNNNN AbrAlgo is: " + abrAlgo)
												// abrAlgo = 7
												switch (abrAlgo) {
													case -1: // same as 0
														bandwidthEstError = self.bwPredictor.getCombinedPredictionError(lastRequested);
														quality = self.fastMPC.getBitrate(lastQuality, bufferLevelAdjusted, bandwidthEst/(1+bandwidthEstError));
														break;
													case 0: 
														bandwidthEstError = self.bwPredictor.getCombinedPredictionError(lastRequested);
														quality = self.fastMPC.getBitrate(lastQuality, bufferLevelAdjusted_mpc, bandwidthEst/(1+bandwidthEstError));
														break;
													case 1:
														quality = self.getBitrateBB(bufferLevel);
														break;
													case 2: 
														quality = self.getBitrateRB(bandwidthEst);
														break;
													case 3: 
														quality = quality_original;
														break;
													case 4: 
														quality = self.festive.getBitrate(lastQuality, bufferLevelAdjusted, bandwidthEst, lastRequested, bitrateArray);
														break;
													case 5:
														quality = fixedQualityArray[lastRequested+1];
														if (quality === undefined) {
															quality = 0;
															console.log("fixedQualityArray, chunk after "+ lastRequested + " is undefined");
														}
														break;
													case 6: // Pensieve
														self.debug.log("Using Pensieve...PENSIEVE");
										                var quality = 0;
										                var xhr = new XMLHttpRequest();
										                xhr.open("POST", "http://localhost:8333", false);
										                self.debug.log("Using Pensieve...PENSIEVE, got xhr: " + xhr);

										                xhr.onreadystatechange = function() {
										                    if ( xhr.readyState == 4 && xhr.status == 200 ) {
										                        console.log("GOT RESPONSE:" + xhr.responseText + "---");
										                        if ( xhr.responseText != "REFRESH" ) {
										                            quality = parseInt(xhr.responseText, 10);
										                        } 
										                    }
										                }
										                var data = {'nextChunkSize': self.next_chunk_size(lastRequested+1),
										                			'lastquality': lastQuality,
									                				'buffer': bufferLevel,
									                				'bufferAdjusted': bufferLevelAdjusted_mpc,
									                				'bandwidthEst': bandwidthEst,
									                				'lastRequest': lastRequested,
									                				'RebufferTime': rebuffer,
									                				'lastChunkFinishTime': lastHTTPRequest.tfinish.getTime(),
									                				'lastChunkStartTime': lastHTTPRequest.tresponse.getTime(),
									                				'lastChunkSize': self.last_chunk_size(lastHTTPRequest)};
						                				var dataStringified = JSON.stringify(data)
										                self.debug.log("Using Pensieve...PENSIEVE, got dataStringified: " + dataStringified);
										                xhr.send(dataStringified);
										                self.debug.log("QUALITY RETURNED IS: " + quality);														 
														break;
													case 7: // RobustMPC, this is just a copy of Pensieve
														self.debug.log("Using RobustMPC...RobustMPC");
										                var quality = 0;
										                var xhr = new XMLHttpRequest();
										                xhr.open("POST", "http://localhost:8334", false);
										                self.debug.log("Using RobustMPC...RobustMPC, got xhr: " + xhr);

										                xhr.onreadystatechange = function() {
										                    if ( xhr.readyState == 4 && xhr.status == 200 ) {
										                        console.log("GOT RESPONSE:" + xhr.responseText + "---");
										                        if ( xhr.responseText != "REFRESH" ) {
										                            quality = parseInt(xhr.responseText, 10);
										                        } 
										                    }
										                }
										                var data = {'nextChunkSize': self.next_chunk_size(lastRequested+1),
										                			'lastquality': lastQuality,
									                				'buffer': bufferLevelAdjusted,
									                				'bufferAdjusted': bufferLevelAdjusted_mpc,
									                				'bandwidthEst': bandwidthEst,
									                				'lastRequest': lastRequested,
									                				'RebufferTime': rebuffer,
									                				'lastChunkFinishTime': lastHTTPRequest.tfinish.getTime(),
									                				'lastChunkStartTime': lastHTTPRequest.tresponse.getTime(),
									                				'lastChunkSize': self.last_chunk_size(lastHTTPRequest)};
						                				var dataStringified = JSON.stringify(data)
										                self.debug.log("Using RobustMPC...RobustMPC, got dataStringified: " + dataStringified);
										                xhr.send(dataStringified);
										                self.debug.log("QUALITY RETURNED IS: " + quality);														 
														break;														
													case 8: // HYB + Tuner 
                                                    	self.debug.log("Using HYB+Tuner OnlineCD...Tuner Online CD");
                                                        var quality = 0;
														var lastChunkBWArray = self.last_chunk_bw(lastHTTPRequest);									                				

                                                        var xhr = new XMLHttpRequest();
                                                        xhr.open("POST", "http://localhost:8335", false);
                                                        self.debug.log("Using HYB+Tuner Online CD...Tuner Online CD, got xhr: " + xhr);

                                                        xhr.onreadystatechange = function() {
                                                            if ( xhr.readyState == 4 && xhr.status == 200 ) {
                                                                console.log("GOT RESPONSE:" + xhr.responseText + "---");
                                                                if ( xhr.responseText != "REFRESH" ) {
                                                                    quality = parseInt(xhr.responseText, 10);
                                                                }
                                                            }
                                                        }

										                var data = {'nextChunkSize': self.next_chunk_size(lastRequested+1),
										                			'lastquality': lastQuality,
									                				'buffer': bufferLevelAdjusted,
									                				'bufferAdjusted': bufferLevelAdjusted_mpc,
									                				'bandwidthEst': bandwidthEst,
									                				'lastRequest': lastRequested,
									                				'RebufferTime': rebuffer,
									                				'lastChunkBWArray': self.last_chunk_bw(lastHTTPRequest),
																	'lastChunkFinishTime': lastHTTPRequest.tfinish.getTime(),
									                				'lastChunkStartTime': lastHTTPRequest.tresponse.getTime(),
									                				'lastChunkSize': self.last_chunk_size(lastHTTPRequest)};
                                                        var dataStringified = JSON.stringify(data);
                                                        self.debug.log("Using HYB+Tuner Online CD..., got dataStringified: " + dataStringified);
                                                        xhr.send(dataStringified);
                                                        self.debug.log("QUALITY RETURNED IS: " + quality);
                                                        break;
													case 9: // MPC + Tuner  -- this is just a copy of the HYB + Tuner code
                                                    	self.debug.log("Using MPC+Tuner OnlineCD...Tuner Online CD");
                                                        var quality = 0;
														var lastChunkBWArray = self.last_chunk_bw(lastHTTPRequest);									                				

                                                        var xhr = new XMLHttpRequest();
                                                        xhr.open("POST", "http://localhost:8336", false);
                                                        self.debug.log("Using MPC+Tuner Online CD...Tuner Online CD, got xhr: " + xhr);

                                                        xhr.onreadystatechange = function() {
                                                            if ( xhr.readyState == 4 && xhr.status == 200 ) {
                                                                console.log("GOT RESPONSE:" + xhr.responseText + "---");
                                                                if ( xhr.responseText != "REFRESH" ) {
                                                                    quality = parseInt(xhr.responseText, 10);
                                                                }
                                                            }
                                                        }

										                var data = {'nextChunkSize': self.next_chunk_size(lastRequested+1),
										                			'lastquality': lastQuality,
									                				'buffer': bufferLevelAdjusted,
									                				'bufferAdjusted': bufferLevelAdjusted_mpc,
									                				'bandwidthEst': bandwidthEst,
									                				'lastRequest': lastRequested,
									                				'RebufferTime': rebuffer,
									                				'lastChunkBWArray': self.last_chunk_bw(lastHTTPRequest),
																	'lastChunkFinishTime': lastHTTPRequest.tfinish.getTime(),
									                				'lastChunkStartTime': lastHTTPRequest.tresponse.getTime(),
									                				'lastChunkSize': self.last_chunk_size(lastHTTPRequest)};
                                                        var dataStringified = JSON.stringify(data);
                                                        self.debug.log("Using MPC+Tuner Online CD..., got dataStringified: " + dataStringified);
                                                        xhr.send(dataStringified);
                                                        self.debug.log("QUALITY RETURNED IS: " + quality);
                                                        break;
													case 10:
														self.debug.log("Using HYB...HHHHHHYYYYYBBBBBB");
														quality = self.getBitrateHYB(bufferLevelAdjusted, bandwidthEst, lastRequestedSegmentIndex + 1);
														break;
													default:
														self.debug.log("Using Default...DDDEEEFFFAAAUUULLLTTT"); 
														quality = 0; 
														break;
												}

											}
										}
										chunkCount = chunkCount + 1;
										lastRequested = lastRequestedSegmentIndex + 1;
										self.debug.log("Yun : abrController: Algo = "+abrAlgo+",ChunkID="+lastRequested+", quality="+quality);
                                                            if (lastRequestedSegmentIndex === 48) {
                                                                var xmlHttp = new XMLHttpRequest();
                                                                xmlHttp.open( "GET", "http://localhost/finishme.txt", false);
                                                                xmlHttp.send( null );
                                                            }
										lastQuality = quality;
										
									}
									oldQuality = quality; 
									self.debug.log("XIAOQI: abrController: lastRequested="+lastRequestedSegmentIndex+", lastBuffered="+lastBufferedSegmentIndex+ ", chunkCount="+chunkCount+", quality="+quality);
									//Xiaoqi

									setInternalQuality(type, quality);
									//self.debug.log("New quality of " + quality);

									setInternalConfidence(type, confidence);
									//self.debug.log("New confidence of " + confidence);

									deferred.resolve({quality: quality, confidence: confidence});
								}
								);
							}
							);
						}
						);
					}
					);
				} 
				else {
						self.debug.log("Unchanged quality of " + quality);
						deferred.resolve({quality: quality, confidence: confidence});
				}
				// Xiaoqi_cr
			} else {
				deferred.resolve({quality: quality, confidence: 0.5});
			}
			// Xiaoqi_cr

			return deferred.promise;
		},

		setPlaybackQuality: function (type, newPlaybackQuality) {
			var quality = getInternalQuality(type);

			if (newPlaybackQuality !== quality) {
				setInternalQuality(type, newPlaybackQuality);
			}
		},

		getQualityFor: function (type) {
			return getInternalQuality(type);
		}
	};
};

MediaPlayer.dependencies.AbrController.prototype = {
	constructor: MediaPlayer.dependencies.AbrController
};

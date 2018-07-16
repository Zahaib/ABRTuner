#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import base64
import urllib
import sys
import os
import json
os.environ['CUDA_VISIBLE_DEVICES']=''

import numpy as np
import time
import mpc_tuner_logic
import mpc_lookup_table_4300
import mpc_lookup_table_4300_fix
import mpc_lookup_table_4300_default
import mpc_lookup_table_4300_fix1012
import mpc_lookup_table_8600_fix1012
import mpc_lookup_table_8600_fix1012_min
import mpc_lookup_table_8600_fix1012_range
import mpc_lookup_table_8600_fix1012_range_pickmax

S_INFO = 6  # bit_rate, buffer_size, rebuffering_time, bandwidth_measurement, chunk_til_video_end
S_LEN = 8  # take how many frames in the past
A_DIM = 6
TOTAL_VIDEO_CHUNKS = 48
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
BITRATE_REWARD = [1, 2, 3, 12, 15, 20]
BITRATE_REWARD_MAP = {0: 0, 300: 1, 750: 2, 1200: 3, 1850: 12, 2850: 15, 4300: 20}
M_IN_K = 1000.0
BUFFER_NORM_FACTOR = 10.0
CHUNK_TIL_VIDEO_END_CAP = 48.0
DEFAULT_QUALITY = 0  # default video quality without agent
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
TRAIN_SEQ_LEN = 100  # take as a train batch
MODEL_SAVE_INTERVAL = 100
RANDOM_SEED = 42
RAND_RANGE = 1000
SUMMARY_DIR = './results'
LOG_FILE = './results/mpctuner_log'
# in format of time_stamp bit_rate buffer_size rebuffer_time video_chunk_size download_time reward
# NN_MODEL = None
NN_MODEL = '../rl_server/results/pretrain_linear_reward.ckpt'
#NN_MODEL = '../rl_server/results/nn_model_ep_176200.ckpt'
# video chunk sizes
size_video1 = [2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658]
size_video2 = [1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412]
size_video3 = [1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850]
size_video4 = [668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450]
size_video5 = [450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954]
size_video6 = [181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270]

size_envivo = {0:[181801, 155580, 139857, 155432, 163442, 126289, 153295, 173849, 150710, 139105, 141840, 156148, 160746, 179801, 140051, 138313, 143509, 150616, 165384, 140881, 157671, 157812, 163927, 137654, 146754, 153938, 181901, 111155, 153605, 149029, 157421, 157488, 143881, 163444, 179328, 159914, 131610, 124011, 144254, 149991, 147968, 161857, 145210, 172312, 167025, 160064, 137507, 118421, 112270], 1:[450283, 398865, 350812, 382355, 411561, 318564, 352642, 437162, 374758, 362795, 353220, 405134, 386351, 434409, 337059, 366214, 360831, 372963, 405596, 350713, 386472, 399894, 401853, 343800, 359903, 379700, 425781, 277716, 400396, 400508, 358218, 400322, 369834, 412837, 401088, 365161, 321064, 361565, 378327, 390680, 345516, 384505, 372093, 438281, 398987, 393804, 331053, 314107, 255954], 2:[668286, 611087, 571051, 617681, 652874, 520315, 561791, 709534, 584846, 560821, 607410, 594078, 624282, 687371, 526950, 587876, 617242, 581493, 639204, 586839, 601738, 616206, 656471, 536667, 587236, 590335, 696376, 487160, 622896, 641447, 570392, 620283, 584349, 670129, 690253, 598727, 487812, 575591, 605884, 587506, 566904, 641452, 599477, 634861, 630203, 638661, 538612, 550906, 391450], 3:[1034108, 957685, 877771, 933276, 996749, 801058, 905515, 1060487, 852833, 913888, 939819, 917428, 946851, 1036454, 821631, 923170, 966699, 885714, 987708, 923755, 891604, 955231, 968026, 874175, 897976, 905935, 1076599, 758197, 972798, 975811, 873429, 954453, 885062, 1035329, 1026056, 943942, 728962, 938587, 908665, 930577, 858450, 1025005, 886255, 973972, 958994, 982064, 830730, 846370, 598850], 4:[1728879, 1431809, 1300868, 1520281, 1472558, 1224260, 1388403, 1638769, 1348011, 1429765, 1354548, 1519951, 1422919, 1578343, 1231445, 1471065, 1491626, 1358801, 1537156, 1336050, 1415116, 1468126, 1505760, 1323990, 1383735, 1480464, 1547572, 1141971, 1498470, 1561263, 1341201, 1497683, 1358081, 1587293, 1492672, 1439896, 1139291, 1499009, 1427478, 1402287, 1339500, 1527299, 1343002, 1587250, 1464921, 1483527, 1231456, 1364537, 889412], 5:[2354772, 2123065, 2177073, 2160877, 2233056, 1941625, 2157535, 2290172, 2055469, 2169201, 2173522, 2102452, 2209463, 2275376, 2005399, 2152483, 2289689, 2059512, 2220726, 2156729, 2039773, 2176469, 2221506, 2044075, 2186790, 2105231, 2395588, 1972048, 2134614, 2164140, 2113193, 2147852, 2191074, 2286761, 2307787, 2143948, 1919781, 2147467, 2133870, 2146120, 2108491, 2184571, 2121928, 2219102, 2124950, 2246506, 1961140, 2155012, 1433658]}


def get_chunk_size(quality, index):
    if ( index < 0 or index > 48 ):
        return 0
    # note that the quality and video labels are inverted (i.e., quality 8 is highest and this pertains to video1)
    sizes = {5: size_video1[index], 4: size_video2[index], 3: size_video3[index], 2: size_video4[index], 1: size_video5[index], 0: size_video6[index]}
    #sizes = {4: size_video1[index], 3: size_video2[index], 2: size_video3[index], 1: size_video4[index], 0: size_video5[index]}
    return sizes[quality]

def make_request_handler(input_dict):

    class Request_Handler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.input_dict = input_dict
            self.log_file = input_dict['log_file']
            # self.playerVisibleBW = input_dict['playerVisibleBW']
            # self.sessionHistory = input_dict['sessionHistory']
            BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

        def parse_post_data(self, post_data):
            bufferLen = float(post_data['buffer'])
            lastChunkBW = (post_data['lastChunkSize'] * 8) / float(post_data['lastChunkFinishTime'] - post_data['lastChunkStartTime'])
            lastChunkBWArray = post_data['lastChunkBWArray']
            bandwidthEst = float(post_data['bandwidthEst'])
            lastChunkID = post_data['lastRequest']
            lastChunkBR = post_data['lastquality']
            sessionID = int(post_data['sessionID'])

            return lastChunkBR, \
                   bufferLen, \
                   lastChunkBW, \
                   lastChunkBWArray, \
                   bandwidthEst, \
                   lastChunkID, \
                   sessionID

        def reset_state(self):
                self.input_dict['playerVisibleBW'] = []
                self.input_dict['sessionHistory'] = dict()
                self.input_dict['chunkBWSamples'] = []
                self.input_dict['bandwidthEsts'] = []
                self.input_dict['pastErrors'] = []
                self.input_dict['chunksDownloaded'] = 0
                self.input_dict['chunk_when_last_chd_ran'] = -1
                self.input_dict['discount'] = 0.0

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            # print post_data

            lastChunkBR, \
            bufferLen, \
            lastChunkBW, \
            lastChunkBWArray, \
            bandwidthEst, \
            lastChunkID, \
            sessionID = self.parse_post_data(post_data)

            if sessionID not in self.input_dict['sessionIDs']:
                print "...SESSION START..."
                self.input_dict['sessionIDs'].add(sessionID)
                self.reset_state()

            # omit the first and last sample, it is usually bad
            self.input_dict['playerVisibleBW'] += lastChunkBWArray[1:][:-1]
            self.input_dict['sessionHistory'][lastChunkID] = [lastChunkBW]
            self.input_dict['chunkBWSamples'].append(lastChunkBW)
            self.input_dict['chunksDownloaded'] = lastChunkID

            # print lastChunkID, "len", len(self.input_dict['chunkBWSamples'])

            chpd_interval = 5
            chd_detected, chd_index = mpc_tuner_logic.onlineCD(self.input_dict['chunk_when_last_chd_ran'], \
                                                           chpd_interval, \
                                                           self.input_dict['playerVisibleBW'])
            avg_bw = std_bw = 0.0
            # get new config if change is detected. Always get new config after first chunk completes download
            if chd_detected or lastChunkID == 0:
                if lastChunkID == 0:
                  chd_index = 0
                  print "change detected i = ", 0, " chd_index = ", chd_index, " chunk_when_last_chd =", self.input_dict['chunk_when_last_chd_ran'], " len = ", len(self.input_dict['playerVisibleBW'])

                self.input_dict['chunk_when_last_chd_ran'] = chd_index

                avg_bw, std_bw = mpc_tuner_logic.getBWFeaturesWeightedPlayerVisible(\
                                 self.input_dict['playerVisibleBW'], \
                                 self.input_dict['chunk_when_last_chd_ran'])
                cellsize = 1000
                #table = tuner_lookup_tables.dash_syth_hyb_pen_table_900
                table = mpc_lookup_table_4300_default.mpc_dash_syth_hyb_pen_table_4300_default_1000
                ABRChoice, \
                p1_min, \
                p1_median, \
                p1_max = mpc_tuner_logic.getDynamicconfig_mpc(table, \
                                                          avg_bw, \
                                                          std_bw, \
                                                          cellsize)
                # here we will get the discount factor from the table lookup
                self.input_dict['discount'] = p1_max

            mpcBW, \
            harmonic_bandwidth, \
            bandwidthEsts, \
            pastErrors = mpc_tuner_logic.getMPCBW(\
                        self.input_dict['chunkBWSamples'], \
                        self.input_dict['bandwidthEsts'], \
                        self.input_dict['pastErrors'], \
                        self.input_dict['chunksDownloaded'], \
                        self.input_dict['discount'])

            self.input_dict['bandwidthEsts'] = bandwidthEsts
            self.input_dict['pastErrors'] = pastErrors

            quality = mpc_tuner_logic.getMPCDecision(bufferLen, \
                    lastChunkBR, \
                    lastChunkID, \
                    mpcBW)

            #print lastChunkID, lastChunkID + 1, quality
            # log wall_time, bit_rate, buffer_size, rebuffer_time, video_chunk_size, download_time, reward
            self.log_file.write(str(time.time()) + '\t' +
                                str(self.input_dict['chunksDownloaded']) + '\t' +
                                str(VIDEO_BIT_RATE[post_data['lastquality']]) + '\t' +
                                str(round(post_data['buffer'],2)) + '\t' +
                                str(post_data['lastChunkSize']) + '\t' +
                                str(post_data['lastChunkStartTime']) + '\t' +
                                str(post_data['lastChunkFinishTime']) + '\t' +
                                str(round(avg_bw,2)) + '\t' +
                                str(round(std_bw,2)) + '\t' +
                                str(self.input_dict['chunk_when_last_chd_ran']) + '\t' +
                                str(np.mean(self.input_dict['playerVisibleBW'][self.input_dict['chunk_when_last_chd_ran']:])) + '\t' +
                                str(float(post_data['lastChunkFinishTime'] - post_data['lastChunkStartTime'])) + '\t' +
                                str((post_data['lastChunkSize'] * 8)/(float(post_data['lastChunkFinishTime'] - post_data['lastChunkStartTime']))) + '\t' +
                                str(harmonic_bandwidth * 8 * 1000) + '\t' +
                                str(mpcBW) + '\t' +
                                str(self.input_dict['discount']) + '\n')
            self.log_file.flush()


            end_of_video = False
            if ( lastChunkID == TOTAL_VIDEO_CHUNKS):
                end_of_video = True
                print "...SESSION END..."
                self.reset_state()
                self.log_file.write('\n')

            
            send_data_json = json.dumps({'quality': quality, 'config': self.input_dict['discount']})
            send_data = str(quality)
            self.send_response(200)
            #self.send_header('Content-Type', 'text/plain')
            #self.send_header('Content-Length', len(send_data))
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', "*")
            self.end_headers()
            self.wfile.write(send_data_json)

        def do_GET(self):
            print >> sys.stderr, 'GOT REQ'
            self.send_response(200)
            #self.send_header('Cache-Control', 'Cache-Control: no-cache, no-store, must-revalidate max-age=0')
            self.send_header('Cache-Control', 'max-age=3000')
            self.send_header('Content-Length', 20)
            self.end_headers()
            self.wfile.write("console.log('here');")


        def log_message(self, format, *args):
            return

    return Request_Handler


def run(server_class=HTTPServer, port=8336, log_file_path=LOG_FILE):

    assert len(VIDEO_BIT_RATE) == A_DIM

    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)

    with open(log_file_path, 'wb') as log_file:

        discount = 0.0
        chunksDownloaded = 0
        chunk_when_last_chd_ran = -1
        playerVisibleBW = []
        chunkBWSamples = []
        bandwidthEsts = []
        pastErrors = []
        sessionIDs = set()
        sessionHistory = dict()
        input_dict = {'log_file': log_file,
                      'discount': discount,
                      'chunksDownloaded': chunksDownloaded,
                      'chunk_when_last_chd_ran': chunk_when_last_chd_ran,
                      'chunkBWSamples': chunkBWSamples,
                      'playerVisibleBW': playerVisibleBW,
                      'sessionHistory': sessionHistory,
                      'bandwidthEsts': bandwidthEsts,
                      'sessionIDs': sessionIDs,
                      'pastErrors': pastErrors}

        # interface to tuner server
        handler_class = make_request_handler(input_dict=input_dict)

        server_address = ('localhost', port)
        httpd = server_class(server_address, handler_class)
        print 'Listening on port ' + str(port)
        httpd.serve_forever()


def main():
    if len(sys.argv) == 2:
        trace_file = sys.argv[1]
        run(log_file_path=LOG_FILE)
    else:
        run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupted."
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

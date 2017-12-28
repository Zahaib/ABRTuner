import math
### debug settings
DEBUG = False
VERBOSE_DEBUG = False
CHUNK_DEBUG = False

### simulation settings
SIMULATION_STEP = 50
# MEDIAN_BITRATE_MODE = True
CHUNK_AWARE_MODE = True
PS_STYLE_BANDWIDTH = False
VALIDATION_MODE = False
AVERAGE_BANDWIDTH_MODE = False
ESTIMATED_BANDWIDTH_MODE = True
INDUCE_BW_ERROR = False
PRINT_CONFIG_MODE = False
EXPERIMENT_MODE = False
ONCD = False

## chunk interunption
NOINTERUPT = True
ALLINTERUPT  = False
SMARTINTERUPT = False

### Operation mode ###
DATABRICKS_MODE = False
TRACE_MODE = True

### Player settings ###
MAX_BUFFLEN = 12000
LOCK = 0

### ABR selection ###
COMBINATION_ABR = False
UTILITY_BITRATE_SELECTION = False
BANDWIDTH_UTILITY = False
BUFFERLEN_UTILITY = False
BUFFERLEN_BBA1_UTILITY = False
BUFFERLEN_BBA2_UTILITY = False
WEIGHTED_BANDWIDTH = False
MPC_ABR = False
HYB_ABR = False
BOLA_ABR = True

### Video settings
TOTAL_CHUNKS = 49
NUM_BITRATES = 6
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]
VIDEO_BIT_RATE_TO_INDEX = {300:0,750:1,1200:2,1850:3,2850:4,4300:5}
CHUNKSIZE = 4.0


### QoE metric settings
REBUF_PENALTY = 4.3 #100000.0#4.3
SMOOTH_PENALTY = 0.0

### BB settings
conf = {'maxbuflen':120, 'r': 5, 'maxRPct':0.50, 'xLookahead':50}

### MPC settings
WINDOWSIZE = 5

### BOLA settings
MINIMUM_BUFFER_S = 5 #10 # BOLA should never add artificial delays if buffer is less than MINIMUM_BUFFER_S. Orig val: 10
BUFFER_TARGET_S = 30 # If Schedule Controller does not allow buffer level to reach BUFFER_TARGET_S, this can be a virtual buffer level. Orig val: 30
REBUFFER_SAFETY_FACTOR = 0.5 # Used when buffer level is dangerously low, might happen often in live streaming.
BOLA_BITRATES = [br * 1000.0 for br in VIDEO_BIT_RATE]
BOLA_UTILITIES = [math.log(br) for br in BOLA_BITRATES]

### Output stats settings
TRUE_AVG_BITRATE = False

### DYNAMIC settings
DYNAMIC_BSM = False

### COMBINATION ABR settings
COMBINATION_ABR_BW_THRESHOLD = 3000.0
COMBINATION_ABR_CV_THRESHOLD = 1.0

### racecar video settings
#VIDEO_BIT_RATE = [350,600,1000,2000,3000]
#VIDEO_BIT_RATE_TO_INDEX = {350:0,600:1,1000:2,2000:3,3000:4}

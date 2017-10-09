### debug configuration
DEBUG = False
VERBOSE_DEBUG = False

### simulation configuration
# MEDIAN_BITRATE_MODE = True
CHUNK_AWARE_MODE = True
PS_STYLE_BANDWIDTH = False
VALIDATION_MODE = False
TOTAL_CHUNKS  = 0
AVERAGE_BANDWIDTH_MODE = False
ESTIMATED_BANDWIDTH_MODE = True
INDUCE_BW_ERROR = False
PRINT_CONFIG_MODE = False
EXPERIMENT_MODE = False


## chunk interunption
NOINTERUPT = True
ALLINTERUPT  = False
SMARTINTERUPT = False

### Operation mode ###
DATABRICKS_MODE = False
TRACE_MODE = True

### BB ABR configuration
conf = {'maxbuflen':120, 'r': 5, 'maxRPct':0.50, 'xLookahead':50}

### Player properties ###
MAX_BUFFLEN = 30
LOCK = 0

### ABR configuration ###
COMBINATION_ABR = False
UTILITY_BITRATE_SELECTION = True
BANDWIDTH_UTILITY = False
BUFFERLEN_UTILITY = False
BUFFERLEN_BBA1_UTILITY = False
BUFFERLEN_BBA2_UTILITY = False
WEIGHTED_BANDWIDTH = False

### COMBINATION ABR settings
COMBINATION_ABR_BW_THRESHOLD = 3000.0
COMBINATION_ABR_CV_THRESHOLD = 1.0

### DYNAMIC settings
DYNAMIC_BSM = False

### Simulation settings
SIMULATION_STEP = 50

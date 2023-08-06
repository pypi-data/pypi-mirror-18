# BOT Motion Module
#
# SDO Dictionary
#
# Author:      Henrik Stroetgen <hstroetgen@synapticon.com> / <support@synapticon.com>
# Date:        2016-11-19
# Location:    Filderstadt, Germany
#
#
#
#       Copyright (c) 2016, Synapticon GmbH
#       All rights reserved.
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice, this
#          list of conditions and the following disclaimer.
#       2. Redistributions in binary form must reproduce the above copyright notice,
#          this list of conditions and the following disclaimer in the documentation
#          and/or other materials provided with the distribution.
#       3. Execution of this software or parts of it exclusively takes place on hardware
#          produced by Synapticon GmbH.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#       ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#       WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#       DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#       ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#       (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#       LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#       ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#       SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#       The views and conclusions contained in the software and documentation are those
#       of the authors and should not be interpreted as representing official policies,
#       either expressed or implied, of the Synapticon GmbH.
#


SENSOR_POLARITY                 = 0x2004
CIA402_POSITION_ENC_RESOLUTION  = 0x308F
CIA402_MOTOR_SPECIFIC           = 0x2410
COMMUTATION_OFFSET_CLKWISE      = 0x2001
CIA402_CURRENT_GAIN             = 0x20F6 
CIA402_VELOCITY_GAIN            = 0x20F9 
CIA402_POSITION_GAIN            = 0x20FB
CIA402_POLARITY                 = 0x607E
CIA402_MAX_CURRENT              = 0x6073
CIA402_POSITION_RANGELIMIT      = 0x607B
CIA402_MAX_TORQUE               = 0x6072
CIA402_SENSOR_SELECTION_CODE    = 0x606A

sdo_dict = [
    # ************************************************* MOTOR 1 *************************************************
    [
    #      Index,                  Subindex,  , DataType,           Object Code, Bitlength, Obj Acc, Value, Name
        [ CIA402_SENSOR_SELECTION_CODE,   0, 16,  6,        "Sensor Selection Mode" ],
        [ SENSOR_POLARITY,                0, 16,  1,        "Position Sensor Polarity"],
        [ CIA402_POSITION_ENC_RESOLUTION, 0, 32,  65536,    "Position Encoder Resolution" ],

        [ CIA402_MOTOR_SPECIFIC,          1, 32,  5,        "Motor Specific Nominal Current" ],
        [ CIA402_MOTOR_SPECIFIC,          2, 32,  307000,   "Motor Specific Phase Resistance" ],
        [ CIA402_MOTOR_SPECIFIC,          3, 32,  7,        "Motor Specific pole pair number" ],
        [ CIA402_MOTOR_SPECIFIC,          4, 32,  4250,     "Motor Specific Max Speed" ],
        [ CIA402_MOTOR_SPECIFIC,          5, 32,  188,      "Motor Specific Phase Inductance" ],
        [ CIA402_MOTOR_SPECIFIC,          6, 32,  900,      "Motor Specific Torque Constant" ], # MAXIMUM_TORQUE

        [ COMMUTATION_OFFSET_CLKWISE,     0, 16,  936,      "Commutation Offset Clockwise"],
        [ CIA402_POLARITY,                0, 32,  1,        "Polarity" ],
        [ CIA402_MAX_CURRENT,             0, 16,  5390,     "Max Current" ],
        [ CIA402_POSITION_RANGELIMIT,     1, 32,  -0x7fffffff, "Min Postition Range Limit"],
        [ CIA402_POSITION_RANGELIMIT,     2, 32,  0x7fffffff, "Max Postition Range Limit"],
        [ CIA402_MAX_TORQUE,              0, 32,  2500,     "Max Torque" ],

        [ CIA402_VELOCITY_GAIN,           1, 32,  1500,     "Velocity P-Gain" ],
        [ CIA402_VELOCITY_GAIN,           2, 32,  2,        "Velocity I-Gain" ],
        [ CIA402_VELOCITY_GAIN,           3, 32,  0,        "Velocity D-Gain" ],

        [ CIA402_POSITION_GAIN,           1, 32,  2000000,  "Position P-Gain" ], #989500
        [ CIA402_POSITION_GAIN,           2, 32,  150000,   "Position I-Gain" ], #100100
        [ CIA402_POSITION_GAIN,           3, 32,  2000000,  "Position D-Gain" ], #4142100

        [ CIA402_CURRENT_GAIN,            1, 32,  40,       "Current P-Gain" ],
        [ CIA402_CURRENT_GAIN,            2, 32,  40,       "Current I-Gain" ],
        [ CIA402_CURRENT_GAIN,            3, 32,  0,        "Current D-Gain" ],
    ],
]

sdo_ip_id = {
    '192.168.101.221': 0,
    '192.168.101.222': 1,
    '192.168.101.223': 2,
    '192.168.101.224': 3,
}

Not ready !
## Development progress
- [X] Integrated hardware
- [X] Hardware procedures
- [ ] SMS commands
- [ ] Main procedures
- [ ] Documentation

## Command reference
Commands can be send via SMS message or UART interface.
Command has to be writen in this format:
`command arg1 arg2`

### System Commands
| Command | Arguments | Description |
| ------- | --------- | ----------- |
| help    |           | Show all valid commands |
| state   |           | Reports state of all modules and sensors |
| time    |  [HH:MM:SS] | Overwrites system time with argument, if no argument is given returns system time |
| date    | [YY:MM:DD] | Similar to command time write or read system date |
| admin   | [A/D] [number] | With no argument returns all recognized phone numbers; A-add new number, D-delete number |


### Hardware Commands
| Command | Arguments | Description |
| ------- | --------- | ----------- |
| atcmd   | [command] | Sends an AT command from argument to SIM800 module, returns response from module |
| door    | [O/C]     | Force door to change state to argument, if no argument is given returns state; O-open, C-close |
| doormin | [value]   | Set minimal temperature required for door to open, if no argument is given returns current minimal temperature |
| light   | [O/F]     | Set state of light relay to argument, if no argument is given returns state; O-on, F-off |
| heatet  | [O/F]     | Set state of heater relay to argument, if no argument is given returns state; O-on, F-off |
| temp    |           | Returns temperature value from sensor |
| press   |           | Returns atmospheric pressure value form sensor |

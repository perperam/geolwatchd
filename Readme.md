# geolwatchd

## Installation
Make the `install.sh` script executable and run it

```
chmod +x install.sh
./install.sh
```

This will create the working environment, install the python dependencies and copy the systemd service file witch is enabled and started afterwards


## Uninstall
Make the `uninstall.sh` script executable and run it

```
chmod +x uninstall.sh
./uninstall.sh
```

This will remove all files from your system

## Configuration
### Blacklist
The Blacklist can be configured by creating or editing the `blacklist.json` in `/opt/geolwatchd`.
There can be as many areas as you like and there is no limit for the points describing the polygon.Here is an Example configuration:


```json
{
  "example_area": [[10.53735, 60.7325], [10.53735, 59.265], [11.45265, 58.4265], [11.45265, 60.7325]],
  "second_area": [[20.5425, 60.2452], [20.5425, 64.6], [21.01, 62.832]]
}
```

### Subscribers
The Service notifies its subscribers over tcp.
To specify which devices should be notified (host, port) there must be  a `subscribers.json` in `/opt/geolwatchd`.
Here is an example

```json
{
  "example_sub": {
    "host": "localhost",
    "port": 12345
  },
  "second_sub": {
    "host": "localhost",
    "port":  42124
  }
}
```

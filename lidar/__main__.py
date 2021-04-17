from rplidar import RPLidar, RPLidarException
import click
import time
import redis
from typing import Dict, Tuple
from serial.tools import list_ports

def get_device_com(comports, vid_pid_tuple: Tuple[int, int]):
    device_com = [com.device for com in comports
                  if (com.vid, com.pid) == vid_pid_tuple]
    return device_com[0] if len(device_com) else None
    
LIDAR_VID_PID = (4292, 60000)
comports = list(list_ports.comports())
lidar_dev_com = get_device_com(comports, LIDAR_VID_PID)
client = redis.Redis()


@click.command()
@click.option("--port", type=str, default=lidar_dev_com)
@click.argument("start", type=click.INT)
@click.argument("stop", type=click.INT)
def main(port, start, stop):
    lidar = RPLidar(port)

    while True:
        # summation = 0
        # noElement = 1
        min_dist = 999999

        try:
            scan = next(lidar.iter_scans(max_buf_meas=200, min_len=3))
            for i, sample in enumerate(scan):
                if int(sample[1]) > start and int(sample[1]) < stop:
                    print(str(sample[2]))
                    if int(sample[2]) < min_dist:
                        min_dist = sample[2]
            client.set("min", min_dist)
            #         summation = summation + sample[2]
            #         noElement = noElement + 1
            #         #print(sample[1], "  ", sample[2])
            # print("\n\n -------------------------------- \n\n")
            # print("Avg. of the interval [" + str(start) +
            #       ", " + str(stop) + "] is " + str(summation/noElement))
            # print("\n\n -------------------------------- \n\n")

            # return min
            # print("\n\n--------------------------\nmin: " +
            #       str(min) + "\n---------------------------------\n\n")

        except RPLidarException as e:
            pass
        finally:
            lidar.stop()


main()

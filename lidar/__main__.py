from rplidar import RPLidar, RPLidarException
import click
import time
import redis

client = redis.Redis()


@click.command()
@click.argument("port")
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

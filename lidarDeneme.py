from rplidar import RPLidar
lidar = RPLidar("COM13")

while True:
    scan = next(lidar.iter_scans())
    lidar.stop()
    angle_start = input("Gimme start of the angle interval bro")
    angle_end = input("Gimme end of the angle interval bro")

    for i, sample in enumerate(scan):
        if int(sample[1]) > int(angle_start) and int(sample[1]) < int(angle_end):
            print(sample[1], "  ", sample[2])

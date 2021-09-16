import glob

from astropy.io import fits


file_list = glob.glob("BAT_157m_eight_band_monthly_lightcurve/*.*")


f = fits.open(file_list[0])


Time = f[1].data["TIME"]

Rate = f[1].data["RATE"]

Rateerror = f[1].data["RATE_ERR"]

Name = f[1].data["NAME"][0]

Raobj = f[1].data["RA_OBJ "][0]

Decobj = f[1].data["DEC_OBJ"][0]


data = [[[Time, Rate, Rateerror]], [Name], [Raobj, Decobj]]


print(data[1])


fakelist = file_list[0:2]


data1 = [[], [], []]


for a in file_list:

    temp = [Time, Rate, Rateerror]

    file1 = fits.open(a)

    Time = file1[1].data["TIME"]

    Rate = file1[1].data["RATE"]

    Rateerror = file1[1].data["RATE_ERR"]

    Name = file1[1].data["NAME"][0]

    Raobj = file1[1].data["RA_OBJ "][0]

    Decobj = file1[1].data["DEC_OBJ"][0]

    data1[0].append([Time, Rate, Rateerror])

    data1[1].append(Name)

    data1[2].append([Raobj, Decobj])


print(data1[0][0][0])

f = open("sinhvien.txt", 'a')

while True:
    masv = input("Nhap: ")
    if masv == "":
        break

    f.write("\t".join([masv]) + "\n")
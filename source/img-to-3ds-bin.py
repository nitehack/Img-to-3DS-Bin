# -*- coding: utf-8 -*-
"""
IMG TO 3DS BIN

@author: nitehack
"""
import sys

def alignment(num):
    alin=0
    if (num%4) != 0:
        c=int(num/4)
        alin=(c+1)*4-num
    return alin

hmax_3ds=400
vmax_3ds=240

try:
    orig=sys.argv[1]
    dest=sys.argv[2]
except:
    print "Usage: python img-to-3ds-bin.py image.bmp image.bin"
    exit()

try:
    imagen=open(orig,"rb")
except:
    print "EROR: The image file is not found. Check that the route is correct"
    exit()

imagen.seek(0x02)
tam_file=imagen.read(4)

imagen.seek(0x0A)
ini_imagen=imagen.read(4)

imagen.seek(0x12)
tam_h=imagen.read(4)

imagen.seek(0x16)
tam_v=imagen.read(4)

imagen.seek(0x1C)
codi=imagen.read(2)

imagen.seek(0x1E)
compa=imagen.read(4)

imagen.seek(0x22)
tam_imagen=imagen.read(4)

tamano=int(tam_file[::-1].encode("hex"),16) #Invertimos la cadena y la convertimos a hexadecimal
width=int(tam_h[::-1].encode("hex"),16)
height=int(tam_v[::-1].encode("hex"),16)
comp=int(compa[::-1].encode("hex"),16)
cod=int(codi[::-1].encode("hex"),16)
inicio=int(ini_imagen[::-1].encode("hex"),16)
tam_img_total=int(tam_imagen[::-1].encode("hex"),16)

num_pix=height*width
imagen_bin=""
alin=alignment(width*3) #alineamiento tiene que ser cada linea multiplo de 4


#identificar distintos tipos de codificaciones, futuro
if cod == 24:
    saltos=3
else:
    saltos=0
    
#Solo para BMP de 24 bits sin comprimir
if (width<=hmax_3ds) and (height<=vmax_3ds):
    if cod == 24:
        if comp == 0:
            imagen.seek(inicio)
            datos_imagen=imagen.read(tam_img_total)

            for j in range(width):
                for i in range(height):
                    k=i*(width*saltos+alin)+j*saltos
                    imagen_bin+=datos_imagen[k:(k+saltos)] #ordenamos los datos
            try:
                bin_file=open(dest,"w")
            except:
                print "ERROR: There was a problem creating the file"
                exit()

            bin_file.write(imagen_bin)
            bin_file.close()
            print "Creado satisfactoriamente"

            
imagen.close()

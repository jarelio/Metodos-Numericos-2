#-*- coding: utf-8 -*-
from PIL import Image

# Abrindo Imagem no Formato 'Image'
normal_image = Image.open('test-image.jpg')

#Printa largura e altura da imagem
print(normal_image.size)

# Criando Image em Grayscale
grayscale_image = normal_image.convert('L')

# Salvando a imagem em Grayscale em disco
#grayscale_image.save('image-grayscale.jpg')

# Recebe coordenadas da imagem
def function(image, position):
    # Retorna valor do pixel
    return image.getpixel(position)

def forward(image, position, direction):
        if(direction == 'x'):
                xi = position
                xi1 = (position[0]+1,position[1])
                #print(xi, xi1)
                fxi = function(image, xi)
                fxi1 = function(image, xi1)
                f_xiderivated = abs(fxi1 - fxi)
                return f_xiderivated
        if(direction == 'y'):
                xi = position
                xi1 = (position[0],position[1]+1)
                #print(xi, xi1)
                fxi = function(image, xi)
                fxi1 = function(image, xi1)
                f_xiderivated = abs(fxi1 - fxi)
                return f_xiderivated

def central(image, position, direction):
        if(direction == 'x'):
                ximinor1 = (position[0]-1,position[1])
                xi1 = (position[0]+1,position[1])
                #print(ximinor1,xi,xi1)
                fximinor1 = function(image, ximinor1)
                fxi1 = function(image, xi1)
                f_xiderivated = abs(fxi1 - fximinor1)/2
                return f_xiderivated
        if(direction == 'y'):
                ximinor1 = (position[0],position[1]-1)
                xi1 = (position[0],position[1]+1)
                #print(ximinor1,xi1)
                fximinor1 = function(image, ximinor1)
                fxi1 = function(image, xi1)
                f_xiderivated = abs(fxi1 - fximinor1)/2
                return f_xiderivated

def backward(image, position, direction):

        if(direction == 'x'):
                xi = position
                ximinor1 = (position[0]-1,position[1])
                #print(xi, ximinor1)
                fxi = function(image, xi)
                fximinor1 = function(image, ximinor1)
                f_xiderivated = abs(fxi-fximinor1)
                return f_xiderivated
        if(direction == 'y'):
                xi = position
                ximinor1 = (position[0],position[1]-1)
                #print(xi, ximinor1)
                fxi = function(image, xi)
                fximinor1 = function(image, ximinor1)
                f_xiderivated = abs(fxi-fximinor1)
                return f_xiderivated


# Cria a imagem que receberá a mascara nova
masc_image_x = grayscale_image.copy()
masc_image_y = grayscale_image.copy()

# Recebe valor de altura e largura da imagem (último pixel da 'direita' e último pixel de 'baixo')

width, height = masc_image_x.size
#Trabalhando percorrendo da esquerda pra direita da imagem (percorrendo por colunas)

#Plano de execução em X

# Laço de repetição para utilização do Forward (Todos os pixels da primeira coluna da imagem)
for h in range(0, height):
        masc_image_x.putpixel( (0,h), forward(grayscale_image, (0,h), 'x') )

# Laço de repetição para utilização do Central (Todos os pixels das colunas e linhas centrais)
for w in range(1, width-1):
    for h in range(0, height):
        masc_image_x.putpixel( (w,h), int(central(grayscale_image, (w,h), 'x')) )

# Laço de repetição para utilização do Backward (Todos os pixels da última coluna da imagem)
for h in range(0, height):
    masc_image_x.putpixel( (width-1,h) , backward(grayscale_image, (width-1,h), 'x') )

#masc_image_x.save('image-mascX.jpg')

#Plano de Execução em Y

# Laço de repetição para utilização do Forward (Todos os pixels da primeira linha da imagem)
for w in range(0, width):
        masc_image_y.putpixel( (w,0), forward(grayscale_image, (w,0), 'y') )
# Laço de repetição para utilização do Central (Todos os pixels das colunas e linhas centrais)
for h in range(1, height-1):
    for w in range(0, width):
        masc_image_y.putpixel( (w,h), int(central(grayscale_image, (w,h), 'y')) )
# Laço de repetição para utilização do Backward (Todos os pixels da última linha da imagem)
for w in range(0, width):
    masc_image_y.putpixel( (w,height-1) , backward(grayscale_image, (w,height-1), 'y') )

#masc_image_y.save('image-mascY.jpg')

# Cria a imagem aplicando o treshold
treshimage_x = masc_image_x.copy()
treshimage_y = masc_image_y.copy()
treshold = 10

# Percorre todos os pixels verificando o treshold
for x in range(0, height):
    for y in range(0, width):
        if(masc_image_x.getpixel((y,x))>=treshold):
                treshimage_x.putpixel( (y,x),  255)
        else:
                treshimage_x.putpixel( (y,x), 0)

        if(masc_image_y.getpixel((y,x))>=treshold):
                treshimage_y.putpixel( (y,x), 255)
        else:
                treshimage_y.putpixel( (y,x), 0)

treshimage_x.save('image-tresh_x.jpg')
treshimage_y.save('image-tresh_y.jpg')

# Receives any of the images (x or y) for joining them
complete_image = treshimage_x.copy()
for h in range(0, height):
    for w in range(0, width):
            pixel_y = treshimage_y.getpixel((w,h))
            if(complete_image.getpixel((w,h)) < pixel_y):
                complete_image.putpixel((w,h),pixel_y)

complete_image.save('complete_image.jpg')
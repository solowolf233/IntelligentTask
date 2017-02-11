# -*- coding:utf-8 -*

from PIL import Image,ImageDraw,ImageFont
import random
class ImageChar():
    def __init__(self,size = (100,40),fontPath='arial.ttf',bgColor=(255,255,255),
                 fontsize=20):
        self.size=size
        self.fontPath=fontPath
        self.bgColor=bgColor
        self.fontSize=fontsize
        self.image = Image.new('RGB',size,bgColor)
        self.font = ImageFont.truetype(self.fontPath,self.fontSize)

    #随机字母:
    def rndChar(self):
        return chr(random.randint(65,90))

    #随机颜色
    def rndColor(self):
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

    # 随机颜色2:
    def rndColor2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def randImage(self,num):
        strRes = ''
        #创建Draw对象
        draw = ImageDraw.Draw(self.image)
        #填充每个像素
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                draw.point((x,y),fill=self.rndColor())
        #输出文字
        for t in range(num):
            char = self.rndChar()
            strRes += char
            draw.text((20*t+10,5),char,font=self.font,fill=self.rndColor2())
        #模糊
        # image = self.image.filter(ImageFilter.BLUR)
        # self.image.save('app/static/images/randImage/rand.jpg','jpeg')

        return self.image,strRes
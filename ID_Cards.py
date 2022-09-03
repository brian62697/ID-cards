import pandas as pd
from PIL import Image, ImageOps, ImageDraw, ImageFont
import sys

#fonts to be used
font_league_spartan = ImageFont.truetype("LeagueSpartan-SemiBold.ttf", size = 50)
font_mont_student = ImageFont.truetype('Montserrat-Regular.ttf', size = 45)
font_mont_id = ImageFont.truetype('Montserrat-Regular.ttf', size = 40)

#User to input data until one is recognised
def get_file():
    while True:
        student_data = input("Hi Mel, please enter your csv file: ")
        try:
            df = pd.read_csv(student_data)
            data = df.to_dict(orient='record')
            break
        except: 
            try_again = input('No file exists, do you want to try again?(y/n) ').lower()
            if try_again == 'y':
                continue
            else:
                sys.exit()

#Two new key value pairs are made: 
# key = full_name2 removing '/' since it cannot be used in saving a file name
# key = length_name to determine names that are too long later in code            
    for person in data: 
        try:
            person['length_name'] = len(person['Full Name'])
            person['full_name2'] = ''.join(list(filter(lambda ch: ch not in "/", person['Full Name'])))
        except:
            continue
    
    return data



#creating a circular image and pasting it onto the template creating a new background
def create_circle(image):
    background = Image.open('ID card template.PNG')
    im1 = Image.open(image)  #opens the image
    im1 = ImageOps.exif_transpose(im1) #keeps image orientation
    im = im1.crop((300, 500, 3700, 3900)) #crops the image a square based on a 4000*6000 sized image to ensure it doesn't stretch in the resizing
    im = im.resize((377, 377)); #resizes the image
    bigsize = (im.size[0]*3, im.size[1]*3) #creates a tuple with the elements being 3 times the size of the image
    mask = Image.new('L', bigsize, 0) #creates a black image, L is a mode and stands for  (8-bit pixels, black and white), 0 is the colour black
    draw = ImageDraw.Draw(mask) #lets us draw on mask
    draw.ellipse((0, 0) + bigsize, fill=255) #creates a circle in the centre the size of big size
    mask = mask.resize(im.size) #resizes the image based on our original image size
    im.putalpha(mask) 
    output = ImageOps.fit(im, mask.size, centering=(0.1, 0.1))
    output.putalpha(mask)
    background.paste(im, (126, 222), im)
    return background

#for photos that don't have a dimension of 4000*6000. The image is cropped based on the size of the image. The width remains the same while 1/15th of the height is cut off
def create_circle_cropped(image):
    background = Image.open('ID card template.PNG')
    im1 = Image.open(image)  #opens the image
    im1 = ImageOps.exif_transpose(im1)
    x, y = im1.size
    im = im1.crop((0, (1/15)*y, x, x+(1/15)*y))
    # im = im1.crop(((3/40)*width, height*(1/15), width-(6/40)*width, width-(3/40)*width + height*(1/15)))
    # im = im1.crop((300, 400, 3700, 3800))
    im = im.resize((377, 377)); #resizes the image
    bigsize = (im.size[0]*3, im.size[1]*3) #creates a tuple with the elements being 3 times the size of the image
    mask = Image.new('L', bigsize, 0) #creates a black image, L is a mode and stands for  (8-bit pixels, black and white), 0 is the colour black
    draw = ImageDraw.Draw(mask) #lets us draw on mask
    draw.ellipse((0, 0) + bigsize, fill=255) #creates a circle in the centre the size of big size
    mask = mask.resize(im.size) #resizes the image based on our original image size
    im.putalpha(mask) 
    output = ImageOps.fit(im, mask.size, centering=(0.1, 0.1))
    output.putalpha(mask)
    background.paste(im, (126, 222), im)
    return background

def add_details_short(background, name, ID):
    draw = ImageDraw.Draw(background)
    draw.text(
            xy=(313, 670),
            text=f"{name}",
            fill="#000000",
            font=font_league_spartan,
            anchor="mm",
            align="center"
        )

    draw.text(
            xy=(313, 794),
            text="STUDENT",
            fill="#000000",
            font=font_mont_student,
            anchor="mm",
            align="center"
        )

    draw.text(
            xy=(313, 856),
            text=f'ID: {ID}',
            fill="#000000",
            font=font_mont_id,
            anchor="mm",
            align="center"
        )
    return background

#If the persons name is too long, it splits it into two lines on the ID
def add_details_long(background, name, ID, font = font_league_spartan):
    name = name.split(' ')
    first_name = ' '.join(name[0:2])
    last_name = ' '.join(name[2:])
    draw = ImageDraw.Draw(background)
    # draw.text((120, 663), "Brian Ung", font = font_league_spartan, fill = 'black')
    draw.text(
            xy=(313, 670),
            text=f"{first_name}",
            fill="#000000",
            font=font,
            anchor="mm",
            align="center"
        )

    draw.text(
            xy=(313, 731),
            text=f"{last_name}",
            fill="#000000",
            font=font,
            anchor="mm",
            align="center"
        )
    
    draw.text(
            xy=(313, 794),
            text="STUDENT",
            fill="#000000",
            font=font_mont_student,
            anchor="mm",
            align="center"
        )

    draw.text(
            xy=(313, 856),
            text=f'ID: {ID}',
            fill="#000000",
            font=font_mont_id,
            anchor="mm",
            align="center"
        )
    return background


def make_id(data):
    for person in data:
        if type(person['Full Name']) == float: #checking for empty cell
            continue
        if type(person['Photo']) == float: #checking for whether there is an attached photo or not
            print(f"{person['Full Name']} didn't have a photo")
            continue

        elif person['length_name'] > 33:
            try: 
                smaller_font = ImageFont.truetype("LeagueSpartan-SemiBold.ttf", size = 35)
                if person['Cropped'] == 'Y':
                    background = create_circle_cropped(person['Photo'])
                else:
                    background = create_circle(person['Photo'])
                ID_card = add_details_long(background, person['Full Name'], person['ID'], smaller_font)
                ID_card.save(f"{person['Grade']} {person['full_name2']} ID_card.PNG")
            except:
                print(f"Failed for {person['Full Name']}")
                continue  
            
        elif person['length_name'] < 17:
            try: 
                if person['Cropped'] == 'Y':
                    background = create_circle_cropped(person['Photo'])
                else:
                    background = create_circle(person['Photo'])
                ID_card = add_details_short(background, person['Full Name'], person['ID'])
                ID_card.save(f"{person['Grade']} {person['full_name2']} ID_card.PNG")
            except:
                print(f"Failed for {person['Full Name']}")
                continue 

        else:
            try: 
                if person['Cropped'] == 'Y':
                    background = create_circle_cropped(person['Photo'])
                else:
                    background = create_circle(person['Photo'])
                ID_card = add_details_long(background, person['Full Name'], person['ID'])
                ID_card.save(f"{person['Grade']} {person['full_name2']} ID_card.PNG")
            except:
                print(f"Failed for {person['Full Name']}")
                continue 


if __name__ == '__main__':
    data = get_file()
    make_id(data)
    print('Have a good day Mel!')



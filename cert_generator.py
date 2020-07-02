from PIL import Image, ImageDraw, ImageFont
import pandas as pd


csv_data = pd.read_csv('names.csv')
name_list = csv_data['Name'].to_list()
college_name_list = csv_data['College'].to_list()
data = zip(name_list, college_name_list)

def generate_certs(name, college_name) :
    im = Image.open('cert_template.png')
    image = Image.new('RGB', im.size, (255, 255, 255))
    image.paste(im, mask=im.split()[3])
    d = ImageDraw.Draw(image)
    #coordinates
    name_coord_x, name_coord_y = (1010,594)
    of_coord_x, of_coord_y = (999,682)
    college_name_coord_x, college_name_coord_y = (1001,749)
    text_color = '#000000'
    #fonts
    font_for_name = ImageFont.truetype("MontserratBold.ttf", 90)
    font_for_of = ImageFont.truetype("MontserratLight.ttf", 40)
    font_for_college_name = ImageFont.truetype("MontserratBold.ttf", 50)
    #lineheights
    name_line_width, name_line_height = d.textsize(name, font_for_name)
    of_line_width, of_line_height = d.textsize('of', font_for_of)
    college_name_line_width, college_name_line_height = d.textsize(college_name, font_for_college_name)
    #writting on image
    d.text((name_coord_x-name_line_width/2, name_coord_y-name_line_height/2), name, fill=text_color, font=font_for_name)
    d.text((of_coord_x-of_line_width/2, of_coord_y-of_line_height/2), 'of', fill=text_color, font=font_for_of)
    d.text((college_name_coord_x-college_name_line_width/2, college_name_coord_y-college_name_line_height/2), college_name, fill=text_color, font=font_for_college_name)
    image.save("./generated_certificates/" + name + ".pdf")
    print('saving cert of: ' + name)


for name,college in data:
    generate_certs(name, college)

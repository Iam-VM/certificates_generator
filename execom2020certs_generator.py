import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


# creating dir for saving
MAIN_DIR_NAME = "Execom2020Certificates"

# taking in data
csv_data = pd.read_csv('cert_data.csv')
csv_data.dropna()
event_names = csv_data['event_name'].to_list()
# processing coordinators list
coordinator_names_unprocessed = csv_data['coordinator_names'].to_list()
coordinator_names_unstripped = [y.strip(',').split(',') for y in coordinator_names_unprocessed]
coordinator_names = []
for x in coordinator_names_unstripped:
    k = []
    for y in x:
        k.append(y.strip())
    coordinator_names.append(k)
# processing volunteers list
volunteer_names_unprocessed = csv_data['volunteer_names'].to_list()
volunteer_names_unstripped = [y.strip(',').split(',') for y in volunteer_names_unprocessed]
volunteer_names = []
for x in volunteer_names_unstripped:
    k = []
    for y in x:
        k.append(y.strip())
    volunteer_names.append(k)
# zipping data for grouping events with details
cert_data = zip(event_names, coordinator_names, volunteer_names)


def generate_cert_for_event(event_name, coordinators, volunteers):

    # loading and drawing images
    coord_template = Image.open('coord_template.png')
    vol_template = Image.open('volunteer_template.png')
    coord_image = Image.new('RGB', coord_template.size, (255, 255, 255))
    vol_image = Image.new('RGB', vol_template.size, (255, 255, 255))
    coord_image.paste(coord_template, mask=coord_template.split()[3])
    coord_image_drawn = ImageDraw.Draw(coord_image)
    vol_image.paste(vol_template, mask=vol_template.split()[3])
    vol_image_drawn = ImageDraw.Draw(vol_image)

    # coordinates config
    event_name_x, event_name_y = (1010, 594)
    coord_name_x, coord_name_y = (999, 682)
    vol_name_x, vol_name_y = (999, 682)

    # color config
    text_color = '#000000'

    # fonts config
    event_name_font = ImageFont.truetype("MontserratBold.ttf", 90)
    coord_name_font = ImageFont.truetype("MontserratLight.ttf", 40)
    vol_name_font = ImageFont.truetype("MontserratLight.ttf", 40)

    # obtaining line size of event_name (height and width)
    event_name_line_width, event_name_line_height = coord_image_drawn.textsize(event_name, event_name_font)

    # writing event name
    coord_image_drawn.text((event_name_x - event_name_line_width / 2, event_name_y - event_name_line_height / 2), event_name, fill=text_color, font=event_name_font)
    vol_image_drawn.text((event_name_x - event_name_line_width / 2, event_name_y - event_name_line_height / 2), event_name, fill=text_color, font=event_name_font)

    if coordinators[0] != "None":
        # generating dir for coord
        Path(MAIN_DIR_NAME + "/" + event_name + "/" + "Coordinators").mkdir(parents=True)
        for coordinator in coordinators:
            coord_name_line_width, coord_name_line_height = coord_image_drawn.textsize(coordinator, coord_name_font)
            coord_image_drawn.text((coord_name_x - coord_name_line_width / 2, coord_name_y - coord_name_line_height / 2), coordinator, fill=text_color, font=coord_name_font)
            coord_image.save("./Execom2020Certificates/" + event_name + "/Coordinators/" + coordinator + ".pdf")
            print('Saving certificate of coordinator [' + event_name + '] - ' + coordinator)

    if volunteers[0] != "None":
        # generating dir for vol
        Path(MAIN_DIR_NAME + "/" + event_name + "/" + "Volunteers").mkdir(parents=True)
        for volunteer in volunteers:
            vol_name_line_width, vol_name_line_height = vol_image_drawn.textsize(volunteer, vol_name_font)
            vol_image_drawn.text((vol_name_x - vol_name_line_width / 2, vol_name_y - vol_name_line_height / 2), volunteer, fill=text_color, font=vol_name_font)
            vol_image.save("./Execom2020Certificates/" + event_name + "/Volunteers/" + volunteer + ".pdf")
            print('Saving certificate of volunteer [' + event_name + '] - ' + volunteer)


for event_tuple in tuple(cert_data):
    generate_cert_for_event(event_tuple[0],  event_tuple[1], event_tuple[2])

print("Completed.")

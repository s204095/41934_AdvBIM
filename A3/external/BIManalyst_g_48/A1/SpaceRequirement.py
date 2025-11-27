import ifcopenshell

def check_space_requirement(model, requirement_nam, requirement_num):
    spaces = model.by_type("IfcSpace")
    meeting_room = []

    for space in spaces:
        # Go through all spaces and pick out the ones of the desired type
        if space.LongName == requirement_nam:
            # Take all spaces of required kind and put into a list to see how many of the space type there is
            meeting_room.append(int(space.Name))
        else:
            continue
    if len(meeting_room) == requirement_num:
        print(f'The requirement of {requirement_nam} = {requirement_num} is fulfilled')
    elif len(meeting_room) > requirement_num:
        print(f'There are {len(meeting_room)} {requirement_nam} in the model which is more than the required {requirement_num}')
    elif len(meeting_room) < requirement_num:
        print(f'There are {len(meeting_room)} {requirement_nam} in the model which is less than the required {requirement_num}')
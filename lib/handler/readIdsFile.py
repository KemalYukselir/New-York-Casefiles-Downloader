def readIds():
  # Read ids file with all ids needed
  with open('ids.txt') as file:
    lines = file.readlines()
    lines = [line.replace(' ', '').replace("\n","") for line in lines]
    lines.pop(0)

    return lines

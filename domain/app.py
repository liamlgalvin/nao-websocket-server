
import base64
from infrastucture.dto.app import AppDto


class App:
  def __init__(self, id, name, description, image, location, language):
    self.id = id
    self.name = name
    self.description = description
    self.image = image
    self.location = location
    self.language = language

  def getCommand(self):
    return [self.language, self.location]

  def getShellCommand(self):
    if self.language in ["python", "python3"]:
      return "{} {}".format(self.language, self.location)
    elif self.language in ["c", "c++", "cpp"]:
      return "{}".format(self.location)



  def mapToDto(self):
    with open(self.image, "rb") as image_file:
      data = base64.b64encode(image_file.read())
      bitmap_image = data.decode('utf-8')
    return AppDto(self.id, self.name, self.description, bitmap_image)

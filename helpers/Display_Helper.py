class Display_Helper:
    def text_file(self, file_path):
        with open(file_path, 'r') as file:
            print(file.read())

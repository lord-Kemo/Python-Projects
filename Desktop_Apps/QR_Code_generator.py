import qrcode

class MyQR:
    def __init__(self, size: int , padding:int):
        self.qr = qrcode.QRCode(box_size=size, border=padding)
        
        
    def create_qr(self, file_name: str, fg: str, bg: str):
        user_input = input("Enter the data to be encoded: ")
        try:
            self.qr.add_data(user_input)
            qr_image = self.qr.make_image(fill_color=fg, back_color=bg)
            qr_image.save(file_name)
            print(f"QR code created successfully!{file_name}")
        except Exception as e:
            print(f"Error: {e}")
            

def main():
    myqr = MyQR(10, 5)
    myqr.create_qr("Discord_server_invite_link.png", "black", "white")

if __name__ == "__main__":
    main()
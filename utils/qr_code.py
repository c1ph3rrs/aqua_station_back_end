import qrcode

dynamic_link = "https://yourapp.page.link/xyz123"

# Generate QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(dynamic_link)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("app_redirect_qr.png")

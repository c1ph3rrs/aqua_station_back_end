import qrcode

dynamic_link = "http://aqua-station-dynamic-link.s3-website-us-east-1.amazonaws.com"

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

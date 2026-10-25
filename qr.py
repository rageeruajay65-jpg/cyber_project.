import qrcode

# URL of your third HTML page
page3_url = "https://rageeruajay65-jpg.github.io/verifier/"

# Generate the QR code
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4
)

qr.add_data(page3_url)
qr.make(fit=True)

# Create and save the QR image
img = qr.make_image(fill_color="black", back_color="white")
img.save("githubio.png")

print("QR code generated successfully!")

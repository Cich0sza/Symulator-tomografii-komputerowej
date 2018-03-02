import sinogram

sinogram = sinogram.Sinogram("Images_for_tests/test.png", number_of_emitters=200, experimental=True)

# sinogram.save_as_image("output3.png")
sinogram.reverse()

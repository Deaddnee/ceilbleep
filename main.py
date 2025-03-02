#prequesites
test10mb = "./mp3/10mbtestr.mp3"
import	pygame
pygame.init()
pygame.mixer.init()

# i don't like running the server every test..
testque = input("test? (y/n): ")
if testque == "n":
	from http.server import SimpleHTTPRequestHandler, test
	test(SimpleHTTPRequestHandler)
else:
	print("Server init skipped")

pygame.mixer.music.load(test10mb)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
	pygame.time.Clock().tick(10)
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
#Gabriel Lessard - Samy Tétrault - Guillaume Légaré 
#Laboratoire 5 - KF2

import cv2

class Caméra:

    global PORT_CAMERA
    PORT_CAMERA = 0

    def __init__(self):
        self.vcap = cv2.VideoCapture(PORT_CAMERA)
        self.modele = cv2.cvtColor(cv2.imread("modele-objet.bmp"),cv2.COLOR_BGR2GRAY)
        self.lit_une_image = True
        self.image_modele = None
        
    def set_resolution_camera(self):
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT,240) 
        
    def creation_modele(self):
        self.set_resolution_camera()
        while self.lit_une_image:
            ok,image = self.vcap.read()
            if not ok:
                print("Erreur avec l'image!")
                break
            cv2.imshow("Labo 5", image)
            touche = cv2.waitKey(33)
            if touche == ord('q'):
                self.lit_une_image = False
                break
        self.image_modele = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
        cv2.imwrite("image_modele.bmp", self.image_modele)
        self.vcap.release()
        cv2.destroyAllWindows()

    def trouver_modele(self):
        self.set_resolution_camera()
    
        while self.lit_une_image:
            ok,image = self.vcap.read()
            if not ok:
                print("Erreur avec l'image!")
                break
            cv2.imshow("Labo 5", image)
            image_en_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #print(f"img:{image_en_gris.shape}")   
            #print(f"mod:{self.modele.shape}")   
            res = cv2.matchTemplate(image_en_gris, self.modele, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            touche = cv2.waitKey(33)
            if touche == ord('q'):
                self.lit_une_image = False
                break
        print(max_loc)
        self.vcap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Caméra()
    cam.trouver_modele()
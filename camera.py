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
        self.mask = cv2.imread("mask-objet.bmp")
        self.frame_roi = None
        
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
            image_en_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            res = cv2.matchTemplate(image_en_gris, self.modele, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            xMin,yMin= min_loc
            xMax,yMax = max_loc
            self.frame_roi = image[yMin:yMax, xMin:xMax]
            touche = cv2.waitKey(33)
            image_roi = cv2.rectangle(image,self.frame_roi[0],self.frame_roi[1],(175,175,175),2) 
            cv2.imshow("Labo 5", image_roi)
            if touche == ord('q'):
                self.lit_une_image = False
                break
        self.vcap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Caméra()
    cam.trouver_modele()
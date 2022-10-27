#Gabriel Lessard - Samy Tétrault - Guillaume Légaré 
#Laboratoire 5 - KF2
import cv2
from time import sleep
class Caméra:

    global PORT_CAMERA
    PORT_CAMERA = 0

    def __init__(self,width_photo,height_photo):
        self.vcap = cv2.VideoCapture(PORT_CAMERA)
        self.lit_une_image = True
        self.WIDTH_ROI_MARGIN = 25
        self.HEIGTH_ROI_MARGIN = 25
        self.x1_modele = 0
        self.y1_modele = 0
        self.x2_modele = width_photo - 1
        self.y2_modele = height_photo - 1
        self.SEUIL_ACCEPTATION = 0.27
        self.WIDTH_PHOTO = width_photo - 1
        self.HEIGHT_PHOTO = height_photo - 1
        
    def set_resolution_camera(self):
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH,self.WIDTH_PHOTO + 1)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.HEIGHT_PHOTO + 1) 

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
        # Vas chercher le modele, le masque et les dimensions
        self.modele = cv2.cvtColor(cv2.imread("modele-objet.bmp"),cv2.COLOR_BGR2GRAY)
        height_modele,width_modele = self.modele.shape[:2]
        self.mask = cv2.cvtColor(cv2.imread("mask-objet.bmp"),cv2.COLOR_BGR2GRAY)
        while self.lit_une_image:
            # Lis une image et la convertie en gris 
            ok,image = self.vcap.read()
            if not ok:
                print("Erreur avec l'image!")
                break
            image_en_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Verifie si l'on doit chercher dans toute l'image ou le roi
            if self.x2_modele == self.WIDTH_PHOTO :
                #MatchTemplate dans toute l'image
                res = cv2.matchTemplate(image_en_gris, self.modele, cv2.TM_CCOEFF_NORMED,None,self.mask)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                xMax,yMax = max_loc
            else:
                #MatchTemplate dans le roi
                image_gris_roi = image_en_gris[self.y1_modele:self.y2_modele , self.x1_modele:self.x2_modele]
                res = cv2.matchTemplate(image_gris_roi, self.modele, cv2.TM_CCOEFF_NORMED,None,self.mask)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                xMax,yMax = max_loc
                xMax = xMax + self.x1_modele
                yMax = yMax + self.y1_modele

            # Vas chercher les valeurs des resultats du matchTemplate

            # Verifier si on a trouver l'objet selon notre seuil d'acceptation et change les valeurs pour la prochaine iterations
            # Bug potentielle : il se peut que lon doit faire WIDTH_PHOTO - 1 et HEIGHT_PHOTO -1 
            if max_val > self.SEUIL_ACCEPTATION:
                self.x1_modele = xMax - self.WIDTH_ROI_MARGIN
                if self.x1_modele < 0 : 
                    self.x1_modele = 0
                self.x2_modele = xMax + width_modele + self.WIDTH_ROI_MARGIN
                if self.x2_modele > self.WIDTH_PHOTO : 
                    self.x2_modele = self.WIDTH_PHOTO
                self.y1_modele = yMax - self.HEIGTH_ROI_MARGIN
                if self.y1_modele < 0 : 
                    self.y1_modele = 0
                self.y2_modele = yMax + height_modele + self.HEIGTH_ROI_MARGIN
                if self.y2_modele > self.HEIGHT_PHOTO : 
                    self.y2_modele = self.HEIGHT_PHOTO
                print(max_val)
                #Dessiner rectangle de l'objet trouver
                image_avec_objet = cv2.rectangle(image,(self.x1_modele + self.WIDTH_ROI_MARGIN,self.y1_modele + self.HEIGTH_ROI_MARGIN),(self.x2_modele - self.WIDTH_ROI_MARGIN,self.y2_modele - self.HEIGTH_ROI_MARGIN),(0,255,0),2)
                # Dessiner rectangle du ROI
                image_avec_roi = cv2.rectangle(image_avec_objet,(self.x1_modele,self.y1_modele),(self.x2_modele,self.y2_modele),(0,0,255),2)
            else :
                self.x1_modele = 0
                self.x2_modele = self.WIDTH_PHOTO
                self.y1_modele = 0
                self.y2_modele = self.HEIGHT_PHOTO
                # Dessiner rectangle du ROI
                image_avec_roi = cv2.rectangle(image,(self.x1_modele,self.y1_modele),(self.x2_modele,self.y2_modele),(0,0,255),2)

            cv2.imshow("Labo 5",image_avec_roi)
            touche = cv2.waitKey(33)
            if touche == ord('q'):
                self.lit_une_image = False
                break
        self.vcap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Caméra(320,240)
    cam.trouver_modele()
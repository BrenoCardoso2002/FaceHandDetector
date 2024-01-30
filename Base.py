# to colocando por enquanto para nao perder o codigo
# finalizei no dia 29/01/2024 mais ou menos as 21:10
# as 21:13 tava funcionando ;-;
# importações:
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

class faceHandDetector():
    # função de inicialização da classe:
    def __init__(self):
        self.indiceCamera = None
        self.captura = None
        self.frame = None
        self.maoDetector = None
        self.rostoDetector = None
        self.maos = None
        self.rostos = None
    
    # função que atribui o valor do indice da camera:
    def setIndiceCamera(self):
        indice = 0
        self.indiceCamera = indice
    
    # função que retorna o valor do indice da camera:
    def getIndiceCamera(self):
        return self.indiceCamera
    
    # função que instancia o detector:
    def inicializaDetector(self):
        self.maoDetector = HandDetector(maxHands=1)
        self.rostoDetector = FaceDetector(minDetectionCon=0.75)

    # função que retorna o detector da mão:
    def getDetectorMao(self):
        return self.maoDetector

    # função que retorna o detector do rosto:
    def getDetectorRosto(self):
        return self.rostoDetector
    
    # função que inicializa a caputra de video da camera:
    def inicializaCaptura(self):
        indiceCam = self.getIndiceCamera()
        self.captura = cv2.VideoCapture(indiceCam)
    
    # função que retorna a variavel de captura do video:
    def getCaptura(self):
        return self.captura
    
    # função que atualiza o frame do video e exibe:
    def atualizaFrame(self):
        while True:
            captura = self.getCaptura()
            sucesso, frame = captura.read()
            if sucesso:
                self.setFrame(frame)
                self.inverteCamera()
                self.identificaMao()
                self.identificaRosto()
                self.fazRetangulos()
                frame = self.getFrame()
                cv2.imshow("Clique 'esc' para fechar!", frame)
                if cv2.waitKey(1) == 27:
                    break
    
    # função que atribui o valor do frame:
    def setFrame(self, frame):
        self.frame = frame
    
    # função que retorna o frame:
    def getFrame(self):
        return self.frame
    
    # função que identifica a mão:
    def identificaMao(self):
        frame = self.getFrame()
        detector = self.getDetectorMao()
        self.maos = detector.findHands(frame, False)
    
    # função que identifica o rosto:
    def identificaRosto(self):
        frame = self.getFrame()
        detector = self.getDetectorRosto()
        frame, self.rostos = detector.findFaces(frame, False)
        self.setFrame(frame)
    
    # função que retorna a rosto:
    def getRosto(self):
        return self.rostos
    
    # função que retorna a mao:
    def getMao(self):
        return self.maos
    
    # função que verifica se tem uma rosto na tela:
    def verificaRosto(self):
        rostos = self.getRosto()
        if rostos:
            return True
        else:
            return False
    
    # função que verifica se tem uma mão na tela:
    def verificaMao(self):
        mao = self.getMao()
        if len(mao) == 1:
            return True
        else:
            return False
    
    # função que define quais retangulos devem ser feitos:
    def fazRetangulos(self):
        # print("Mão ->", self.verificaMao())
        # print("Rosto ->", self.verificaRosto())
        if self.verificaMao() and self.verificaRosto():
            self.rostoMaoRetangulo()
            self.focaRosto()
            # self.salvaFrame()
        elif self.verificaMao():
            self.apenasMaoRetangulo()
        elif self.verificaRosto():
            self.apenasRostoRetangulo()   
    
    # função que inverte a imagem da camera:
    def inverteCamera(self):
        frame = self.getFrame()
        frame = cv2.flip(frame, 1)
        self.setFrame(frame)

    # retangulo de apenas mao:
    def apenasMaoRetangulo(self):
        maos = self.getMao()
        mao = maos[0]
        bbox = mao["bbox"]
        x, y, w, h = bbox
        cor = (0, 0, 255)
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)

    # retangulo de apenas mao:
    def apenasRostoRetangulo(self):
        rostos = self.getRosto()
        rosto = rostos[0]
        bbox = rosto["bbox"]
        x, y, w, h = bbox
        cor = (0, 0, 255)
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)
    
    def rostoMaoRetangulo(self):
        maos = self.getMao()
        mao = maos[0]
        bbox = mao["bbox"]
        x, y, w, h = bbox
        cor = (0, 255, 0)
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)
        rostos = self.getRosto()
        rosto = rostos[0]
        bbox = rosto["bbox"]
        x, y, w, h = bbox
        cor = (0, 255, 0)
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)

    # funçao que foca no rosto:
    def focaRosto(self):
        rostos = self.getRosto()
        rosto = rostos[0]
        bbox = rosto["bbox"]
        x, y, w, h = bbox
        x = x - 15
        y = y - 75
        w = w + 30
        h = h + 90
        cor = (255, 255, 255)
        # cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)
        novo_frame = cv2.resize(self.frame[y:y+h, x:x+w], (w, h), interpolation=cv2.INTER_LINEAR)
        self.setFrame(novo_frame)

    # função que salva o frame da camera:
    def salvaFrame(self):
        frame = self.getFrame()
        cv2.imwrite("Foto salva.jpg", frame)
    
    # função que libera os recursos da câmera:
    def libera(self):
        captura = self.getCaptura()
        captura.release()
        cv2.destroyAllWindows()

# área que instância a classe e chama as funções:
faceHandDetector = faceHandDetector()
faceHandDetector.setIndiceCamera()
faceHandDetector.inicializaCaptura()
faceHandDetector.inicializaDetector()
faceHandDetector.atualizaFrame()
faceHandDetector.libera()

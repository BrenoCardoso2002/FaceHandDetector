# Importações:
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

# Versão que faz retângulos no rostos e na mão:
class faceHandDetector():
    # função de inicialização da classe:
    def __init__(self):
        self.indiceCamera = None
        self.captura = None
        self.frame = None
        self.maoDetector = None
        self.rostoDetector = None
        self.mao = None
        self.rosto = None
        self.cor = None
    
    # função que atribuio o valor do indice da camera:
    def setIndiceCamera(self):
        indice = 0
        self.indiceCamera = indice
    
    # função que retorna o valor do indice da camera:
    def getIndiceCamera(self):
        return self.indiceCamera
    
    # função que instancia os detectore:
    def inicializaDetectores(self):
        self.maoDetector = HandDetector(maxHands=1)
        self.rostoDetector = FaceDetector(minDetectionCon=0.75)
    
    # função que retorna o detector de mão:
    def getDetectorMao(self):
        return self.maoDetector

    # função que retorna o detector de rosto:
    def getDetectorRosto(self):
        return self.rostoDetector

    # função que incializa a captura de video da camera:
    def inicializaCaptura(self):
        indiceCamera = self.getIndiceCamera()
        self.captura = cv2.VideoCapture(indiceCamera)

    # função que retorna a variavel de captura do video:
    def getCaptura(self):
        return self.captura

    # função que atribui o valor do frame:
    def setFrame(self, frame):
        self.frame = frame
    
    # função que retorna a variavel de captura do video:
    def getFrame(self):
        return self.frame
    
    # função que identifica se há uma mão:
    def identificaMao(self):
        frame = self.getFrame()
        detector = self.getDetectorMao()
        mao = detector.findHands(frame, False)
        self.setMao(mao)
    
    # função que atribui o valor da mao:
    def setMao(self, mao):
        self.mao = mao
    
    # função que retorna o valor da mao:
    def getMao(self):
        return self.mao
    
    # função que identifica se há um rosto:
    def identificaRosto(self):
        frame = self.getFrame()
        detector = self.getDetectorRosto()
        _, rosto = detector.findFaces(frame, False)
        self.setRosto(rosto)
    
    # função que atribui o valor do rosto:
    def setRosto(self, rosto):
        self.rosto = rosto
    
    # função que retorna o valor do rosto:
    def getRosto(self):
        return self.rosto
    
    # função que verifica se tem um rosto na camera:
    def verificaRosto(self):
        rosto = self.getRosto()
        if rosto:
            return True
        else:
            return False
    
    # função que verifica se tem uma mão na camera:
    def verificaMao(self):
        mao = self.getMao()
        if len(mao) == 1:
            return True
        else:
            return False
    
    # função que atribui a cor do retangulo:
    def setCor(self, indice):
        if indice == 0:
            self.cor = (0, 255, 0)
        elif indice == 1:
            self.cor = (0, 0, 255)
    
    # função que retorna o valor da cor do retangulo:
    def getCor(self):
        return self.cor

    # função que faz retangulo no rosto:
    def retanguloRosto(self):
        rostos = self.getRosto()
        rosto = rostos[0]
        bbox = rosto["bbox"]
        x, y, w, h = bbox
        cor = self.getCor()
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)
    
    # função que faz retangulo na mao:
    def retanguloMao(self):
        maos = self.getMao()
        mao = maos[0]
        bbox = mao["bbox"]
        x, y, w, h = bbox
        cor = self.getCor()
        cv2.rectangle(self.frame, (x, y), (x+w, y+h), cor, 2)

    # função que define os retangulos que serão feitos:
    def defineRetangulos(self):
        if self.verificaMao() and self.verificaRosto():
            self.setCor(0)
            self.retanguloRosto()
            self.retanguloMao()
        elif self.verificaMao():
            self.setCor(1)
            self.retanguloMao()
        elif self.verificaRosto():
            self.setCor(1)
            self.retanguloRosto()
    
    # função que atualiza o frame do video que é exibido:
    def atualizaFrame(self):
        while True:
            captura = self.getCaptura()
            sucesso, frame = captura.read()
            if sucesso:
                self.setFrame(frame)
                self.inverteCamera()
                self.identificaMao()
                self.identificaRosto()
                self.defineRetangulos()
                frame = self.getFrame()
                cv2.imshow("Clique em 'esc' para fechar!", frame)
                if cv2.waitKey(1) == 27:
                    break
    
    # função que inverte a imagem da camera:
    def inverteCamera(self):
        frame = self.getFrame()
        frame = cv2.flip(frame, 1)
        self.setFrame(frame)
    
    # função que libera os recursos da camera:
    def libera(self):
        captura = self.getCaptura()
        captura.release()
        cv2.destroyAllWindows()

# área que instância a classe e chama as funções:
faceHandDetector = faceHandDetector()
faceHandDetector.setIndiceCamera()
faceHandDetector.inicializaCaptura()
faceHandDetector.inicializaDetectores()
faceHandDetector.atualizaFrame()
faceHandDetector.libera()

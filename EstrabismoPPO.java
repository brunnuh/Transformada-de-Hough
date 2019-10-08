package br.ufma.nca.hirschberg;

import java.awt.image.BufferedImage;

import javax.media.jai.JAI;
import javax.media.jai.RenderedOp;
import javax.swing.JOptionPane;
import javax.swing.text.Segment;

import br.ufma.nca.conf.Configuracao;
import br.ufma.nca.ed.MapaLista;
import br.ufma.nca.hirschberg.purkinje.Context;
import br.ufma.nca.hirschberg.purkinje.EsccStrategyBright;
import br.ufma.nca.hirschberg.purkinje.HoughStrategyBright;
import br.ufma.nca.hirschberg.purkinje.SegmentationStrategyBright;
import br.ufma.nca.imageprocessing.Converters;
import br.ufma.nca.imageprocessing.edgedetectors.Canny;
import br.ufma.nca.imageprocessing.edgedetectors.HoughTransform;
import br.ufma.nca.imageprocessing.filters.PassaAltaFilter;
import br.ufma.nca.imageprocessing.filters.PassaBaixaFilter;
import br.ufma.nca.utils.Imagem;
import br.ufma.nca.utils.Utility;

import com.jhlabs.image.SmartBlurFilter;

public class EstrabismoPPO extends AbstractEstrabismo {
	
	/**--- PARAMETROS CANNY ----------***/
	private String KSIZE = "MASK_SIZE_5";
	
	private float FT_DER = 1.2F;
	
	private float LI = 100;
		
	private float LH = 136;
	/** -----------------------------****/
	
	
	/** Diferença permitida em pixels para o tamanho do raio entre os limbos */
	private int DIF_RAIO_LIMBO = 2;
	
	public EstrabismoPPO(RenderedOp img, MapaLista eyes, String foto, int scala, int raioMarcador, boolean imprimiSaida) {
		super(img, eyes, foto, scala, raioMarcador, imprimiSaida);
		// TODO Auto-generated constructor stub
	}
	
	@Override
	public boolean preProcessamento() {
		
		// TESTANTO FILTRO PARA MELHORAR A DETECÇÃO DO BRILHO----------
		// ---26/07/2012
		SmartBlurFilter sbf = new SmartBlurFilter();
		sbf.setHRadius(50);
		sbf.setVRadius(100);
		sbf.setThreshold(30); //123
		
		olhoDireito = img_orig.getAsBufferedImage().getSubimage(eyeD.x * zoom, eyeD.y * zoom, 30 * zoom, 30 * zoom);
		olhoEsquerdo = img_orig.getAsBufferedImage().getSubimage(eyeE.x * zoom, eyeE.y * zoom, 30 * zoom, 30 * zoom);
		
		olhoDireito = sbf.filter(olhoDireito, olhoDireito);
		olhoEsquerdo = sbf.filter(olhoEsquerdo, olhoEsquerdo);
		
		ODGray = PassaBaixaFilter.passaBaixa(olhoDireito,5);
		OEGray = PassaBaixaFilter.passaBaixa(olhoEsquerdo,5);
		//JAI.create("filestore",olhoDireito,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_OD.jpg","JPEG");
		//JAI.create("filestore",olhoEsquerdo,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_OE.jpg","JPEG");
		
		//ODGray = Imagem.ColorToGray(olhoDireito);	
		//OEGray = Imagem.ColorToGray(olhoEsquerdo);	
		
		if (imprimiSaida) {
			JAI.create("filestore",olhoDireito,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_sbf_OD.jpg","JPEG");
			JAI.create("filestore",olhoEsquerdo,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_sbf_OE.jpg","JPEG");
		}
		//------------------------------------	
		return true;
	}
	/**
	 * Realiza a localização do limbo utilizando o método de canny para detecção de bordas e a Tranformada de Hough para detecção de círculo
	 *  
	 *  */
	@Override
	public boolean localizaLimbo() {
		// TODO Auto-generated method stub
		aplicaCanny();
		
		aplicaHough();
		
		return true;
	}
	
	@Override
	public boolean localizaBrilho() {
		// TODO Auto-generated method stub
		Context context = null;
		
		olhoDireito = ODGray;
		olhoEsquerdo = OEGray;
		
		aplicaCanny();
		
		// Define a estratégia utilizada na localização do brilho
		int estrategia = Utility.returnIndex(Configuracao.ESTRATEGIA_BRILHO, "TH", "ESCC");
		 switch (estrategia) {
		 	// case 0 : context = new Context(new SegmentationStrategyBright(getODCinza(), getOECinza())); break; 
	         case 0 : context = new Context(new HoughStrategyBright (OD, OE,2,6)); break;  
	         case 1 : context = new Context(new EsccStrategyBright()); break;  
         default : JOptionPane.showMessageDialog(null, "Configure a estratégia utilizada na localização do Brilho");  
		 }  
		
		BufferedImage imgD = null;
		BufferedImage imgE = null;
		
		//PlanarImage pi = PlanarImage.wrapRenderedImage(imgD);
		imgD = Converters.pegaLimbo(olhoDireito,OD,Rd-3); //Converters.pegaLimbo(pi.getAsBufferedImage(), OD, Rd-3, true);
		//pi = PlanarImage.wrapRenderedImage(imgE);
		imgE = Converters.pegaLimbo(olhoEsquerdo,OE,Re-3);//Converters.pegaLimbo(pi.getAsBufferedImage(), OE, Re-3, true);
				
		MapaLista resultA = context.executeStrategy(imgD,imgE);
		
		OBD = resultA.pega(1);
		OBE = resultA.pega(2);
		
		if (imprimiSaida) {
			JAI.create("filestore",imgD,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_sbf_limbo_OD.jpg","JPEG");
			JAI.create("filestore",imgE,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\SmartFilter\\"+foto+"_sbf_imbo_OE.jpg","JPEG");
		}
		
		return true;		
	}
	
	/**
	 * Aplica método de Canny (Detector de Bordas)
	 * @return true
	 */
	private boolean aplicaCanny(){
		
		Canny c = new Canny(olhoDireito,FT_DER,KSIZE,LI,LH); //1.0F,"MASK_SIZE_5",100,136
		olhoDireito = c.aplicaMetodo();
		olhoDireito = Imagem.excluiBorda(olhoDireito,10);
		
		//JAI.create("filestore",olhoDireito,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\Canny\\"+foto+"OD1.jpg","JPEG");
		
		c = new Canny(olhoEsquerdo,FT_DER,KSIZE,LI,LH); // 1.0F,"MASK_SIZE_5",100,136
		olhoEsquerdo = c.aplicaMetodo();		
		olhoEsquerdo = Imagem.excluiBorda(olhoEsquerdo,10);
		
		//JAI.create("filestore",olhoEsquerdo,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\Canny\\"+foto+"OE1.jpg","JPEG");
		
		c = new Canny(olhoDireito,FT_DER,KSIZE,LI,LH); // 1.0F,"MASK_SIZE_5",100,136
		olhoDireito = c.aplicaMetodo();
		olhoDireito = Imagem.excluiBorda(olhoDireito,10);
		
		//JAI.create("filestore",olhoDireito,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\Canny\\"+foto+"OD2.jpg","JPEG");
		
		c = new Canny(olhoEsquerdo,FT_DER,KSIZE,LI,LH); // 1.0F,"MASK_SIZE_5",100,136
		olhoEsquerdo = c.aplicaMetodo();
		olhoEsquerdo = Imagem.excluiBorda(olhoEsquerdo,10);
		
		if (imprimiSaida) {
		 JAI.create("filestore",olhoDireito,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\Canny\\"+foto+"OD.jpg","JPEG");
		 JAI.create("filestore",olhoEsquerdo,"F:\\Meus Documentos\\Doutorado\\Resultados\\Hirschberg\\Canny\\"+foto+"OE.jpg","JPEG");
		}
		return true;
	}
	
	private boolean aplicaHough() {
		int qtd = 80;
		int rMin = (int)(Configuracao.ZOOM * Configuracao.RAIO_MIN_LIMBO)/40;  // o valor 15 era usado para zoom de 40%
		int rMax = 	(int)(Configuracao.ZOOM * Configuracao.RAIO_MAX_LIMBO)/40; //o valor 37 era usado para zoom de 40%
		
		// -------------------BUSCA LIMBO DIREITO -------------------------------
		HoughTransform h = new HoughTransform(olhoDireito, rMin , rMax);  //15 e 37 usado para ZOOM de 40% 
		houghD =  h.applyMethod(qtd, 1.03f, 6f); //7.5f
		
		//Ordena os elementos em ordem crescente
		houghD = h.ordenaHough(houghD);
		
		// O último elemento é o maior
		int maiorD = houghD[qtd-1][3];
		OD.x = houghD[qtd-1][0];
		OD.y = houghD[qtd-1][1]; 
		Rd = houghD[qtd-1][2];
		
		// Busca os pontos iguais  de maior pico pega o de menor Raio dentre eles
		/* COMENTADO DIA: 06/08/2012  */
		for (int x = qtd-2; x >= 0; x--){
			if ((maiorD == houghD[x][3]) && (houghD[x][2] < Rd)){
				OD.x = houghD[x][0];
				OD.y = houghD[x][1]; 
				Rd = houghD[x][2];
			}
			else x = 0;
		}
		
		//-----------------BUSCA LIMBO ESQUERDO -------------------------------
		
		h = new HoughTransform(olhoEsquerdo, rMin, rMax); //15,37 //80,120 
		houghE =  h.applyMethod(qtd, 1.03f, 6f); //7.5f
		
		houghE = h.ordenaHough(houghE);
	
		int maiorE = houghE[qtd-1][3];
		OE.x = houghE[qtd-1][0];
		OE.y = houghE[qtd-1][1]; 
		Re = houghE[qtd-1][2];
		
		/* COMENTADO DIA: 06/08/2012 */
		for (int x = qtd-2; x >= 0; x--){
			if ((maiorE == houghE[x][3]) && (houghE[x][2] < Re)){
				OE.x = houghE[x][0];
				OE.y = houghE[x][1]; 
				Re = houghE[x][2];
			}
			else x = 0;
		}
	

		//--COMPARA OS LIMBOS E BUSCA OS QUE APRESENTAM CARACTERISTICAS MAIS PRÓXIMAS (RAIO, LOCALIZAÇAO)
		if (Math.abs(Rd - Re) > DIF_RAIO_LIMBO){
			if (Rd < Re){
				
				for (int x = qtd-2; x >= 0; x--){
					// Removi: (houghE[x][2] - Rd >=0) 
					// data: 02/02/2012
					// OBS: O Ideial seria verificar o raio de acordo com o tipo de imagem (LEVO e DEXTRO)
					if ((houghE[x][2] - Rd <= DIF_RAIO_LIMBO) ){ //&& 
						OE.x = houghE[x][0];
						OE.y = houghE[x][1]; 
						Re = houghE[x][2];
			
						// COMENTADO DIA 06/08/2012-------MELHORAR ESSA PARTE!!!!!!!!!!!
						/*int menorY = 100000;
						for (int y = x-1; y >= 0; y--){
							if ((Math.abs(houghE[y][1] - OD.y) <= menorY) && (Re == houghE[y][2])){
								menorY = Math.abs(houghE[y][1] - OD.y);
								OE.x = houghE[y][0];
								OE.y = houghE[y][1];
							}
							else y = 0;
						} */
						x = 0;
					}
				}
			}
			else {
				for (int x = qtd-2; x >= 0; x--){
					if ((houghD[x][2] - Re <= DIF_RAIO_LIMBO)){ // && (houghD[x][2] - Re >=0)){
						OD.x = houghD[x][0];
						OD.y = houghD[x][1]; 
						Rd = houghD[x][2];
						// COMENTADO DIA 06/08/2012-------MELHORAR ESSA PARTE!!!!!!!!!!!
						/*int menorY = 100000;
						for (int y = x-1; y >= 0; y--){
							if ((Math.abs(houghD[y][1] - OE.y) <= menorY) && (Rd == houghD[y][2])){
								menorY = Math.abs(houghD[y][1] - OE.y);
								OD.x = houghD[y][0];
								OD.y = houghD[y][1];
							}
							else y = 0;
						}*/ 
						x = 0;
					}
				}
			}
		}
		
		return true;
	}
	
	/*
	private BufferedImage getODCinza() {
		return Imagem.ColorToGray(img_orig.getAsBufferedImage().getSubimage(eyeD.x * zoom, eyeD.y * zoom, 30 * zoom, 30 * zoom));
	}
	
	private BufferedImage getOECinza() {
		return Imagem.ColorToGray(img_orig.getAsBufferedImage().getSubimage(eyeE.x * zoom, eyeE.y * zoom, 30 * zoom, 30 * zoom));
	}
	*/
	
}

package pnml2grgen;

import java.io.File;

import fr.lip6.move.pnml.framework.general.PNType;
import fr.lip6.move.pnml.framework.hlapi.HLAPIRootClass;
import fr.lip6.move.pnml.framework.utils.PNMLUtils;
import jgrsi.GrFile;
import run.BaseConvert;

public class Convert extends BaseConvert {

	@Override
	public String convertFile(String fileName) {
		File f = new File(fileName);
		GrFile a = null;
		try {
			// Load the document. No fall back to any compatible type (false).
			// Fall back takes place between an unknown Petri Net type and the CoreModel.
			HLAPIRootClass rc = PNMLUtils.importPnmlDocument(f, false);
			// Determine the Petri Net Document type... See code snippets below

			// System.out.println("Imported document workspace ID: " + ModelRepository.getInstance().getCurrentDocWSId());
			a = processDocument(rc);

		} catch (Exception e) {
			e.printStackTrace();
		}

		if (a == null) {
			System.err.print("No AST generated");
		} else {
			StringBuilder b = generateGrsi(a);
			System.out.print(b.toString());
			return b.toString();
		}
		return null;
	}

	protected static GrFile processDocument(HLAPIRootClass rc) throws Exception {
		GrFile a = null;
		PNType type = PNMLUtils.determinePNType(rc);
		switch (type) {
		case COREMODEL:
			// process the Core Model document, get the right type first
			fr.lip6.move.pnml.pnmlcoremodel.hlapi.PetriNetDocHLAPI coreDoc = (fr.lip6.move.pnml.pnmlcoremodel.hlapi.PetriNetDocHLAPI) rc;
			/// ...
			System.out.println("Coremodel (not supported)");
			break;
		case PTNET:
			// process the Place/Transition Net document, get the right type first
			fr.lip6.move.pnml.ptnet.hlapi.PetriNetDocHLAPI ptDoc = (fr.lip6.move.pnml.ptnet.hlapi.PetriNetDocHLAPI) rc;
			System.out.println("PTNET");
			PtNet n = new PtNet();
			n.log = false;
			a = n.process(ptDoc);
			break;
		case SYMNET:
			// process the Symmetric Net document, get the right type first
			fr.lip6.move.pnml.symmetricnet.hlcorestructure.hlapi.PetriNetDocHLAPI snDoc = (fr.lip6.move.pnml.symmetricnet.hlcorestructure.hlapi.PetriNetDocHLAPI) rc;
			System.out.println("symnet (not supported)");
			break;
		case HLPN:
			// process the High-level Petri Net Document, get the right type first
			fr.lip6.move.pnml.hlpn.hlcorestructure.hlapi.PetriNetDocHLAPI hlpnDoc = (fr.lip6.move.pnml.hlpn.hlcorestructure.hlapi.PetriNetDocHLAPI) rc;
			System.out.println("hlpn");
			break;
		case PTHLPN:
			// process the P/T Net in high-level notation, get the right type first
			fr.lip6.move.pnml.pthlpng.hlcorestructure.hlapi.PetriNetDocHLAPI pthlpnDoc = (fr.lip6.move.pnml.pthlpng.hlcorestructure.hlapi.PetriNetDocHLAPI) rc;
			System.out.println("pthlpn (not supported)");
			break;
		default:
			System.out.println("Unknown (not supported)");
			break;
		}
		return a;
	}

	protected static StringBuilder generateGrsi(GrFile a) {
		StringBuilder b = new StringBuilder();
		a.prettyPrint(b);
		return b;
	}

}

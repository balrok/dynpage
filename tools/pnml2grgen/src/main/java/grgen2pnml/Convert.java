package grgen2pnml;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;

import fr.lip6.move.pnml.framework.general.PnmlExport;
import fr.lip6.move.pnml.framework.utils.ModelRepository;
import fr.lip6.move.pnml.framework.utils.exception.BadFileFormatException;
import fr.lip6.move.pnml.framework.utils.exception.OCLValidationFailed;
import fr.lip6.move.pnml.framework.utils.exception.OtherException;
import fr.lip6.move.pnml.framework.utils.exception.UnhandledNetType;
import fr.lip6.move.pnml.framework.utils.exception.ValidationFailedException;
import fr.lip6.move.pnml.ptnet.hlapi.PetriNetDocHLAPI;
import run.BaseConvert;

import grgenreader.Reader;
import jgrsi.GrFile;

public class Convert extends BaseConvert {

	@Override
	public String convertFile(String fileName) {
		Mapper mapper = new Mapper();
		PetriNetDocHLAPI doc;
		Reader r = new Reader();
		GrFile grsiFile = r.read(fileName);
		
		try {
			doc = mapper.convert(grsiFile);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}

		ModelRepository mr = ModelRepository.getInstance();
		mr.setPrettyPrintStatus(true);

		PnmlExport pex = new PnmlExport();
		try {
			Path tmp =  Files.createTempFile("pnml", ".pnml");
			// System.out.println(tmp.toString());
			pex.exportObject(doc, tmp.toString(), true);
			return String.join("\n", Files.readAllLines(tmp));
		} catch (UnhandledNetType | OCLValidationFailed | IOException | ValidationFailedException
				| BadFileFormatException | OtherException e) {
			e.printStackTrace();
		}
		return null;
	}

}

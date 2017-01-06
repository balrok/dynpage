package grgen2net;

import grgenreader.Reader;
import jgrsi.GrFile;
import grgen2net.Mapper;
import run.BaseConvert;
import jnet.NetFile;

public class Convert extends BaseConvert {

	@Override
	public String convertFile(String fileName) {
		Reader r = new Reader();
		GrFile grsiFile = r.read(fileName);

		Mapper mapper = new Mapper();
		NetFile netFile;
		
		try {
			netFile = mapper.convert(grsiFile);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			netFile = null;
		}
		
		if (netFile == null) {
			System.err.print("No AST generated");
		} else {
			StringBuilder b = generateNet(netFile);
			System.out.print(b.toString());
			return b.toString();
		}
		return null;
	}

	protected static StringBuilder generateNet(NetFile a) {
		StringBuilder b = new StringBuilder();
		a.prettyPrint(b);
		return b;
	}
}

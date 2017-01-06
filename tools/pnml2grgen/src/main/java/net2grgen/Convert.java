package net2grgen;

import netreader.Reader;
import jgrsi.GrFile;
import jnet.NetFile;
import run.BaseConvert;

public class Convert extends BaseConvert {

	@Override
	public String convertFile(String fileName) {
		Reader r = new Reader();
		NetFile netFile = r.read(fileName);
		GrFile a;

		Mapper mapper = new Mapper();

		try {
			a = mapper.convert(netFile);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			a = null;
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
	
	protected static StringBuilder generateGrsi(GrFile a) {
		StringBuilder b = new StringBuilder();
		a.prettyPrint(b);
		return b;
	}

}
